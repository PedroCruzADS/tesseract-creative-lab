"""Trilha instrumental simples e ORIGINAL (sintetizada aqui, sem amostras de terceiros), para os vídeos de mídia paga.

Por ser gerada por código, não há licença de terceiros a cumprir: a trilha é do próprio workspace e pode ser usada em anúncios.
141 BPM (1 compasso = 1,7 s; 2 compassos = 3,4 s, a duração de cada carta do carrossel), progressão Am - F - C - G - Am.
Camadas: bumbo suave, palma nos tempos 2 e 4, chimbal, baixo, pad, arpejo e subida de ruído antes de cada troca.
Saída: WAV estéreo 44,1 kHz em assets/audio/trilha-simples-17s.wav

Uso: python scripts/gerar_trilha_simples.py
"""
from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
OUT = LAB / "assets" / "audio" / "trilha-simples-17s.wav"
SR = 44100
BEAT = 0.425                   # 141,18 BPM
BAR = BEAT * 4
SECONDS = 17.0
N = int(SR * SECONDS)
rng = np.random.default_rng(7)

CHORDS = [  # (raiz do baixo, notas do acorde) em Hz
    (110.00, (220.00, 261.63, 329.63)),   # Am
    (87.31, (174.61, 220.00, 261.63)),    # F
    (130.81, (261.63, 329.63, 392.00)),   # C
    (98.00, (196.00, 246.94, 293.66)),    # G
    (110.00, (220.00, 261.63, 329.63)),   # Am
]


def t_axis(n: int) -> np.ndarray:
    return np.arange(n) / SR


def env(n: int, a: float, d: float, s: float, r: float) -> np.ndarray:
    e = np.ones(n)
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na, endpoint=False) if na else 1
    if nd:
        e[na:na + nd] = np.linspace(1, s, nd)
    e[na + nd:] = s
    if nr and nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def lowpass(x: np.ndarray, hz: float) -> np.ndarray:
    a = np.exp(-2 * np.pi * hz / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def put(buf: np.ndarray, start: float, sig: np.ndarray, gain: float = 1.0, pan: float = 0.0) -> None:
    i = int(start * SR)
    if i >= buf.shape[0]:
        return
    sig = sig[: buf.shape[0] - i] * gain
    buf[i:i + len(sig), 0] += sig * (1 - max(pan, 0))
    buf[i:i + len(sig), 1] += sig * (1 + min(pan, 0))


def kick() -> np.ndarray:
    n = int(0.28 * SR)
    t = t_axis(n)
    f = 52 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def clap() -> np.ndarray:
    n = int(0.22 * SR)
    t = t_axis(n)
    ruido = rng.standard_normal(n)
    ruido = lowpass(ruido, 5200) - lowpass(ruido, 900)
    return ruido * (np.exp(-t * 22) + 0.5 * np.exp(-((t - 0.012) ** 2) * 9000)) * 0.9


def hat() -> np.ndarray:
    n = int(0.07 * SR)
    t = t_axis(n)
    ruido = rng.standard_normal(n)
    ruido = ruido - lowpass(ruido, 6500)
    return ruido * np.exp(-t * 60)


def tom(freq: float, dur: float, wave_: str = "saw", harm: int = 6) -> np.ndarray:
    n = int(dur * SR)
    t = t_axis(n)
    if wave_ == "sine":
        return np.sin(2 * np.pi * freq * t)
    sig = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, harm + 1))
    return sig * 0.6


def pad(freqs: tuple[float, ...], dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = t_axis(n)
    sig = np.zeros(n)
    for f in freqs:
        for det in (-0.004, 0.0, 0.004):
            sig += np.sin(2 * np.pi * f * (1 + det) * t) + 0.35 * np.sin(2 * np.pi * 2 * f * (1 + det) * t)
    sig = lowpass(sig, 1700)
    return sig * env(n, 0.25, 0.4, 0.8, 0.5) / (len(freqs) * 3)


def subida(dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = t_axis(n)
    ruido = rng.standard_normal(n)
    brilho = ruido - lowpass(ruido, 1200)
    return brilho * (t / dur) ** 2.2 * 0.5


def main() -> None:
    mix = np.zeros((N, 2))
    k, c, h = kick(), clap(), hat()
    for b in range(int(SECONDS / BEAT) + 1):
        tt = b * BEAT
        if tt >= SECONDS:
            break
        sec = min(int(tt // (BAR * 2)), 4)
        raiz, acorde = CHORDS[sec]
        compasso_fim = (b % 8) >= 6            # últimos dois tempos de cada carta: sem bumbo, só a subida
        if b % 8 != 7 or True:
            if not (b % 8 == 7):
                put(mix, tt, k, 0.55 if not compasso_fim else 0.0)
        if b % 2 == 1 and not compasso_fim:
            put(mix, tt, c, 0.20)
        for m in (0, 1):                      # chimbal nos contratempos e semicolcheias leves
            put(mix, tt + BEAT * 0.5 * m + (BEAT * 0.5 if m == 0 else 0) * 0, h, 0.10 if m == 0 else 0.05, pan=0.2 if m else -0.2)
        # baixo em colcheias
        for m in range(2):
            tb = tt + m * BEAT / 2
            if tb < SECONDS:
                nb = int(BEAT / 2 * SR)
                sig = lowpass(tom(raiz if m == 0 else raiz * 2, BEAT / 2, "saw", 5), 420) * env(nb, 0.004, 0.06, 0.7, 0.04)
                put(mix, tb, sig, 0.32 if m == 0 else 0.18)
        # arpejo em colcheias
        for m in range(2):
            tb = tt + m * BEAT / 2
            nota = acorde[(b * 2 + m) % 3] * 2
            nb = int(0.2 * SR)
            sig = tom(nota, 0.2, "saw", 4) * env(nb, 0.003, 0.05, 0.25, 0.1)
            put(mix, tb, lowpass(sig, 3800), 0.07, pan=-0.35 if (b + m) % 2 == 0 else 0.35)
    for s in range(5):
        raiz, acorde = CHORDS[s]
        ini = s * BAR * 2
        if ini < SECONDS:
            put(mix, ini, pad(acorde, min(BAR * 2 + 0.3, SECONDS - ini + 0.3)), 0.55)
        if s < 4:
            fim = (s + 1) * BAR * 2
            put(mix, fim - BEAT * 2, subida(BEAT * 2), 0.18)
    # fecha com fade; normaliza para pico de -3 dBFS
    fade = int(1.2 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))[:, None]
    pico = np.abs(mix).max()
    mix = mix / pico * 0.708
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pcm = (mix * 32767).astype("<i2")
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(OUT, f"{N / SR:.1f} s")


if __name__ == "__main__":
    main()
