"""v04: base instrumental original 104 BPM (do v03) + Foley de interface deterministico nos tempos do v04. Sem voz, sem amostras."""
import math, random, wave, array
from pathlib import Path
RATE=48000;DURATION=18;N=RATE*DURATION
left=array.array('f',[0])*N;right=array.array('f',[0])*N
rng=random.Random(20261005)
def add(at,duration,fn,gain=1,pan=0):
    start=round(at*RATE);count=min(round(duration*RATE),N-start)
    for j in range(max(0,count)):
        t=j/RATE;v=gain*fn(t,j,duration)
        left[start+j]+=v*(.8-.2*pan);right[start+j]+=v*(.8+.2*pan)
def note(at,freq,duration,gain=.07,pan=0):
    def fn(t,j,d):
        env=(1-math.exp(-t*38))*math.exp(-t*2.5)*(min(1,(d-t)/.12))
        return env*(math.sin(2*math.pi*freq*t)+.25*math.sin(4*math.pi*freq*t)+.1*math.sin(6*math.pi*freq*t))
    add(at,duration,fn,gain,pan)
beat=60/104
chords=[(146.832,185,220,277.18),(123.471,146.832,185,246.942),(97.999,146.832,195.998,246.942),(110,146.832,220,277.18)]
for bar in range(8):
    at=bar*4*beat;chord=chords[bar%4]
    for k,f in enumerate(chord):note(at+.03*k,f,2.2,.035,(k-1.5)/2)
    for k in range(8):note(at+k*beat/2,chord[k%4]*2,.48,.035,math.sin(k))
    note(at,chord[0]/2,1.6,.095)
for k in range(32):
    at=k*beat
    add(at,.24,lambda t,j,d:math.sin(2*math.pi*(48*t+35*.018*(1-math.exp(-t/.018))))*math.exp(-t*24),.18)
    add(at+beat/2,.055,lambda t,j,d:rng.uniform(-1,1)*math.exp(-t*95),.018,.2)
    if k%2:add(at,.12,lambda t,j,d:(rng.uniform(-1,1)*.7+math.sin(2*math.pi*190*t)*.3)*math.exp(-t*35),.038)
# --- Efeitos de interface sincronizados com o v04 (tempos em segundos do filme) ---
def whoosh(at,dur,gain=.06,pan=0):
    add(at,dur,lambda t,j,d:rng.uniform(-1,1)*math.sin(math.pi*t/d)**3*(.55+.45*math.sin(2*math.pi*9*t/d)**2),gain,pan)
def tick(at,gain=.027,pan=0,hz=1300):
    add(at,.025,lambda t,j,d:(rng.uniform(-1,1)*.6+math.sin(2*math.pi*hz*t)*.4)*math.exp(-t*190),gain,pan)
def typing(start,count,duration,gain=.027):
    for k in range(count):
        tick(start+(k+.5)*duration/count,gain,.1*math.sin(k*1.7))
# 1: ticket entra e a pergunta e digitada
add(0.0,.34,lambda t,j,d:math.sin(2*math.pi*(70*t))*math.exp(-t*14),.16)
whoosh(0.0,.7,.05,-.2)
typing(0.0,12,.5);typing(.5,12,.4)
note(.88,880,.3,.03,.15)
whoosh(2.85,.5,.05,.2)
# 2: carrossel
whoosh(3.0,.65,.055)
for at in (4.9,6.5,8.1,9.7):
    whoosh(at,.62,.05,.25)
    add(at+.3,.05,lambda t,j,d:math.sin(2*math.pi*520*t)*math.exp(-t*60),.03)
whoosh(11.2,.45,.05,-.2)
# 3: carrinho
whoosh(11.55,.65,.055)
typing(12.4,14,.8)
add(13.5,.045,lambda t,j,d:(math.sin(2*math.pi*760*t)+rng.uniform(-1,1)*.3)*math.exp(-t*120),.065)
add(13.58,.47,lambda t,j,d:math.sin(2*math.pi*(420+520*(t/d))*t)*math.sin(math.pi*t/d),.016)
note(14.1,739.99,.28,.04,-.2);note(14.22,987.77,.45,.034,.2);note(14.36,1318.51,.5,.026,0)
whoosh(15.3,.45,.05,.1)
# 4: fechamento
whoosh(15.55,.5,.045)
add(15.82,.55,lambda t,j,d:(math.sin(2*math.pi*(62*t+20*(1-math.exp(-t/.05))))*math.exp(-t*7))+.25*math.sin(2*math.pi*1480*t)*math.exp(-t*9),.19)
note(16.2,659.25,.5,.03,-.15)
typing(16.5,24,.75)
whoosh(17.3,.35,.035,.2)
out=Path(__file__).parent/'filme'/'assets'/'audio-v04.wav'
samples=array.array('h')
for i in range(N):
    t=i/RATE;fade=min(1,t/.3,(DURATION-t)/.25)
    for channel in (left,right):samples.append(round(32767*max(-.99,min(.99,channel[i]*fade))))
with wave.open(str(out),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(samples.tobytes())
print(out)
