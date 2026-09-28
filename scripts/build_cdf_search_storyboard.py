"""Four approval stills for the CDF search/category motion concept.

This is a Tesseract-native storyboard project, not the final animated film.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from build_cdf_mix import Builder, tr

LAB = Path(__file__).resolve().parents[1]
OUT = LAB / "outputs" / "cdf-busca-categorias"
WORK = OUT / ".tesseract-work" / "quadrado-1x1"
PROJECT = OUT / "projeto" / "quadrado-1x1.tsrct"
BRAND = LAB / "assets" / "casa-do-fitness-brand"
PRODUCTS = LAB / "assets" / "cdf-merchant-teste" / "cutout"
TSRCT = Path(os.environ["LOCALAPPDATA"]) / "Tesseract" / "bin" / "tsrct.cmd"

BLACK = [0.035, 0.035, 0.043, 1]
INK = [0.10, 0.10, 0.12, 1]
WHITE = [1, 1, 1, 1]
OFFWHITE = [0.965, 0.967, 0.97, 1]
GREY = [0.50, 0.52, 0.55, 1]
LIGHT = [0.90, 0.91, 0.93, 1]
RED = [0.898, 0.035, 0.078, 1]
SOFTRED = [0.99, 0.92, 0.93, 1]


def run(*args: str) -> str:
    p = subprocess.run([str(TSRCT), *args], capture_output=True, text=True, encoding="utf-8")
    if p.returncode:
        raise RuntimeError(f"Tesseract {' '.join(args)} failed:\n{p.stdout}\n{p.stderr}")
    return p.stdout


def add_image(doc: dict, asset: str, lid: int, name: str, start: int, duration: int,
              x: float, y: float, anchor: tuple[float, float], scale: float) -> None:
    doc["composition"]["layers"].insert(0, {
        "type": "Image", "id": lid, "name": name,
        "activeRange": {"start": start, "duration": duration},
        "transform": tr(x, y, anchor, scale),
        "source": {"assetId": asset, "fit": "contain"},
    })


def make() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    PROJECT.parent.mkdir(parents=True, exist_ok=True)
    (OUT / "previews").mkdir(exist_ok=True)
    if PROJECT.exists():
        raise RuntimeError(f"Project already exists: {PROJECT}; preserve it before rebuilding")
    run("project", "create", "--project", str(PROJECT))
    fonts = {}
    for key, filename in (("bold", "BaiJamjuree-Bold"), ("semibold", "BaiJamjuree-SemiBold"),
                          ("medium", "BaiJamjuree-Medium")):
        r = json.loads(run("project", "import-font", "--project", str(PROJECT),
                           "--file", str(BRAND / "fonts" / f"{filename}.ttf")).strip().splitlines()[-1])
        face = r["faces"][0]
        fonts[key] = (face.get("typographicFamilyName") or r["fontFamily"],
                      face.get("typographicStyleName") or r["fontStyle"])
    assets = {
        "cdf-logo-black": BRAND / "logo" / "logo-header.png",
        "cdf-logo-white": BRAND / "logo" / "logo-header-white.png",
        "treadmill": PRODUCTS / "esteira-speedo-tr7.png",
        "bike": PRODUCTS / "bike-mormaii-motion-s.png",
        "elliptical": PRODUCTS / "eliptico-starke-sh30.png",
        "station": PRODUCTS / "estacao-speedo-multi3.png",
    }
    for asset, path in assets.items():
        run("project", "import-asset", "--project", str(PROJECT), "--file", str(path),
            "--asset-id", asset, "--kind", "image")

    b = Builder(1080, fonts)
    # Four approval frames: f40, f86, f150, f230 (30 fps storyboard timeline).
    # f40: a generic browser search, already in motion in the final film.
    b.rect(1, "S1 page", 0, 2500, 0, 0, 1080, 1080, OFFWHITE)
    b.rect(2, "S1 browser shadow", 0, 2500, 78, 190, 924, 660, LIGHT, 54)
    b.rect(3, "S1 browser", 0, 2500, 80, 184, 920, 660, WHITE, 52)
    b.rect(4, "S1 browser top", 0, 2500, 80, 184, 920, 86, OFFWHITE, 44)
    for lid, x, color in ((5, 118, RED), (6, 145, [0.83, 0.84, 0.86, 1]), (7, 172, [0.83, 0.84, 0.86, 1])):
        b.rect(lid, f"S1 browser dot {lid}", 0, 2500, x, 218, 13, 13, color, 7)
    b.rect(8, "S1 url bar", 0, 2500, 276, 207, 475, 39, WHITE, 20)
    b.text(9, "S1 url", 0, 2500, 298, 214, 430, 28, "Buscar na web", "medium", 21, GREY)
    b.text(10, "S1 eyebrow", 0, 2500, 170, 354, 740, 45, "ENCONTRE SEU PRÓXIMO TREINO", "semibold", 27, RED, "center")
    b.text(11, "S1 question", 0, 2500, 150, 404, 780, 110, "O que move você?", "bold", 62, INK, "center")
    b.rect(12, "S1 search shadow", 0, 2500, 149, 534, 782, 108, LIGHT, 54)
    b.rect(13, "S1 search", 0, 2500, 150, 528, 780, 108, WHITE, 54)
    b.text(14, "S1 search indicator", 0, 2500, 178, 562, 58, 50, ">", "bold", 38, RED)
    b.text(15, "S1 typed query", 0, 2500, 244, 555, 670, 58, "esteiras, bicicletas, equipamentos", "medium", 34, INK)
    b.rect(16, "S1 caret", 0, 2500, 837, 560, 3, 51, RED, 2)
    b.text(17, "S1 suggestion 1", 0, 2500, 193, 677, 700, 40, "esteiras para treinar em casa", "medium", 24, GREY)
    b.text(18, "S1 suggestion 2", 0, 2500, 193, 725, 700, 40, "bicicletas e equipamentos para academia", "medium", 24, GREY)
    b.rect(19, "S1 bottom accent", 0, 2500, 80, 830, 920, 14, RED, 7)

    # f86: search turns into a compact category hub, CDF mark arrives at center.
    b.rect(100, "S2 page", 2500, 1800, 0, 0, 1080, 1080, WHITE)
    b.rect(101, "S2 red disc", 2500, 1800, 388, 357, 304, 304, RED, 152)
    b.rect(102, "S2 top tile", 2500, 1800, 458, 104, 164, 164, SOFTRED, 35)
    b.rect(103, "S2 left tile", 2500, 1800, 136, 428, 164, 164, OFFWHITE, 35)
    b.rect(104, "S2 right tile", 2500, 1800, 780, 428, 164, 164, OFFWHITE, 35)
    b.rect(105, "S2 bottom tile", 2500, 1800, 458, 752, 164, 164, SOFTRED, 35)
    b.text(106, "S2 top label", 2500, 1800, 440, 290, 200, 45, "ESTEIRAS", "bold", 27, RED, "center")
    b.text(107, "S2 left label", 2500, 1800, 105, 614, 220, 45, "ELÍPTICOS", "semibold", 24, GREY, "center")
    b.text(108, "S2 right label", 2500, 1800, 755, 614, 220, 45, "BICICLETAS", "bold", 25, RED, "center")
    b.text(109, "S2 bottom label", 2500, 1800, 440, 930, 200, 45, "MUITO MAIS", "semibold", 25, RED, "center")
    b.text(110, "S2 motion marker", 2500, 1800, 340, 1000, 400, 34, "CASA DO FITNESS", "semibold", 27, INK, "center")

    # f150: a reimagined CDF category search page, not a literal site screenshot.
    b.rect(200, "S3 page", 4300, 2200, 0, 0, 1080, 1080, OFFWHITE)
    b.rect(201, "S3 nav", 4300, 2200, 0, 0, 1080, 174, BLACK)
    b.rect(202, "S3 nav accent", 4300, 2200, 0, 168, 1080, 6, RED)
    b.rect(203, "S3 search", 4300, 2200, 75, 215, 930, 94, WHITE, 46)
    b.text(204, "S3 query", 4300, 2200, 123, 234, 840, 60, "esteiras, bicicletas, equipamentos para academia", "medium", 28, INK)
    b.text(205, "S3 eyebrow", 4300, 2200, 75, 363, 740, 40, "ENCONTRE O QUE MOVE VOCÊ", "semibold", 25, RED)
    b.text(206, "S3 title", 4300, 2200, 75, 415, 890, 150, "Seu treino começa aqui.", "bold", 65, INK)
    b.text(207, "S3 body", 4300, 2200, 77, 552, 905, 102,
           "Da primeira corrida à academia completa: encontre o equipamento certo para o seu momento.",
           "medium", 30, GREY)
    b.rect(208, "S3 card treadmill", 4300, 2200, 75, 708, 288, 260, WHITE, 38)
    b.rect(209, "S3 card bike", 4300, 2200, 396, 708, 288, 260, WHITE, 38)
    b.rect(210, "S3 card more", 4300, 2200, 717, 708, 288, 260, BLACK, 38)
    b.text(211, "S3 treadmill label", 4300, 2200, 99, 732, 240, 45, "Esteiras", "bold", 33, INK)
    b.text(212, "S3 bike label", 4300, 2200, 420, 732, 240, 45, "Bicicletas", "bold", 33, INK)
    b.text(213, "S3 more label", 4300, 2200, 745, 785, 235, 95, "E muito\nmais.", "bold", 42, WHITE)
    b.rect(214, "S3 more accent", 4300, 2200, 745, 907, 112, 7, RED, 4)

    # f230: two product-led cards in motion, no price or stock claims.
    b.rect(300, "S4 page", 6500, 4000, 0, 0, 1080, 1080, OFFWHITE)
    b.text(301, "S4 eyebrow", 6500, 4000, 76, 75, 850, 42, "CATEGORIAS PARA SE MOVER", "semibold", 26, RED)
    b.text(302, "S4 title", 6500, 4000, 76, 123, 930, 92, "Escolha o seu ritmo.", "bold", 64, INK)
    b.rect(303, "S4 tread card", 6500, 4000, 73, 271, 934, 319, WHITE, 43)
    b.rect(304, "S4 tread accent", 6500, 4000, 73, 271, 12, 319, RED, 6)
    b.text(305, "S4 tread overline", 6500, 4000, 120, 327, 475, 37, "PARA IR MAIS LONGE", "semibold", 24, RED)
    b.text(306, "S4 tread title", 6500, 4000, 119, 365, 480, 90, "Esteiras", "bold", 55, INK)
    b.text(307, "S4 tread descriptor", 6500, 4000, 121, 447, 460, 96, "Treine no seu tempo.\nConheça a categoria.", "medium", 28, GREY)
    b.rect(308, "S4 bike card", 6500, 4000, 73, 626, 934, 319, BLACK, 43)
    b.rect(309, "S4 bike accent", 6500, 4000, 73, 626, 12, 319, RED, 6)
    b.text(310, "S4 bike overline", 6500, 4000, 120, 682, 475, 37, "PARA CADA VOLTA", "semibold", 24, [1, 0.47, 0.49, 1])
    b.text(311, "S4 bike title", 6500, 4000, 119, 720, 480, 90, "Bicicletas", "bold", 55, WHITE)
    b.text(312, "S4 bike descriptor", 6500, 4000, 121, 802, 460, 96, "Encontre sua próxima pedalada.\nE muito mais na CDF.", "medium", 28, [0.72, 0.73, 0.76, 1])
    b.rect(313, "S4 footer line", 6500, 4000, 73, 997, 934, 2, LIGHT)
    b.text(314, "S4 footer", 6500, 4000, 74, 1012, 860, 40, "casadofitness.com.br", "medium", 26, GREY)

    edits = WORK / "edits.json"
    edits.write_text(json.dumps([{**a, "insertIndex": 0} for a in b.front], ensure_ascii=False), encoding="utf-8")
    run("project", "apply", "--project", str(PROJECT), "--actions", str(edits))
    editable = WORK / "editable.json"
    run("project", "checkout", "--project", str(PROJECT), "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    doc["dimensions"] = {"width": 1080, "height": 1080}
    doc["duration"] = 15.0
    add_image(doc, "cdf-logo-white", 401, "S2 logo", 2500, 1800, 540, 508, (1200, 164), 11)
    add_image(doc, "treadmill", 407, "S2 Esteiras", 2500, 1800, 540, 184, (440, 440), 11)
    add_image(doc, "elliptical", 410, "S2 Elípticos", 2500, 1800, 218, 508, (440, 440), 11)
    add_image(doc, "bike", 408, "S2 Bicicletas", 2500, 1800, 862, 508, (467, 433), 12)
    add_image(doc, "station", 409, "S2 Muito mais", 2500, 1800, 540, 834, (500, 500), 10)
    add_image(doc, "cdf-logo-white", 402, "S3 logo", 4300, 2200, 540, 86, (1200, 164), 20)
    add_image(doc, "treadmill", 403, "S3 Esteira Speedo TR7", 4300, 2200, 220, 855, (440, 440), 20)
    add_image(doc, "bike", 404, "S3 Bike Mormaii Motion-S", 4300, 2200, 540, 855, (467, 433), 20)
    add_image(doc, "treadmill", 405, "S4 Esteira Speedo TR7", 6500, 4000, 816, 428, (440, 440), 31)
    add_image(doc, "bike", 406, "S4 Bike Mormaii Motion-S", 6500, 4000, 816, 785, (467, 433), 31)
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", str(PROJECT), "--file", str(editable))
    for frame in (40, 86, 150, 230):
        run("preview", "--project", str(PROJECT), "--time", f"{frame/30:.6f}",
            "--output", str(OUT / "previews" / f"f{frame:03}.png"))
    print(PROJECT)


if __name__ == "__main__":
    make()
