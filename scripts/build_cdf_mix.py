"""Criativo CDF 'Mes do Cliente' - mix de 4 produtos (feed 4:5 e stories 9:16) no Tesseract.

Uso:
  python scripts/build_cdf_mix.py                 regrava a versão atual (somente MP4)
  python scripts/build_cdf_mix.py --nova-versao   arquiva a atual em versoes/ e cria a próxima
  python scripts/build_cdf_mix.py --formato feed  gera só um formato (feed|stories)
  python scripts/build_cdf_mix.py --gif           também gera GIF quando solicitado
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lab_versions import prepare  # noqa: E402

LAB = Path(__file__).resolve().parents[1]
TSRCT = os.path.join(os.environ["LOCALAPPDATA"], "Tesseract", "bin", "tsrct.cmd")
SNAPSHOT = LAB / "data" / "cdf-mix-produtos" / "offer_20260923.json"
BRAND = LAB / "assets" / "casa-do-fitness-brand"
PRODUCTS = LAB / "assets" / "cdf-merchant-teste" / "product"

SLUG = "cdf-mix-produtos"
ROOT = LAB / "outputs" / SLUG
FORMATS = {"feed": (1350, "feed-4x5"), "stories": (1920, "stories-9x16")}
W = 1080
CONTENT_H = 1350  # referência do feed; stories usa coordenadas próprias
STORY_SAFE_TOP = 250
STORY_SAFE_BOTTOM = 250

# timeline (ms)
HOOK_END = 1500
SLIDE_MS = 1800
PRODUCTS_END = HOOK_END + 4 * SLIDE_MS  # 8700
TOTAL_MS = 10000
FIRST_OFFSET = 320  # 1o produto espera o card branco chegar

# paleta (site casadofitness.com.br)
BLACK = [0.043, 0.043, 0.047, 1]
GRAPHITE = [0.13, 0.13, 0.14, 1]
WHITE = [1, 1, 1, 1]
GREY = [0.66, 0.66, 0.68, 1]
RED = [0.902, 0.039, 0.078, 1]
ORANGE = [1.0, 0.42, 0.0, 1]
YELLOW = [1.0, 0.77, 0.0, 1]

SLIDES = [  # (sku, asset, px, nome na peca)
    ("19", "esteira-speedo-tr7", 1000, "Esteira Speedo TR7"),
    ("27", "bike-mormaii-motion-s", 1000, "Bike Spinning Mormaii Motion-S"),
    ("33", "eliptico-starke-sh30", 1000, "Elíptico Starke SH30"),
    ("67", "estacao-speedo-multi3", 960, "Estação Speedo Multi 3"),
]
FREE_SHIPPING_MIN = 10000.0


def brl(v: float) -> str:
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def run(*args: str) -> str:
    out = subprocess.run([TSRCT, *args], capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit(f"tsrct {' '.join(args)} falhou:\n{out.stdout}\n{out.stderr}")
    return out.stdout


def tr(x: float, y: float, anchor=(0, 0), scale: float = 100, opacity: float = 100) -> dict:
    return {"anchorPoint": list(anchor), "position": [x, y], "scale": [scale, scale],
            "rotation": 0, "opacity": opacity}


EASE_OUT = {"type": "cubicBezier", "x1": 0.16, "y1": 1, "x2": 0.3, "y2": 1}
EASE_INOUT = {"type": "cubicBezier", "x1": 0.65, "y1": 0, "x2": 0.35, "y2": 1}
LINEAR = {"type": "linear"}


def keys(layer_id: int, prop: str, pts: list[tuple[int, float, dict]]) -> dict:
    return {"type": "setFxPropertyKeyframes", "compositionId": "main",
            "property": {"layerId": layer_id, "propertyType": prop},
            "keyframes": [{"id": f"L{layer_id}-{prop}-{i}", "layerTime": t,
                           "value": {"type": "float", "value": v}, "easing": e}
                          for i, (t, v, e) in enumerate(pts)]}


class Builder:
    def __init__(self, height: int, fonts: dict[str, tuple[str, str]]):
        self.H = height
        self.oy = (height - CONTENT_H) / 2
        self.fonts = fonts
        self.front: list[dict] = []   # criados por cima (insertIndex 0), em ordem de tras p/ frente
        self.back: list[dict] = []    # criados por baixo (append), em ordem de frente p/ tras
        self.anim: list[dict] = []

    def y(self, v: float) -> float:
        return self.oy + v

    def rect(self, lid, name, start, dur, x, y, w, h, color=None, radius=0, gradient=None,
             front=True, opacity=100):
        r = {"size": [w, h], "fillColor": color or WHITE, "roundness": radius}
        if gradient:
            r["fillPaint"] = gradient
        act = {"type": "createFxRectLayer", "compositionId": "main", "layerId": lid, "name": name,
               "activeRange": {"start": start, "duration": dur},
               "transform": tr(x + w / 2, y + h / 2, (w / 2, h / 2), opacity=opacity), "rect": r}
        (self.front if front else self.back).append(act)
        return act

    def text(self, lid, name, start, dur, x, y, w, h, txt, font, size, color=WHITE,
             just="left", strike=False, tracking=0):
        fam, sty = self.fonts[font]
        self.front.append({
            "type": "createFxTextLayer", "compositionId": "main", "layerId": lid, "name": name,
            "activeRange": {"start": start, "duration": dur},
            "transform": tr(x + w / 2, y + h / 2, (w / 2, h / 2)),
            "sourceText": {"text": txt, "fontFamily": fam, "fontStyle": sty, "fontSize": size,
                           "fillColor": color, "justification": just, "boxText": True,
                           "boxPosition": [0, 0], "boxSize": [w, h], "strikethrough": strike,
                           "tracking": tracking}})

    def shape(self, lid, name, start, dur, pts, paint, opacity=1.0, front=False):
        cmds = [{"type": "moveTo", "x": pts[0][0], "y": pts[0][1]}]
        cmds += [{"type": "lineTo", "x": px, "y": py} for px, py in pts[1:]]
        cmds.append({"type": "close"})
        act = {"type": "createFxShapeLayer", "compositionId": "main", "layerId": lid, "name": name,
               "activeRange": {"start": start, "duration": dur}, "transform": tr(0, 0),
               "shape": {"path": {"commands": cmds},
                         "fills": [{"paint": paint, "fillRule": "nonZeroWinding",
                                    "blendMode": "normal", "opacity": opacity}]}}
        (self.front if front else self.back).append(act)


def grad(x0, y0, x1, y1, stops):
    return {"type": "gradient", "gradientType": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}


BRAND_GRAD = [(0, RED), (0.55, ORANGE), (1, YELLOW)]


def build_layers(b: Builder, offer: dict) -> list[dict]:
    H, y = b.H, b.y
    prods = {p["sku"]: p for p in offer["produtos"]}
    story = H > CONTENT_H
    def pos(feed: float, stories: float) -> float:
        return stories if story else feed
    card_top = pos(120, STORY_SAFE_TOP + 110)
    card_height = pos(760, 820)
    card_center = card_top + card_height / 2

    # ---------- fundo (back: frente -> tras) ----------
    b.rect(90, "Card branco", HOOK_END, PRODUCTS_END - HOOK_END, 80, card_top, 920, card_height,
           WHITE, 44, front=False)
    b.shape(92, "Faixa diagonal marca", 0, TOTAL_MS,
            [(1080, y(-40)), (1080, y(560)), (380, H + 40), (-40, H + 40), (-40, H - 40)],
            grad(1080, 0, 0, H, [(0, [0.902, 0.039, 0.078, 1]), (1, [0.35, 0.02, 0.04, 1])]),
            opacity=0.22)
    b.rect(93, "Fundo", 0, TOTAL_MS, 0, 0, W, H, BLACK, front=False)

    # ---------- hook ----------
    hook_pill = pos(340, 610)
    hook_headline = pos(440, 720)
    b.rect(10, "Pill Mes do Cliente", 0, HOOK_END, 330, hook_pill, 420, 66, RED, 33)
    b.text(11, "Texto Mes do Cliente", 0, HOOK_END, 330, hook_pill + 11, 420, 50, "MÊS DO CLIENTE",
           "bold", 34, WHITE, "center", tracking=60)
    b.text(12, "Headline", 0, HOOK_END, 60, hook_headline, 960, 300, "SUA ACADEMIA\nEM CASA",
           "bold", 124, WHITE, "center")
    b.text(13, "Sub hook", 0, HOOK_END, 60, pos(800, 1080), 960, 60, "Até 18x sem juros + 5% OFF no PIX",
           "semibold", 42, GREY, "center")
    b.rect(14, "Linha gradiente hook", 0, HOOK_END, 390, pos(885, 1170), 300, 8, RED, 4,
           grad(0, 0, 300, 0, BRAND_GRAD))
    b.anim += [keys(12, "positionY", [(0, hook_headline + 190, LINEAR),
                                      (450, hook_headline + 150, EASE_OUT)]),
               keys(12, "opacity", [(0, 100, LINEAR), (HOOK_END - 160, 100, LINEAR), (HOOK_END, 0, LINEAR)]),
               keys(10, "opacity", [(0, 100, LINEAR), (HOOK_END - 160, 100, LINEAR), (HOOK_END, 0, LINEAR)]),
               keys(11, "opacity", [(0, 100, LINEAR), (HOOK_END - 160, 100, LINEAR), (HOOK_END, 0, LINEAR)]),
               keys(14, "opacity", [(0, 100, LINEAR), (HOOK_END - 160, 100, LINEAR), (HOOK_END, 0, LINEAR)]),
               keys(10, "scaleX", [(0, 85, LINEAR), (300, 100, EASE_OUT)]),
               keys(10, "scaleY", [(0, 85, LINEAR), (300, 100, EASE_OUT)]),
               keys(14, "scaleX", [(0, 0, LINEAR), (150, 0, LINEAR), (550, 100, EASE_OUT)]),
               keys(13, "opacity", [(0, 0, LINEAR), (150, 0, LINEAR), (400, 100, EASE_OUT),
                                     (HOOK_END - 160, 100, LINEAR), (HOOK_END, 0, LINEAR)])]

    # ---------- logo topo (persistente nos produtos) ----------
    b.front.append({"__image__": True})  # marcador: imagens ficam entre fundo e frente

    # ---------- produtos ----------
    for i, (sku, asset, px, nome) in enumerate(SLIDES):
        p = prods[sku]
        s = HOOK_END + i * SLIDE_MS
        base = 100 + i * 10
        name_y = pos(900, 1200)
        offer_y = pos(960, 1260)
        label_y = pos(1010, 1310)
        amount_y = pos(1040, 1340)
        pix_y = pos(1170, 1470)
        legal_y = pos(1245, H - STORY_SAFE_BOTTOM - 70)
        b.text(base + 1, f"Nome {i+1}", s, SLIDE_MS, 80, name_y, 920, 56, nome, "semibold", 42)
        if p["de"]:
            b.text(base + 2, f"De {i+1}", s, SLIDE_MS, 80, offer_y, 430, 44,
                   f"de {brl(p['de'])}", "medium", 32, [0.78, 0.78, 0.8, 1], strike=True)
        b.text(base + 10, f"Por {i+1}", s, SLIDE_MS, 540 if p["de"] else 80, offer_y,
               460 if p["de"] else 920, 44,
               f"{'por' if p['de'] else 'preço'} {brl(p['por'])}", "semibold", 32, WHITE,
               "right" if p["de"] else "left")
        b.text(base + 3, f"Parcela label {i+1}", s, SLIDE_MS, 80, label_y, 430, 44,
               "18x sem juros de", "semibold", 34, YELLOW)
        b.text(base + 4, f"Parcela {i+1}", s, SLIDE_MS, 72, amount_y, 940, 120,
               brl(p["parc18"]), "bold", 108, WHITE)
        b.rect(base + 5, f"Acento PIX {i+1}", s, SLIDE_MS, 80, pix_y + 5, 7, 42, RED, 3)
        b.text(base + 6, f"PIX {i+1}", s, SLIDE_MS, 104, pix_y, 896, 52,
               f"ou {brl(p['pix'])} no PIX", "semibold", 36, WHITE)
        stagger = [(base + 1, 0), (base + 2, 40), (base + 10, 40), (base + 3, 70), (base + 4, 100), (base + 5, 150),
                   (base + 6, 150)]
        off = FIRST_OFFSET if i == 0 else 0
        for lid, d in stagger:
            d += off
            if lid == base + 2 and not p["de"]:
                continue
            pts = [(0, 0, LINEAR)] + ([(d, 0, LINEAR)] if d else []) + [(d + 220, 100, EASE_OUT)]
            pts += [(SLIDE_MS - 180, 100, LINEAR), (SLIDE_MS - 30, 0, LINEAR)]
            b.anim.append(keys(lid, "opacity", pts))
        if p["pix"] >= FREE_SHIPPING_MIN:
            b.rect(base + 7, f"Selo frete {i+1}", s, SLIDE_MS, 112, card_top + 32, 300, 58, YELLOW, 29,
                   grad(0, 0, 300, 0, [(0, YELLOW), (1, ORANGE)]))
            b.text(base + 8, f"Selo frete txt {i+1}", s, SLIDE_MS, 112, card_top + 43, 300, 40,
                   "FRETE GRÁTIS*", "bold", 30, BLACK, "center")
            b.text(base + 9, f"Nota frete {i+1}", s, SLIDE_MS, 80, legal_y, 920, 34,
                   "*Frete grátis acima de R$ 10 mil. Preços válidos até 30/09/2026.",
                   "medium", 25, GREY)
            for lid in (base + 7, base + 8):
                b.anim += [keys(lid, ax, [(0, 0, LINEAR), (200 + off, 0, LINEAR),
                                          (420 + off, 100, EASE_OUT)]) for ax in ("scaleX", "scaleY")]
        else:
            b.text(base + 9, f"Nota {i+1}", s, SLIDE_MS, 80, legal_y, 920, 34,
                   "Preços válidos até 30/09/2026.", "medium", 25, GREY)

    # card entra de baixo
    b.anim += [keys(90, "positionY", [(0, card_center + 500, LINEAR),
                                      (420, card_center, EASE_OUT)])]

    # ---------- end card ----------
    e0, ed = PRODUCTS_END, TOTAL_MS - PRODUCTS_END
    b.text(80, "End beneficios", e0, ed, 60, pos(650, 900), 960, 60, "Até 18x sem juros  ·  5% OFF no PIX",
           "semibold", 42, WHITE, "center")
    b.text(81, "End frete", e0, ed, 60, pos(710, 965), 960, 50, "Frete grátis acima de R$ 10 mil",
           "medium", 34, GREY, "center")
    b.rect(82, "CTA botao", e0, ed, 260, pos(815, 1080), 560, 104, RED, 52,
           grad(0, 0, 560, 0, [(0, RED), (1, [0.78, 0.02, 0.06, 1])]))
    b.text(83, "CTA texto", e0, ed, 260, pos(839, 1104), 560, 60, "COMPRE AGORA", "bold", 48, WHITE,
           "center", tracking=40)
    b.text(84, "URL", e0, ed, 60, pos(960, 1235), 960, 50, "casadofitness.com.br", "medium", 34, GREY,
           "center")
    b.rect(85, "Linha gradiente end", e0, ed, 340, pos(590, 825), 400, 8, RED, 4,
           grad(0, 0, 400, 0, BRAND_GRAD))
    b.anim += [keys(85, "scaleX", [(0, 0, LINEAR), (350, 100, EASE_OUT)]),
               keys(80, "opacity", [(0, 0, LINEAR), (150, 0, LINEAR), (400, 100, EASE_OUT)]),
               keys(81, "opacity", [(0, 0, LINEAR), (220, 0, LINEAR), (470, 100, EASE_OUT)]),
               keys(84, "opacity", [(0, 0, LINEAR), (300, 0, LINEAR), (550, 100, EASE_OUT)])]
    for lid in (82, 83):
        b.anim += [keys(lid, "scaleX", [(0, 0, LINEAR), (280, 0, LINEAR), (560, 108, EASE_OUT),
                                        (700, 100, EASE_INOUT), (950, 104, EASE_INOUT),
                                        (1250, 100, EASE_INOUT)]),
                   keys(lid, "scaleY", [(0, 0, LINEAR), (280, 0, LINEAR), (560, 108, EASE_OUT),
                                        (700, 100, EASE_INOUT), (950, 104, EASE_INOUT),
                                        (1250, 100, EASE_INOUT)])]


def image_layers(b: Builder) -> list[dict]:
    """Camadas Image (via commit do documento): produtos, logos e textura."""
    story = b.H > CONTENT_H
    layers = []
    # frente -> tras
    layers.append({"type": "Image", "id": 70, "name": "Logo end card",
                   "activeRange": {"start": PRODUCTS_END, "duration": TOTAL_MS - PRODUCTS_END},
                   "transform": tr(540, 740 if story else 470, (1200, 164), 32),
                   "source": {"assetId": "logo-white", "fit": "contain"}})
    layers.append({"type": "Image", "id": 71, "name": "Logo topo",
                   "activeRange": {"start": 0, "duration": PRODUCTS_END},
                   "transform": tr(540, STORY_SAFE_TOP + 50 if story else 62, (1200, 164), 17),
                   "source": {"assetId": "logo-white", "fit": "contain"}})
    for i, (sku, asset, px, _) in enumerate(SLIDES):
        base = (745 if story else 730) / px * 100
        layers.append({"type": "Image", "id": 60 + i, "name": f"Produto {i+1} - {asset}",
                       "activeRange": {"start": HOOK_END + i * SLIDE_MS, "duration": SLIDE_MS},
                       "transform": tr(540, 770 if story else 500, (px / 2, px / 2), base),
                       "source": {"assetId": asset, "fit": "contain"}})
    layers.append({"type": "Image", "id": 72, "name": "Simbolo textura",
                   "activeRange": {"start": 0, "duration": TOTAL_MS},
                   "transform": tr(760, b.H - 330, (600, 269), 120, 7),
                   "source": {"assetId": "symbol-white", "fit": "contain"}})
    return layers


def image_anim(b: Builder) -> list[dict]:
    story = b.H > CONTENT_H
    anim = []
    for i, (_, _, px, _) in enumerate(SLIDES):
        base = (745 if story else 730) / px * 100
        lid = 60 + i
        o = FIRST_OFFSET if i == 0 else 0
        anim += [keys(lid, "positionX", [(0, 700, LINEAR)] + ([(o, 700, LINEAR)] if o else []) + [(420 + o, 540, EASE_OUT),
                                         (SLIDE_MS - 220, 540, LINEAR),
                                         (SLIDE_MS, 400, EASE_INOUT)]),
                 keys(lid, "scaleX", [(0, base * 0.9, LINEAR), (420 + o, base, EASE_OUT),
                                      (SLIDE_MS - 220, base * 1.02, LINEAR),
                                      (SLIDE_MS, base * 1.02, LINEAR)]),
                 keys(lid, "scaleY", [(0, base * 0.9, LINEAR), (420 + o, base, EASE_OUT),
                                      (SLIDE_MS - 220, base * 1.02, LINEAR),
                                      (SLIDE_MS, base * 1.02, LINEAR)]),
                 keys(lid, "opacity", [(0, 0, LINEAR)] + ([(o, 0, LINEAR)] if o else []) + [(160 + o, 100, EASE_OUT),
                                       (SLIDE_MS - 200, 100, LINEAR), (SLIDE_MS - 20, 0, LINEAR)])]
    anim += [keys(70, "scale" + ax, [(0, 28, LINEAR), (350, 32, EASE_OUT)]) for ax in "XY"]
    anim += [keys(70, "opacity", [(0, 0, LINEAR), (250, 100, EASE_OUT)])]
    anim += [keys(72, "rotation", [(0, -4, LINEAR), (TOTAL_MS, 4, LINEAR)])]
    return anim


def build_project(fmt: str) -> Path:
    height, tag = FORMATS[fmt]
    work = ROOT / ".tesseract-work" / tag
    work.mkdir(parents=True, exist_ok=True)
    project_path = ROOT / "projeto" / f"{tag}.tsrct"
    project_path.unlink(missing_ok=True)
    project = str(project_path)
    offer = json.loads(SNAPSHOT.read_text(encoding="utf-8"))

    run("project", "create", "--project", project)
    fonts = {}
    for key, f in (("bold", "BaiJamjuree-Bold"), ("semibold", "BaiJamjuree-SemiBold"),
                   ("medium", "BaiJamjuree-Medium")):
        r = json.loads(run("project", "import-font", "--project", project,
                           "--file", str(BRAND / "fonts" / f"{f}.ttf")).strip().splitlines()[-1])
        face = r["faces"][0]
        fonts[key] = (face.get("typographicFamilyName") or r["fontFamily"],
                      face.get("typographicStyleName") or r["fontStyle"])
    for asset, path in [("logo-white", BRAND / "logo" / "logo-header-white.png"),
                        ("symbol-white", BRAND / "logo" / "logo-footer.png")] +                        [(a, PRODUCTS / f"{a}.png") for _, a, _, _ in SLIDES]:
        run("project", "import-asset", "--project", project, "--file", str(path),
            "--asset-id", asset, "--kind", "image")

    b = Builder(height, fonts)
    build_layers(b, offer)

    editable = work / "editable.json"
    run("project", "checkout", "--project", project, "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    doc["dimensions"] = {"width": W, "height": height}
    doc["duration"] = TOTAL_MS / 1000
    doc["composition"]["layers"] = image_layers(b)

    front = [a for a in b.front if not a.get("__image__")]
    ids = [l["id"] for l in doc["composition"]["layers"]] + [a["layerId"] for a in b.back + front]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"IDs de camada duplicados: {dup}")

    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", project, "--file", str(editable))
    acts = list(b.back) + [{**a, "insertIndex": 0} for a in front] + b.anim + image_anim(b)
    edits = work / "edits.json"
    edits.write_text(json.dumps(acts, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "apply", "--project", project, "--actions", str(edits))
    return project_path


def render(fmt: str, project: Path, version: int, preview_only: bool = False,
           export_gif: bool = False) -> None:
    height, tag = FORMATS[fmt]
    stamps = ["0", "700", "1400", "2300", "3000", "4300", "5900", "7700", "8600", "9000", "9500",
              str(TOTAL_MS - 10)]
    tile = ("324", "405") if fmt == "feed" else ("270", "480")
    run("filmstrip", "--project", str(project), "--timestamps-ms", *stamps,
        "--tile-width", tile[0], "--tile-height", tile[1], "--items-per-row", "6",
        "--output", str(ROOT / "previews" / f"filmstrip_{tag}.png"))
    if preview_only:
        return
    mp4 = ROOT / f"{SLUG}_{tag}_v{version:02d}.mp4"
    run("export", "--project", str(project), "--output", str(mp4))
    if export_gif:
        gif = mp4.with_suffix(".gif")
        vf = ("fps=15,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=256:"
              "stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-vf", vf, "-loop", "0",
                        str(gif)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nova-versao", action="store_true")
    ap.add_argument("--formato", choices=list(FORMATS), action="append")
    ap.add_argument("--preview-only", action="store_true")
    ap.add_argument("--gif", action="store_true", help="gera GIF alem do MP4")
    args = ap.parse_args()
    if args.preview_only and args.nova_versao:
        ap.error("--preview-only nao pode ser combinado com --nova-versao")
    version = 3 if args.preview_only else prepare(ROOT, SLUG, args.nova_versao)
    if args.preview_only:
        for fmt in args.formato or list(FORMATS):
            project = build_project(fmt)
            render(fmt, project, version, preview_only=True)
            print(f"preview v{version:02d} {fmt}: ok")
        return
    shutil.copy(SNAPSHOT, ROOT / "offer.json")
    shutil.copy(__file__, ROOT / "build_snapshot.py")
    notes = ROOT / "notes.md"
    if not notes.exists():
        notes.write_text(f"# Notas — v{version:02d}" + chr(10) * 2 + "## Mudanças" + chr(10) + "- " + chr(10),
                         encoding="utf-8")
    for fmt in args.formato or list(FORMATS):
        project = build_project(fmt)
        render(fmt, project, version, export_gif=args.gif)
        print(f"v{version:02d} {fmt}: ok")


if __name__ == "__main__":
    main()
