"""Animate the approved CDF search storyboard in Tesseract and export the film.

The storyboard is preserved under versoes/v01 before the animated master replaces it.
"""
from __future__ import annotations

import json
import argparse
import math
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

from build_cdf_mix import Builder, EASE_INOUT, EASE_OUT, LINEAR, keys, tr
from build_cdf_search_storyboard import BLACK, GREY, INK, LAB, OFFWHITE, OUT, RED, WHITE, run

WORK = OUT / ".tesseract-work" / "film"
STORYBOARD = OUT / "projeto" / "quadrado-1x1.tsrct"
FILM_PROJECT = WORK / "quadrado-1x1-film.tsrct"
MP4_SILENT = WORK / "silent_4k60.mp4"
MP4_FINAL = OUT / "cdf-busca-categorias_quadrado-1x1_v02.mp4"
AUDIO = WORK / "trilha-original.wav"
SCENES = {
    0: (0, 3200),
    2500: (3200, 2200),
    4300: (5400, 3600),
    6500: (9000, 3700),
}
END_START = 12700
TOTAL_MS = 15000


def sound(duration: float = 15, typing: tuple[float, float] = (1.05, 2.65),
          transitions: tuple[float, ...] = (3.18, 5.38, 8.98, 12.68),
          output: Path | None = None) -> None:
    """Original, deterministic, voice-free electronic score and sparse SFX."""
    sr = 48000
    n = int(duration * sr)
    time = np.arange(n, dtype=np.float64) / sr
    out = np.zeros(n, dtype=np.float64)
    bpm = 124
    beat = 60 / bpm
    rng = np.random.default_rng(20260928)

    def place(signal: np.ndarray, start: float, gain: float = 1.0) -> None:
        i = int(start * sr)
        if i < 0 or i >= n:
            return
        end = min(n, i + len(signal))
        out[i:end] += signal[: end - i] * gain

    # Warm pulse; deliberately more spacious than a fast product montage.
    chords = [(130.81, 155.56, 196.00), (116.54, 146.83, 174.61),
              (130.81, 164.81, 196.00), (116.54, 155.56, 196.00)]
    for bar in range(math.ceil(duration / (4 * beat))):
        start = bar * 4 * beat
        if start >= duration:
            break
        length = min(int(4 * beat * sr), n - int(start * sr))
        t = np.arange(length) / sr
        env = np.minimum(1.0, t / 0.35) * np.minimum(1.0, (length / sr - t) / 0.5)
        pad = sum(np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * 2 * f * t)
                  for f in chords[bar % 4]) / 3
        place(pad * env * 0.072, start)
    for k in range(math.ceil(duration / beat)):
        start = k * beat
        if start >= duration:
            break
        t = np.arange(int(0.22 * sr)) / sr
        kick = np.sin(2 * np.pi * (58 * t + 25 * np.exp(-27 * t) * t)) * np.exp(-22 * t)
        place(kick, start, 0.15 if start >= 3.2 else 0.08)
        if k % 2 == 1 and start >= 3.2:
            h = rng.normal(0, 1, int(0.055 * sr))
            h = np.concatenate(([0], np.diff(h)))[: len(h)]
            h *= np.exp(-np.linspace(0, 7, len(h)))
            place(h, start, 0.014)
    # Typing and transition details, all synthesized rather than borrowed music.
    for start in np.arange(typing[0], typing[1], 0.15):
        t = np.arange(int(0.028 * sr)) / sr
        click = (np.sin(2 * np.pi * 1150 * t) + 0.3 * np.sin(2 * np.pi * 1700 * t)) * np.exp(-155 * t)
        place(click, float(start), 0.025)
    for start in transitions:
        t = np.arange(int(0.45 * sr)) / sr
        noise = rng.normal(0, 1, len(t))
        noise = np.convolve(noise, np.ones(25) / 25, mode="same")
        whoosh = noise * np.sin(np.pi * np.clip(t / 0.45, 0, 1)) ** 1.5
        place(whoosh, start - 0.22, 0.06)
    out = np.tanh(out * 1.7)
    peak = max(1e-9, np.max(np.abs(out)))
    out *= 0.88 / peak
    pcm = np.int16(np.clip(out, -1, 1) * 32767)
    destination = output or AUDIO
    destination.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destination), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(pcm.tobytes())


