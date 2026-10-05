"""Original 104 BPM instrumental and deterministic UI Foley, no voice or samples."""
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
# Paper fibres, broad swipe and slight irregular flutter.
add(2.1,1.8,lambda t,j,d:rng.uniform(-1,1)*math.sin(math.pi*t/d)**2*(.5+.5*math.sin(2*math.pi*19*t)**2),.075,-.3)
for at in (5.65,7.4,9.4,13.9):
    add(at,.8,lambda t,j,d:rng.uniform(-1,1)*math.sin(math.pi*t/d)**3*.6,.042)
for start,text,duration in ((10.9,'PRIMEIRACOMPRA',1.05),(15.4,'www.casadofitness.com.br',1.0)):
    for k in range(len(text)):
        add(start+(k+.5)*duration/len(text),.025,lambda t,j,d:(rng.uniform(-1,1)*.6+math.sin(2*math.pi*1300*t)*.4)*math.exp(-t*190),.027,.1)
add(12.22,.045,lambda t,j,d:(math.sin(2*math.pi*760*t)+rng.uniform(-1,1)*.3)*math.exp(-t*120),.065)
note(12.38,739.99,.26,.035,-.2);note(12.50,987.77,.4,.03,.2)
out=Path(__file__).parent/'filme'/'assets'/'audio-v03.wav'
samples=array.array('h')
for i in range(N):
    t=i/RATE;fade=min(1,t/.3,(DURATION-t)/.25)
    for channel in (left,right):samples.append(round(32767*max(-.99,min(.99,channel[i]*fade))))
with wave.open(str(out),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(samples.tobytes())
print(out)
