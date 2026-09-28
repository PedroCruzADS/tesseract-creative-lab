"""Slow CDF search film: browser entrance and three-second product orbit."""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess

from animate_cdf_search import sound
from build_cdf_mix import Builder, EASE_OUT, LINEAR, keys
from build_cdf_search_storyboard import GREY, INK, LIGHT, OFFWHITE, OUT, RED, WHITE, run

ROOT_PROJECT = OUT / "projeto" / "quadrado-1x1.tsrct"
OLD = OUT / "cdf-busca-categorias_quadrado-1x1_v02.mp4"
FINAL = OUT / "cdf-busca-categorias_quadrado-1x1_v03.mp4"
WORK = OUT / ".tesseract-work" / "v03"
PROJECT = WORK / "quadrado-1x1-v03.tsrct"
EDIT = WORK / "editable.json"
TOTAL = 18000


def archive() -> None:
    v02 = OUT / "versoes" / "v02"
    (v02 / "projeto").mkdir(parents=True, exist_ok=True)
    (v02 / "previews").mkdir(parents=True, exist_ok=True)
    for src, dst in (
        (ROOT_PROJECT, v02 / "projeto" / ROOT_PROJECT.name),
        (OLD, v02 / OLD.name),
        (OUT / "previews" / "filmstrip_quadrado-1x1.png", v02 / "previews" / "filmstrip_quadrado-1x1.png"),
        (OUT / "brief.md", v02 / "brief.md"),
        (OUT / "notes.md", v02 / "notes.md"),
    ):
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)