def animate() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    archive = OUT / "versoes" / "v01" / "projeto" / "quadrado-1x1.tsrct"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        shutil.copy2(STORYBOARD, archive)
        old_previews = OUT / "versoes" / "v01" / "previews"
        old_previews.mkdir(parents=True, exist_ok=True)
        for still in ("f040.png", "f086.png", "f150.png", "f230.png"):
            shutil.copy2(OUT / "previews" / still, old_previews / still)
    if FILM_PROJECT.exists():
        raise RuntimeError("Film work project exists; review it before re-running")
    shutil.copy2(STORYBOARD, FILM_PROJECT)
    editable = WORK / "editable.json"
    run("project", "checkout", "--project", str(FILM_PROJECT), "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    doc["duration"] = 15.0
    # Retime approved compositions; original .tsrct remains untouched in v01.
    doc["composition"]["layers"] = [x for x in doc["composition"]["layers"] if x["id"] != 15]
    for layer in doc["composition"]["layers"]:
        old_start = layer["activeRange"]["start"]
        if old_start in SCENES:
            start, dur = SCENES[old_start]
            layer["activeRange"] = {"start": start, "duration": dur}
    # Keep the official white logo unchanged on the end card.
    doc["composition"]["layers"].insert(0, {
        "type": "Image", "id": 708, "name": "Assinatura CDF end card",
        "activeRange": {"start": END_START, "duration": TOTAL_MS - END_START},
        "transform": tr(540, 555, (1200, 164), 26),
        "source": {"assetId": "cdf-logo-white", "fit": "contain"},
    })
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", str(FILM_PROJECT), "--file", str(editable))

    # Fonts already imported in the project; recover their exact family/style names.
    source_font = next(x["sourceText"] for x in doc["composition"]["layers"] if x.get("id") == 204)
    title_font = next(x["sourceText"] for x in doc["composition"]["layers"] if x.get("id") == 302)
    fonts = {
        "medium": (source_font["fontFamily"], source_font["fontStyle"]),
        "semibold": (source_font["fontFamily"], "SemiBold"),
        "bold": (title_font["fontFamily"], title_font["fontStyle"]),
    }
    b = Builder(1080, fonts)
    # A live query, not a static block of copy.
    for lid, s, dur, phrase in (
        (500, 1000, 540, "esteiras,"),
        (501, 1540, 450, "esteiras, bicicletas,"),
        (502, 1990, 450, "esteiras, bicicletas, equipamentos"),
        (503, 2440, 760, "esteiras, bicicletas, equipamentos para academia"),
    ):
        b.text(lid, "Busca digitada", s, dur, 244, 557, 680, 58, phrase,
               "medium", 27 if lid == 503 else 32, INK)
    # Micro-details make the interface feel inhabited without competing with the journey.
    b.text(510, "S1 search hint", 2200, 980, 193, 768, 650, 35,
           "Uma busca. Muitas formas de se mover.", "medium", 23, GREY)
    b.rect(520, "S3 selection line", 6950, 2050, 74, 680, 220, 5, RED, 3)
    b.text(521, "S3 category index", 7600, 1300, 78, 1007, 860, 34,
           "ESTEIRAS   /   BICICLETAS   /   E MUITO MAIS", "semibold", 23, GREY)
    b.text(530, "S4 index", 9250, 3400, 801, 213, 200, 42, "01 / 02", "medium", 27, GREY, "right")
    b.rect(700, "End fundo", END_START, 2300, 0, 0, 1080, 1080, BLACK)
    b.rect(701, "End linha", END_START, 2300, 235, 678, 610, 8, RED, 4)
    b.text(702, "End copy", END_START, 2300, 150, 718, 780, 62,
           "O movimento começa aqui.", "semibold", 38, WHITE, "center")
    b.text(703, "End URL", END_START, 2300, 150, 794, 780, 48,
           "casadofitness.com.br", "medium", 29, [0.72, 0.73, 0.76, 1], "center")
    # Brand-color wipes bridge scene boundaries without a crossfade or a dead frame.
    for i, cut in enumerate((3200, 5400, 9000, END_START)):
        b.rect(720 + i, f"Transição vermelha {i+1}", cut - 310, 620,
               -1320, 0, 1320, 1080, RED)
    acts = [{**a, "insertIndex": 0} for a in b.front]
    run_file = WORK / "new_layers.json"
    run_file.write_text(json.dumps(acts, ensure_ascii=False), encoding="utf-8")
    run("project", "apply", "--project", str(FILM_PROJECT), "--actions", str(run_file))

    # Read back exact final positions after all layers are committed.
    run("project", "checkout", "--project", str(FILM_PROJECT), "--output", str(editable))
    document = json.loads(editable.read_text(encoding="utf-8"))
    lookup = {x["id"]: x for x in document["composition"]["layers"]}
    anim = []

    def lift(lids: list[int], delay: int, amount: float = 34, duration: int = 560,
             drift: float = -5) -> None:
        for lid in lids:
            layer = lookup.get(lid)
            if not layer:
                continue
            local_duration = layer["activeRange"]["duration"]
            y = layer["transform"]["position"][1]
            anim.append(keys(lid, "positionY", [(0, y + amount, LINEAR),
                                                  (delay, y + amount, LINEAR),
                                                  (delay + duration, y, EASE_OUT),
                                                  (local_duration, y + drift, LINEAR)]))
            anim.append(keys(lid, "opacity", [(0, 0, LINEAR), (delay, 0, LINEAR),
                                                (delay + min(duration, 430), 100, EASE_OUT),
                                                (local_duration, 100, LINEAR)]))

    lift([10, 11], 150, 42, 650)
    lift([12, 13, 14], 650, 72, 620)
    lift([17, 18], 1860, 28, 500)
    lift([510], 1900, 18, 450)
    # Cursor follows the typed text instead of sitting at the finished position.
    anim.append(keys(16, "positionX", [(0, 301, LINEAR), (1000, 301, LINEAR),
                                        (1540, 393, EASE_OUT), (1990, 568, EASE_OUT),
                                        (2440, 780, EASE_OUT), (3100, 878, EASE_OUT)]))
    anim.append(keys(16, "opacity", [(0, 0, LINEAR), (900, 100, LINEAR),
                                      (2920, 100, LINEAR), (3130, 0, LINEAR)]))
    # Four product tiles orbit out from the CDF signature, then rest long enough to read.
    for lid, start_xy in ((102, (540, 510)), (103, (540, 510)),
                          (104, (540, 510)), (105, (540, 510)),
                          (407, (540, 510)), (410, (540, 510)),
                          (408, (540, 510)), (409, (540, 510))):
        layer = lookup[lid]
        x, y = layer["transform"]["position"]
        anim.append(keys(lid, "positionX", [(0, start_xy[0], LINEAR), (900, x, EASE_OUT), (2200, x, LINEAR)]))
        anim.append(keys(lid, "positionY", [(0, start_xy[1], LINEAR), (900, y, EASE_OUT), (2200, y - 3, LINEAR)]))
    lift([106, 107, 108, 109], 850, 20, 400)
    lift([401, 110], 120, 22, 500)
    # Result page lands, then category cards rise in a stagger rather than rushing through.
    lift([203, 204], 150, 28, 510)
    lift([205, 206], 420, 50, 590)
    lift([207], 720, 30, 530)
    lift([208, 211, 403], 1220, 76, 640)
    lift([209, 212, 404], 1450, 76, 640)
    lift([210, 213, 214], 1680, 76, 640)
    lift([520], 1950, 18, 600)
    lift([521], 2200, 18, 500)
    # Product-led panels receive almost four full seconds of reading time.
    lift([301, 302, 530], 120, 30, 570)
    lift([303, 304, 305, 306, 307, 405], 520, 90, 760)
    lift([308, 309, 310, 311, 312, 406], 1220, 110, 760)
    lift([313, 314], 1900, 20, 550)
    lift([708, 701], 140, 60, 700)
    lift([702, 703], 600, 38, 650)
    anim.append(keys(708, "scaleX", [(0, 23.7, LINEAR), (800, 26, EASE_OUT), (2300, 26.3, LINEAR)]))
    anim.append(keys(708, "scaleY", [(0, 23.7, LINEAR), (800, 26, EASE_OUT), (2300, 26.3, LINEAR)]))
    for i in range(4):
        anim.append(keys(720 + i, "positionX", [(0, -660, LINEAR), (300, 540, EASE_INOUT),
                                                   (620, 1860, EASE_INOUT)]))
    animation_file = WORK / "animations.json"
    animation_file.write_text(json.dumps(anim, ensure_ascii=False), encoding="utf-8")
    run("project", "apply", "--project", str(FILM_PROJECT), "--actions", str(animation_file))
    stamps = (0, 800, 1500, 2500, 3200, 3800, 5000, 5600, 6500, 7400, 8500,
              9300, 10200, 11300, 12400, 13000, 13800, 14700)
    run("filmstrip", "--project", str(FILM_PROJECT), "--timestamps-ms", *map(str, stamps),
        "--tile-width", "270", "--tile-height", "270", "--items-per-row", "6",
        "--output", str(OUT / "previews" / "filmstrip_quadrado-1x1.png"))
    for t in (0.8, 2.5, 3.8, 6.5, 8.1, 10.2, 11.7, 14.2):
        run("preview", "--project", str(FILM_PROJECT), "--time", str(t),
            "--output", str(OUT / "previews" / f"film_{t:.1f}.png"))


def export() -> None:
    if MP4_FINAL.exists():
        backup = WORK / "backup_before_60fps_refine.mp4"
        if not backup.exists():
            shutil.copy2(MP4_FINAL, backup)
    run("export", "--project", str(FILM_PROJECT), "--output", str(MP4_SILENT),
        "--fps", "60", "--resolution", "4k")
    sound()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(MP4_SILENT), "-i", str(AUDIO),
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-vf", "scale=1080:1080:flags=lanczos+accurate_rnd,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-t", "15", "-movflags", "+faststart", str(MP4_FINAL)], check=True)
    shutil.copy2(FILM_PROJECT, STORYBOARD)
    (OUT / "versao.txt").write_text("v02\n", encoding="utf-8")
    print(MP4_FINAL)


def fix_end_logo() -> None:
    """Keep the official wordmark above the newly-added end background."""
    editable = WORK / "editable-final.json"
    run("project", "checkout", "--project", str(FILM_PROJECT), "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    layers = doc["composition"]["layers"]
    logo = next(x for x in layers if x["id"] == 708)
    doc["composition"]["layers"] = [logo] + [x for x in layers if x["id"] != 708]
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", str(FILM_PROJECT), "--file", str(editable))
    action_file = WORK / "logo_scale_fix.json"
    action_file.write_text(json.dumps([
        keys(708, axis, [(0, 23.7, LINEAR), (800, 26, EASE_OUT), (2300, 26.3, LINEAR)])
        for axis in ("scaleX", "scaleY")
    ]), encoding="utf-8")
    run("project", "apply", "--project", str(FILM_PROJECT), "--actions", str(action_file))
    for t in (13.8, 14.7):
        run("preview", "--project", str(FILM_PROJECT), "--time", str(t),
            "--output", str(OUT / "previews" / f"film_{t:.1f}.png"))


def refine_motion() -> None:
    """Natural per-character typing and continuous, subtle product movement."""
    editable = WORK / "editable-refine.json"
    run("project", "checkout", "--project", str(FILM_PROJECT), "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    old_typing = {500, 501, 502, 503}
    doc["composition"]["layers"] = [x for x in doc["composition"]["layers"]
                                    if x["id"] not in old_typing]
    font = next(x["sourceText"] for x in doc["composition"]["layers"] if x["id"] == 204)
    fonts = {"medium": (font["fontFamily"], font["fontStyle"])}
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", str(FILM_PROJECT), "--file", str(editable))
    b = Builder(1080, fonts)
    phrase = "esteiras, bicicletas, equipamentos para academia"
    t0, t1 = 1010, 2740
    for i in range(1, len(phrase) + 1):
        start = round(t0 + (i - 1) * (t1 - t0) / len(phrase))
        end = round(t0 + i * (t1 - t0) / len(phrase)) if i < len(phrase) else 3200
        b.text(800 + i, f"Busca digitada {i}", start, end - start,
               244, 557, 680, 58, phrase[:i], "medium", 27, INK)
    actions = [{**a, "insertIndex": 0} for a in b.front]
    for lid, base, dur in ((403, 20, 3600), (404, 20, 3600),
                           (405, 31, 3700), (406, 31, 3700)):
        for axis in ("scaleX", "scaleY"):
            actions.append(keys(lid, axis, [(0, base * 0.965, LINEAR),
                                            (1050, base, EASE_OUT),
                                            (dur, base * 1.025, LINEAR)]))
    action_file = WORK / "refine_motion.json"
    action_file.write_text(json.dumps(actions, ensure_ascii=False), encoding="utf-8")
    run("project", "apply", "--project", str(FILM_PROJECT), "--actions", str(action_file))
    for t in (1.4, 2.0, 2.8, 10.4, 12.0):
        run("preview", "--project", str(FILM_PROJECT), "--time", str(t),
            "--output", str(OUT / "previews" / f"refine_{t:.1f}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("preview", "fix-layer", "refine", "export"), default="preview")
    args = parser.parse_args()
    if args.stage == "preview":
        animate()
    elif args.stage == "fix-layer":
        fix_end_logo()
    elif args.stage == "refine":
        refine_motion()
    else:
        export()
