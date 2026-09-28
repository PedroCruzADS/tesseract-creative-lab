"""Authorial CDF Mês do Cliente product mix, feed 4:5, Tesseract 0.2.0.

Run without flags to build the editable project, preview and filmstrip.
Inspect the filmstrip, then run --export-existing for MP4 and GIF.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from build_cdf_mix import (
    BRAND, PRODUCTS, SNAPSHOT, Builder, EASE_OUT, LINEAR, brl, keys, run, tr,
)

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB / "outputs" / "cdf-mix-produtos-codex"
SLUG = "cdf-mix-produtos-codex"
W, H = 1080, 1350
HOOK_MS, SCENE_MS, END_MS = 1300, 1900, 1400
END_START = HOOK_MS + 4 * SCENE_MS
TOTAL_MS = END_START + END_MS
INK = [0.065, 0.065, 0.07, 1]
CHARCOAL = [0.13, 0.13, 0.14, 1]
PAPER = [0.955, 0.952, 0.945, 1]
WHITE = [1, 1, 1, 1]
RED = [0.902, 0.039, 0.078, 1]
YELLOW = [0.95, 0.82, 0.20, 1]
MUTED = [0.67, 0.67, 0.68, 1]
PRODUCTS_SPEC = [
    ("19", "esteira-speedo-tr7", "ESTEIRA", "Speedo TR7", 1000),
    ("27", "bike-mormaii-motion-s", "BIKE SPINNING", "Mormaii Motion-S", 1000),
    ("33", "eliptico-starke-sh30", "ELÍPTICO", "Starke SH30", 1000),
    ("67", "estacao-speedo-multi3", "ESTAÇÃO", "Speedo Multi 3", 960),
]


def fade_in_out(layer: int, duration: int, delay: int = 0) -> dict:
    return keys(layer, "opacity", [
        (0, 0, LINEAR), (delay, 0, LINEAR), (delay + 230, 100, EASE_OUT),
        (duration - 180, 100, LINEAR), (duration, 0, LINEAR),
    ])


def build_layers(b: Builder, offer: dict) -> None:
    products = {p["sku"]: p for p in offer["produtos"]}

    # Full-frame surfaces. Back layers are appended behind imported images.
    b.rect(900, "Paper", 0, TOTAL_MS, 0, 0, W, H, PAPER, front=False)
    b.rect(901, "Header dark", 0, TOTAL_MS, 0, 0, W, 152, INK, front=False)
    b.rect(902, "Brand rail", 0, TOTAL_MS, 0, 152, 13, H - 152, RED, front=False)
    b.rect(903, "Header rule", 0, TOTAL_MS, 0, 148, W, 4, RED, front=False)

    # Opening: products are visible from the first frame, in a four-tile grid.
    b.text(10, "Opening kicker", 0, HOOK_MS, 64, 194, 760, 45,
           "MÊS DO CLIENTE  /  CASA DO FITNESS", "bold", 29, RED, tracking=38)
    b.text(11, "Opening headline", 0, HOOK_MS, 64, 256, 960, 290,
           "SEU ESPAÇO.\nSEU TREINO.", "bold", 112, INK)
    b.rect(12, "Opening underline", 0, HOOK_MS, 64, 560, 426, 12, RED, 6)
    b.text(13, "Opening support", 0, HOOK_MS, 64, 600, 930, 85,
           "4 equipamentos para montar sua academia em casa", "semibold", 39, CHARCOAL)
    for i, _ in enumerate(PRODUCTS_SPEC):
        x = 52 + i * 258
        b.rect(20 + i, f"Opening tile {i+1}", 0, HOOK_MS, x, 790, 242, 350,
               WHITE, 24, front=False)
        b.rect(30 + i, f"Opening index {i+1}", 0, HOOK_MS, x, 1149, 242, 54,
               RED if i == 0 else INK, 0)
        b.text(34 + i, f"Opening index text {i+1}", 0, HOOK_MS, x, 1156, 242, 42,
               f"0{i+1} / 04", "bold", 27, WHITE, "center")
        b.anim.append(keys(40 + i, "positionY", [(0, 990, LINEAR), (210 + 90*i, 965, EASE_OUT)]))
    b.anim.append(keys(11, "opacity", [(0, 100, LINEAR),
                                      (HOOK_MS - 180, 100, LINEAR), (HOOK_MS, 0, LINEAR)]))

    # Product scenes use one large image area and a dedicated commercial strip.
    for i, (sku, _, category, model, _) in enumerate(PRODUCTS_SPEC):
        p = products[sku]
        start = HOOK_MS + i * SCENE_MS
        n = 100 + i * 20
        b.rect(n, f"Photo surface {i+1}", start, SCENE_MS, 52, 268, 976, 610,
               WHITE, 28, front=False)
        b.rect(n+1, f"Offer surface {i+1}", start, SCENE_MS, 0, 1000, 1080, 350,
               INK, front=False)
        b.rect(n+2, f"Category pill {i+1}", start, SCENE_MS, 64, 190, 320, 57,
               RED, 27)
        b.text(n+3, f"Category {i+1}", start, SCENE_MS, 64, 201, 320, 44,
               category, "bold", 31, WHITE, "center", tracking=25)
        b.text(n+4, f"Counter {i+1}", start, SCENE_MS, 788, 185, 228, 62,
               f"0{i+1} / 04", "bold", 42, RED, "right")
        b.text(n+5, f"Product name {i+1}", start, SCENE_MS, 64, 910, 945, 75,
               model, "bold", 59, INK)
        b.text(n+6, f"Payment label {i+1}", start, SCENE_MS, 64, 1032, 500, 53,
               "18x sem juros de", "semibold", 37, WHITE)
        b.text(n+7, f"Payment amount {i+1}", start, SCENE_MS, 58, 1079, 960, 122,
               brl(p["parc18"]), "bold", 101, WHITE)
        if p["de"]:
            b.text(n+8, f"Price was {i+1}", start, SCENE_MS, 620, 1033, 390, 44,
                   f"de {brl(p['de'])}", "medium", 31, MUTED, "right", strike=True)
        b.rect(n+9, f"PIX bar {i+1}", start, SCENE_MS, 63, 1210, 780, 66,
               RED, 30)
        b.text(n+10, f"PIX value {i+1}", start, SCENE_MS, 75, 1221, 755, 48,
               f"NO PIX  {brl(p['pix'])}", "bold", 35, WHITE)
        b.text(n+11, f"Offer date {i+1}", start, SCENE_MS, 64, 1300, 900, 31,
               "Preços válidos em 23/09/2026.", "medium", 24, MUTED)
        if p["pix"] >= 10000:
            b.rect(n+12, f"Shipping badge {i+1}", start, SCENE_MS, 84, 294,
                   315, 58, YELLOW, 29)
            b.text(n+13, f"Shipping badge text {i+1}", start, SCENE_MS,
                   94, 302, 295, 44, "FRETE GRÁTIS*", "bold", 27, INK, "center")
            b.text(n+14, f"Shipping rule {i+1}", start, SCENE_MS, 64, 1278, 950, 31,
                   "*Em pedidos acima de R$ 10 mil.", "medium", 23, MUTED)
        for lid, delay in ((n+3, 60), (n+4, 100), (n+5, 180), (n+6, 270),
                           (n+7, 330), (n+9, 400), (n+10, 420)):
            b.anim.append(fade_in_out(lid, SCENE_MS, delay))
        b.anim.append(keys(60 + i, "positionX", [(0, 670, LINEAR), (360, 540, EASE_OUT),
                                                 (SCENE_MS - 240, 530, LINEAR),
                                                 (SCENE_MS, 440, EASE_OUT)]))
        b.anim.append(keys(60 + i, "opacity", [(0, 0, LINEAR), (80, 0, LINEAR),
                                               (300, 100, EASE_OUT),
                                               (SCENE_MS - 190, 100, LINEAR),
                                               (SCENE_MS, 0, LINEAR)]))
        # Segmented progress marker, tied to the current product.
        for j in range(4):
            b.rect(300 + i*4 + j, f"Progress {i+1}.{j+1}", start, SCENE_MS,
                   64 + 249*j, 165, 231, 8, RED if j <= i else [0.74, 0.74, 0.75, 1], 4)

    # Closing card: single short decision, no additional product claims.
    b.rect(800, "End dark", END_START, END_MS, 0, 152, W, H - 152, INK, front=False)
    b.rect(801, "End red block", END_START, END_MS, 0, 1050, W, 300, RED, front=False)
    b.text(810, "End kicker", END_START, END_MS, 66, 290, 850, 56,
           "MÊS DO CLIENTE", "bold", 39, YELLOW, tracking=70)
    b.text(811, "End headline", END_START, END_MS, 60, 386, 970, 310,
           "O PRÓXIMO TREINO\nCOMEÇA AQUI.", "bold", 101, WHITE)
    b.text(812, "End benefit", END_START, END_MS, 65, 740, 950, 69,
           "Até 18x sem juros  •  5% OFF no PIX", "semibold", 39, WHITE)
    b.text(813, "End shipping", END_START, END_MS, 65, 810, 950, 58,
           "Frete grátis em pedidos acima de R$ 10 mil*", "medium", 29, MUTED)
    b.rect(814, "End CTA", END_START, END_MS, 65, 936, 950, 116, RED, 57)
    b.text(815, "End CTA text", END_START, END_MS, 65, 963, 950, 65,
           "ESCOLHA SEU EQUIPAMENTO", "bold", 48, WHITE, "center", tracking=24)
    b.text(816, "End URL", END_START, END_MS, 65, 1154, 950, 65,
           "casadofitness.com.br", "bold", 44, WHITE, "center")
    b.text(817, "End legal", END_START, END_MS, 64, 1300, 950, 31,
           "*Condições e preços consultados em 23/09/2026.", "medium", 23, WHITE)
    for lid, delay in ((810, 20), (811, 100), (812, 210), (813, 280),
                       (814, 380), (815, 420), (816, 490)):
        b.anim.append(keys(lid, "opacity", [(0, 0, LINEAR), (delay, 0, LINEAR),
                                            (delay + 260, 100, EASE_OUT)]))


def image_layers() -> list[dict]:
    layers = [{"type": "Image", "id": 70, "name": "Official CDF logo",
               "activeRange": {"start": 0, "duration": TOTAL_MS},
               "transform": tr(540, 75, (1200, 164), 20),
               "source": {"assetId": "logo-white", "fit": "contain"}}]
    for i, (_, asset, _, _, px) in enumerate(PRODUCTS_SPEC):
        x = 52 + i*258 + 121
        layers.append({"type": "Image", "id": 40+i, "name": f"Opening {asset}",
                       "activeRange": {"start": 0, "duration": HOOK_MS},
                       "transform": tr(x, 965, (px/2, px/2), 25),
                       "source": {"assetId": asset, "fit": "contain"}})
        layers.append({"type": "Image", "id": 60+i, "name": f"Showcase {asset}",
                       "activeRange": {"start": HOOK_MS+i*SCENE_MS, "duration": SCENE_MS},
                       "transform": tr(540, 573, (px/2, px/2), 61),
                       "source": {"assetId": asset, "fit": "contain"}})
    return layers


def create_project() -> Path:
    project = ROOT / "projeto" / "feed-4x5.tsrct"
    work = ROOT / ".tesseract-work" / "feed-4x5"
    work.mkdir(parents=True, exist_ok=True)
    project.unlink(missing_ok=True)
    run("project", "create", "--project", str(project))
    fonts = {}
    for key, name in (("bold", "BaiJamjuree-Bold"),
                      ("semibold", "BaiJamjuree-SemiBold"),
                      ("medium", "BaiJamjuree-Medium")):
        result = json.loads(run("project", "import-font", "--project", str(project),
                                "--file", str(BRAND / "fonts" / f"{name}.ttf")).strip().splitlines()[-1])
        face = result["faces"][0]
        fonts[key] = (face.get("typographicFamilyName") or result["fontFamily"],
                      face.get("typographicStyleName") or result["fontStyle"])
    for asset, source in [("logo-white", BRAND / "logo" / "logo-header-white.png")] + [
        (asset, PRODUCTS / f"{asset}.png") for _, asset, _, _, _ in PRODUCTS_SPEC
    ]:
        run("project", "import-asset", "--project", str(project),
            "--file", str(source), "--asset-id", asset, "--kind", "image")
    builder = Builder(H, fonts)
    offer = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    build_layers(builder, offer)
    # Tesseract append order for back layers is front-to-back; the full paper
    # surface must be the final layer or it hides every local dark panel.
    back_order = {801: 0, 800: 1, 903: 2, 901: 3, 902: 4, 900: 5}
    builder.back.sort(key=lambda action: back_order.get(action["layerId"], 0))
    checkout = work / "editable.json"
    run("project", "checkout", "--project", str(project), "--output", str(checkout))
    doc = json.loads(checkout.read_text(encoding="utf-8"))
    doc["dimensions"] = {"width": W, "height": H}
    doc["duration"] = TOTAL_MS / 1000
    doc["composition"]["layers"] = image_layers()
    all_ids = [x["id"] for x in doc["composition"]["layers"]] + [
        x["layerId"] for x in builder.back + builder.front
    ]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate layer ID")
    checkout.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", str(project), "--file", str(checkout))
    actions = builder.back + [{**a, "insertIndex": 0} for a in builder.front] + builder.anim
    edits = work / "edits.json"
    edits.write_text(json.dumps(actions, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "apply", "--project", str(project), "--actions", str(edits))
    return project


def preview(project: Path) -> None:
    run("preview", "--project", str(project), "--time", "2.3",
        "--output", str(ROOT / "previews" / "preview_feed-4x5.png"))
    run("filmstrip", "--project", str(project),
        "--timestamps-ms", "0", "500", "1100", "1600", "2300", "3400", "4300",
        "5400", "6200", "7300", "8100", "9000", "9600", "10300",
        "--tile-width", "324", "--tile-height", "405", "--items-per-row", "5",
        "--output", str(ROOT / "previews" / "filmstrip_feed-4x5.png"))


def export(project: Path) -> None:
    mp4 = ROOT / f"{SLUG}_feed-4x5_v01.mp4"
    run("export", "--project", str(project), "--output", str(mp4))
    vf = ("fps=15,scale=720:-1:flags=lanczos,split[a][b];"
          "[a]palettegen=max_colors=256:stats_mode=diff[p];"
          "[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4),
                    "-vf", vf, "-loop", "0", str(mp4.with_suffix(".gif"))], check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export-existing", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    project = ROOT / "projeto" / "feed-4x5.tsrct"
    if args.export_existing:
        if not project.exists():
            raise SystemExit("Project missing; build previews first")
        export(project)
        return
    if args.rebuild:
        if not (ROOT / "versao.txt").exists():
            raise SystemExit("Expected Codex output folder is missing")
        shutil.copy(__file__, ROOT / "build_snapshot.py")
        project = create_project()
        preview(project)
        print(project)
        print(ROOT / "previews" / "filmstrip_feed-4x5.png")
        return
    if ROOT.exists():
        raise SystemExit(f"Output already exists; refusing to overwrite: {ROOT}")
    (ROOT / "projeto").mkdir(parents=True)
    (ROOT / "previews").mkdir()
    shutil.copy(SNAPSHOT, ROOT / "offer.json")
    (ROOT / "versao.txt").write_text("v01\n", encoding="utf-8")
    (ROOT / "brief.md").write_text(
        "# CDF Mês do Cliente — versão Codex\n\n"
        "Feed 4:5, 10,3 s. Abertura mostra os quatro equipamentos; cada cena apresenta "
        "um produto real, parcela e valor PIX; fechamento com CTA. Fonte comercial: offer.json.\n",
        encoding="utf-8")
    (ROOT / "notes.md").write_text(
        "# Versão Codex v01\n\n"
        "Hipótese: mostrar os quatro equipamentos desde o primeiro segundo e usar cartões "
        "de oferta mais claros aumenta entendimento e leitura em mobile.\n\n"
        "Original v03 preservado em outputs/cdf-mix-produtos/. Produtos, logo e Bai Jamjuree "
        "são assets oficiais locais; preço e condições vêm do snapshot de 23/09/2026. "
        "Sem áudio.\n",
        encoding="utf-8")
    shutil.copy(__file__, ROOT / "build_snapshot.py")
    project = create_project()
    preview(project)
    print(project)
    print(ROOT / "previews" / "filmstrip_feed-4x5.png")


if __name__ == "__main__":
    main()