def build() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    archive()
    if PROJECT.exists():
        raise RuntimeError("v03 work project exists; inspect it before rebuilding")
    shutil.copy2(ROOT_PROJECT, PROJECT)
    run("project", "checkout", "--project", str(PROJECT), "--output", str(EDIT))
    doc = json.loads(EDIT.read_text(encoding="utf-8"))
    doc["duration"] = 18.0
    typed_ids = set(range(801, 849))
    doc["composition"]["layers"] = [v for v in doc["composition"]["layers"] if v["id"] not in typed_ids]
    s1 = set(range(1, 20)) | {510}
    s2 = set(range(100, 111)) | {401, 407, 408, 409, 410}
    s3 = set(range(200, 215)) | {402, 403, 404, 520, 521}
    s4 = set(range(300, 315)) | {405, 406, 530}
    end = {700, 701, 702, 703, 708}
    cuts = {720: 4500, 721: 8600, 722: 12200, 723: 15900}
    for layer in doc["composition"]["layers"]:
        lid, active = layer["id"], layer["activeRange"]
        if lid in s1:
            active["start"] += 1300
        elif lid in s2:
            active.update(start=4500, duration=4100)
        elif lid in s3 or lid in s4:
            active["start"] += 3200
        elif lid in end:
            active.update(start=15900, duration=2100)
        elif lid in cuts:
            active["start"] = cuts[lid] - 310
        if lid == 204:
            layer["sourceText"]["text"] = "equipamentos fitness para casa"
        elif lid == 17:
            layer["sourceText"]["text"] = "esteiras para casa"
        elif lid == 18:
            layer["sourceText"]["text"] = "bicicletas e equipamentos fitness"
    EDIT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", str(PROJECT), "--file", str(EDIT))
    src_font = next(v["sourceText"] for v in doc["composition"]["layers"] if v["id"] == 204)
    bold_font = next(v["sourceText"] for v in doc["composition"]["layers"] if v["id"] == 302)
    fonts = {"medium": (src_font["fontFamily"], src_font["fontStyle"]),
             "bold": (bold_font["fontFamily"], bold_font["fontStyle"])}
    b = Builder(1080, fonts)
    # Browser enters, settles into exactly the same browser geometry used by S1.
    b.rect(900, "Abertura fundo", 0, 1300, 0, 0, 1080, 1080, OFFWHITE)
    b.rect(901, "Abertura sombra", 0, 1300, 78, 190, 924, 660, LIGHT, 54)
    b.rect(902, "Abertura navegador", 0, 1300, 80, 184, 920, 660, WHITE, 52)
    b.rect(903, "Abertura barra", 0, 1300, 80, 184, 920, 86, OFFWHITE, 44)
    for lid, x, color in ((904, 118, RED), (905, 145, [0.83, 0.84, 0.86, 1]),
                          (906, 172, [0.83, 0.84, 0.86, 1])):
        b.rect(lid, f"Abertura ponto {lid}", 0, 1300, x, 218, 13, 13, color, 7)
    b.rect(907, "Abertura URL", 0, 1300, 276, 207, 475, 39, WHITE, 20)
    b.text(908, "Abertura URL texto", 0, 1300, 298, 214, 430, 28,
           "Buscar na web", "medium", 21, GREY)
    b.text(909, "Abertura headline", 0, 1300, 145, 470, 790, 70,
           "Abra possibilidades.", "bold", 46, INK, "center")
    b.text(910, "Abertura apoio", 0, 1300, 170, 544, 740, 45,
           "Seu próximo treino começa com uma busca.", "medium", 26, GREY, "center")
    phrase = "equipamentos fitness para casa"
    for i in range(1, len(phrase) + 1):
        start = round(2250 + (i - 1) * 1780 / len(phrase))
        stop = round(2250 + i * 1780 / len(phrase)) if i < len(phrase) else 4500
        b.text(930 + i, f"Busca v03 {i}", start, stop - start,
               244, 557, 680, 58, phrase[:i], "medium", 30, INK)
    layer_file = WORK / "new_layers.json"
    layer_file.write_text(json.dumps([{**a, "insertIndex": 0} for a in b.front], ensure_ascii=False), encoding="utf-8")
    run("project", "apply", "--project", str(PROJECT), "--actions", str(layer_file))
    run("project", "checkout", "--project", str(PROJECT), "--output", str(EDIT))
    layer_map = {v["id"]: v for v in json.loads(EDIT.read_text(encoding="utf-8"))["composition"]["layers"]}
    anim = []
    for lid in range(901, 909):
        y = layer_map[lid]["transform"]["position"][1]
        anim += [keys(lid, "positionY", [(0, y + 230, LINEAR), (900, y + 6, EASE_OUT), (1300, y, LINEAR)]),
                 keys(lid, "opacity", [(0, 0, LINEAR), (240, 100, EASE_OUT), (1300, 100, LINEAR)])]
    for lid, delay in ((909, 520), (910, 790)):
        y = layer_map[lid]["transform"]["position"][1]
        anim += [keys(lid, "positionY", [(0, y + 55, LINEAR), (delay, y + 55, LINEAR), (delay + 330, y, EASE_OUT)]),
                 keys(lid, "opacity", [(0, 0, LINEAR), (delay, 0, LINEAR),
                                        (delay + 260, 100, EASE_OUT), (1160, 100, LINEAR), (1300, 0, LINEAR)])]
    anim.append(keys(16, "positionX", [(0, 301, LINEAR), (950, 301, LINEAR),
                                        (1560, 455, EASE_OUT), (2140, 600, EASE_OUT),
                                        (2730, 750, EASE_OUT), (3200, 760, LINEAR)]))
    # One item per category, orbiting as a coherent card/product/label group.
    groups = ((-90, (102, 407, 106)), (0, (104, 408, 108)),
              (90, (105, 409, 109)), (180, (103, 410, 107)))
    centers = {102: (540, 186), 104: (862, 510), 105: (540, 834), 103: (218, 510)}
    for angle0, lids in groups:
        tcx, tcy = centers[lids[0]]
        for lid in lids:
            x0, y0 = layer_map[lid]["transform"]["position"]
            dx, dy = x0 - tcx, y0 - tcy
            xs = [(0, 540 + dx, LINEAR), (900, x0, EASE_OUT)]
            ys = [(0, 510 + dy, LINEAR), (900, y0, EASE_OUT)]
            for step in range(1, 31):
                t = 900 + step * 100
                a = math.radians(angle0 + 90 * step / 30)
                xs.append((t, 540 + 322 * math.cos(a) + dx, LINEAR))
                ys.append((t, 510 + 324 * math.sin(a) + dy, LINEAR))
            xs.append((4100, xs[-1][1], LINEAR))
            ys.append((4100, ys[-1][1], LINEAR))
            anim += [keys(lid, "positionX", xs), keys(lid, "positionY", ys)]
    anim_file = WORK / "animations.json"
    anim_file.write_text(json.dumps(anim, ensure_ascii=False), encoding="utf-8")
    run("project", "apply", "--project", str(PROJECT), "--actions", str(anim_file))
    stamps = (0, 500, 1100, 1500, 2300, 3300, 4300, 4700, 5400, 6200, 7000,
              7800, 8500, 9200, 10500, 11800, 12900, 14000, 15300, 16400, 17400)
    run("filmstrip", "--project", str(PROJECT), "--timestamps-ms", *map(str, stamps),
        "--tile-width", "270", "--tile-height", "270", "--items-per-row", "6",
        "--output", str(OUT / "previews" / "filmstrip_quadrado-1x1_v03.png"))
    for t in (0.5, 1.2, 2.9, 4.8, 6.0, 7.4, 8.2, 10.6, 14.2, 17.3):
        run("preview", "--project", str(PROJECT), "--time", str(t),
            "--output", str(OUT / "previews" / f"v03_{t:.1f}.png"))


def export() -> None:
    silent = WORK / "silent_2160p60.mp4"
    run("export", "--project", str(PROJECT), "--output", str(silent), "--fps", "60", "--resolution", "4k")
    score = WORK / "trilha-original-v03.wav"
    sound(duration=18, typing=(2.25, 4.03), transitions=(4.5, 8.6, 12.2, 15.9), output=score)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(score),
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-vf", "scale=1080:1080:flags=lanczos+accurate_rnd,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-t", "18",
                    "-movflags", "+faststart", str(FINAL)], check=True)
    if not FINAL.exists() or FINAL.stat().st_size < 100_000:
        raise RuntimeError("v03 MP4 missing or unexpectedly small")
    archived = OUT / "versoes" / "v02" / OLD.name
    if OLD.exists():
        if not archived.exists() or archived.stat().st_size != OLD.stat().st_size:
            raise RuntimeError("v02 archive not verified; v02 MP4 retained")
        OLD.unlink()
    shutil.copy2(PROJECT, ROOT_PROJECT)
    shutil.copy2(OUT / "previews" / "filmstrip_quadrado-1x1_v03.png",
                 OUT / "previews" / "filmstrip_quadrado-1x1.png")
    (OUT / "versao.txt").write_text("v03\n", encoding="utf-8")
    print(FINAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("preview", "export"), default="preview")
    args = parser.parse_args()
    build() if args.stage == "preview" else export()
