"""Criativo CDF 'Mes do Cliente' - mix de 4 produtos (feed 4:5 e stories 9:16) no Tesseract.

Uso: python scripts/build_cdf_mix_v02.py feed|stories
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
TSRCT = os.path.join(os.environ["LOCALAPPDATA"], "Tesseract", "bin", "tsrct.cmd")
SNAPSHOT = LAB / "data" / "cdf-mix-produtos" / "offer_20260923.json"
BRAND = LAB / "assets" / "casa-do-fitness-brand"
PRODUCTS = LAB / "assets" / "cdf-merchant-teste" / "product"

FORMATS = {"feed": (1350, "4x5"), "stories": (1920, "9x16")}
W = 1080
CONTENT_H = 1350  # layout desenhado em 1080x1350; no stories fica centralizado (safe area)

# timeline (ms)
HOOK_END = 1000
SLIDE_MS = 1100
PRODUCTS_END = HOOK_END + 4 * SLIDE_MS  # 5400
TOTAL_MS = 6500

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

    # ---------- fundo (back: frente -> tras) ----------
    b.rect(90, "Card branco", HOOK_END, PRODUCTS_END - HOOK_END, 80, y(130), 920, 720,
           WHITE, 44, front=False)
    b.shape(92, "Faixa diagonal marca", 0, TOTAL_MS,
            [(1080, y(-40)), (1080, y(560)), (380, H + 40), (-40, H + 40), (-40, H - 40)],
            grad(1080, 0, 0, H, [(0, [0.902, 0.039, 0.078, 1]), (1, [0.35, 0.02, 0.04, 1])]),
            opacity=0.22)
    b.rect(93, "Fundo", 0, TOTAL_MS, 0, 0, W, H, BLACK, front=False)

    # ---------- hook 0-1000 ----------
    b.rect(10, "Pill Mes do Cliente", 0, HOOK_END, 330, y(300), 420, 66, RED, 33)
    b.text(11, "Texto Mes do Cliente", 0, HOOK_END, 330, y(311), 420, 50, "MÊS DO CLIENTE",
           "bold", 34, WHITE, "center", tracking=60)
    b.text(12, "Headline", 0, HOOK_END, 60, y(400), 960, 300, "SUA ACADEMIA\nEM CASA",
           "bold", 124, WHITE, "center")
    b.text(13, "Sub hook", 0, HOOK_END, 60, y(760), 960, 60, "Até 18x sem juros + 5% OFF no PIX",
           "semibold", 42, GREY, "center")
    b.rect(14, "Linha gradiente hook", 0, HOOK_END, 390, y(845), 300, 8, RED, 4,
           grad(0, 0, 300, 0, BRAND_GRAD))
    b.anim += [keys(12, "positionY", [(0, y(590), LINEAR), (450, y(550), EASE_OUT)]),
               keys(12, "opacity", [(0, 100, LINEAR), (880, 100, LINEAR), (1000, 0, LINEAR)]),
               keys(10, "scaleX", [(0, 85, LINEAR), (300, 100, EASE_OUT)]),
               keys(10, "scaleY", [(0, 85, LINEAR), (300, 100, EASE_OUT)]),
               keys(14, "scaleX", [(0, 0, LINEAR), (150, 0, LINEAR), (550, 100, EASE_OUT)]),
               keys(13, "opacity", [(0, 0, LINEAR), (150, 0, LINEAR), (400, 100, EASE_OUT)])]

    # ---------- logo topo (persistente nos produtos) ----------
    b.front.append({"__image__": True})  # marcador: imagens ficam entre fundo e frente

    # ---------- produtos ----------
    for i, (sku, asset, px, nome) in enumerate(SLIDES):
        p = prods[sku]
        s = HOOK_END + i * SLIDE_MS
        base = 100 + i * 10
        b.text(base + 1, f"Nome {i+1}", s, SLIDE_MS, 80, y(880), 920, 56, nome, "semibold", 42)
        price_top = 940 if p["de"] else 900
        if p["de"]:
            b.text(base + 2, f"De {i+1}", s, SLIDE_MS, 80, y(price_top), 920, 44,
                   f"de {brl(p['de'])}", "medium", 34, [0.78, 0.78, 0.8, 1], strike=True)
        b.text(base + 3, f"Parcela label {i+1}", s, SLIDE_MS, 80, y(price_top + 44), 920, 44,
               "18x sem juros de", "semibold", 34, YELLOW)
        b.text(base + 4, f"Parcela {i+1}", s, SLIDE_MS, 72, y(price_top + 78), 940, 130,
               brl(p["parc18"]), "bold", 108, WHITE)
        b.rect(base + 5, f"Pill PIX {i+1}", s, SLIDE_MS, 80, y(price_top + 222), 600, 70, RED, 35,
               grad(0, 0, 600, 0, [(0, RED), (1, [0.78, 0.02, 0.06, 1])]))
        b.text(base + 6, f"PIX {i+1}", s, SLIDE_MS, 80, y(price_top + 235), 600, 50,
               f"ou {brl(p['pix'])} no PIX", "bold", 36, WHITE, "center")
        stagger = [(base + 1, 0), (base + 2, 40), (base + 3, 70), (base + 4, 100), (base + 5, 150),
                   (base + 6, 150)]
        for lid, d in stagger:
            if lid == base + 2 and not p["de"]:
                continue
            pts = [(0, 0, LINEAR)] + ([(d, 0, LINEAR)] if d else []) + [(d + 220, 100, EASE_OUT)]
            b.anim.append(keys(lid, "opacity", pts))
        if p["pix"] >= FREE_SHIPPING_MIN:
            b.rect(base + 7, f"Selo frete {i+1}", s, SLIDE_MS, 112, y(162), 300, 58, YELLOW, 29,
                   grad(0, 0, 300, 0, [(0, YELLOW), (1, ORANGE)]))
            b.text(base + 8, f"Selo frete txt {i+1}", s, SLIDE_MS, 112, y(173), 300, 40,
                   "FRETE GRÁTIS*", "bold", 30, BLACK, "center")
            b.text(base + 9, f"Nota frete {i+1}", s, SLIDE_MS, 80, y(1300), 920, 34,
                   "*Frete grátis em pedidos acima de R$ 10 mil. Preços válidos em 23/09/2026.",
                   "medium", 22, GREY)
            for lid in (base + 7, base + 8):
                b.anim += [keys(lid, "scaleX", [(0, 60, LINEAR), (200, 0, LINEAR), (420, 100, EASE_OUT)]),
                           keys(lid, "scaleY", [(0, 60, LINEAR), (200, 0, LINEAR), (420, 100, EASE_OUT)])]
        else:
            b.text(base + 9, f"Nota {i+1}", s, SLIDE_MS, 80, y(1300), 920, 34,
                   "Preços válidos em 23/09/2026.", "medium", 22, GREY)

    # card entra de baixo
    b.anim += [keys(90, "positionY", [(0, y(130 + 360) + 500, LINEAR), (420, y(130 + 360), EASE_OUT)])]

    # ---------- end card ----------
    e0, ed = PRODUCTS_END, TOTAL_MS - PRODUCTS_END
    b.text(80, "End beneficios", e0, ed, 60, y(700), 960, 60, "Até 18x sem juros  ·  5% OFF no PIX",
           "semibold", 42, WHITE, "center")
    b.text(81, "End frete", e0, ed, 60, y(760), 960, 50, "Frete grátis acima de R$ 10 mil",
           "medium", 34, GREY, "center")
    b.rect(82, "CTA botao", e0, ed, 260, y(860), 560, 104, RED, 52,
           grad(0, 0, 560, 0, [(0, RED), (1, [0.78, 0.02, 0.06, 1])]))
    b.text(83, "CTA texto", e0, ed, 260, y(884), 560, 60, "COMPRE AGORA", "bold", 48, WHITE,
           "center", tracking=40)
    b.text(84, "URL", e0, ed, 60, y(1000), 960, 50, "casadofitness.com.br", "medium", 34, GREY,
           "center")
    b.rect(85, "Linha gradiente end", e0, ed, 340, y(640), 400, 8, RED, 4,
           grad(0, 0, 400, 0, BRAND_GRAD))
    b.anim += [keys(85, "scaleX", [(0, 0, LINEAR), (350, 100, EASE_OUT)]),
               keys(80, "opacity", [(0, 0, LINEAR), (150, 0, LINEAR), (400, 100, EASE_OUT)]),
               keys(81, "opacity", [(0, 0, LINEAR), (220, 0, LINEAR), (470, 100, EASE_OUT)]),
               keys(84, "opacity", [(0, 0, LINEAR), (300, 0, LINEAR), (550, 100, EASE_OUT)])]
    for lid in (82, 83):
        b.anim += [keys(lid, "scaleX", [(0, 0, LINEAR), (280, 0, LINEAR), (560, 108, EASE_OUT),
                                        (700, 100, EASE_INOUT), (900, 104, EASE_INOUT),
                                        (1100, 100, EASE_INOUT)]),
                   keys(lid, "scaleY", [(0, 0, LINEAR), (280, 0, LINEAR), (560, 108, EASE_OUT),
                                        (700, 100, EASE_INOUT), (900, 104, EASE_INOUT),
                                        (1100, 100, EASE_INOUT)])]


def image_layers(b: Builder) -> list[dict]:
    """Camadas Image (via commit do documento): produtos, logos e textura."""
    y = b.y
    layers = []
    # frente -> tras
    layers.append({"type": "Image", "id": 70, "name": "Logo end card",
                   "activeRange": {"start": PRODUCTS_END, "duration": TOTAL_MS - PRODUCTS_END},
                   "transform": tr(540, y(520), (1200, 164), 32),
                   "source": {"assetId": "logo-white", "fit": "contain"}})
    layers.append({"type": "Image", "id": 71, "name": "Logo topo",
                   "activeRange": {"start": 0, "duration": PRODUCTS_END},
                   "transform": tr(540, y(62), (1200, 164), 17),
                   "source": {"assetId": "logo-white", "fit": "contain"}})
    for i, (sku, asset, px, _) in enumerate(SLIDES):
        base = 700 / px * 100
        layers.append({"type": "Image", "id": 60 + i, "name": f"Produto {i+1} - {asset}",
                       "activeRange": {"start": HOOK_END + i * SLIDE_MS, "duration": SLIDE_MS},
                       "transform": tr(540, y(490), (px / 2, px / 2), base),
                       "source": {"assetId": asset, "fit": "contain"}})
    layers.append({"type": "Image", "id": 72, "name": "Simbolo textura",
                   "activeRange": {"start": 0, "duration": TOTAL_MS},
                   "transform": tr(760, b.H - 330, (600, 269), 120, 7),
                   "source": {"assetId": "symbol-white", "fit": "contain"}})
    return layers


def image_anim(b: Builder) -> list[dict]:
    y = b.y
    anim = []
    for i, (_, _, px, _) in enumerate(SLIDES):
        base = 700 / px * 100
        lid = 60 + i
        anim += [keys(lid, "positionX", [(0, 700, LINEAR), (380, 540, EASE_OUT)]),
                 keys(lid, "scaleX", [(0, base * 0.9, LINEAR), (380, base, EASE_OUT),
                                      (SLIDE_MS, base * 1.03, LINEAR)]),
                 keys(lid, "scaleY", [(0, base * 0.9, LINEAR), (380, base, EASE_OUT),
                                      (SLIDE_MS, base * 1.03, LINEAR)]),
                 keys(lid, "opacity", [(0, 0, LINEAR), (160, 100, EASE_OUT)])]
    anim += [keys(70, "scale" + ax, [(0, 28, LINEAR), (350, 32, EASE_OUT)]) for ax in "XY"]
    anim += [keys(70, "opacity", [(0, 0, LINEAR), (250, 100, EASE_OUT)])]
    anim += [keys(72, "rotation", [(0, -4, LINEAR), (TOTAL_MS, 4, LINEAR)])]
    return anim


def main() -> None:
    fmt = sys.argv[1] if len(sys.argv) > 1 else "feed"
    height, tag = FORMATS[fmt]
    root = LAB / "outputs" / f"20260923_cdf-mix-produtos_mes-do-cliente_{tag}_v02"
    work = root / ".tesseract-work"
    root.mkdir()  # falha se ja existir: nao sobrescreve trabalho anterior
    for d in (work, root / "Previews"):
        d.mkdir(parents=True)
    project = str(root / "Project.tsrct")
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
                        ("symbol-white", BRAND / "logo" / "logo-footer.png")] + \
                       [(a, PRODUCTS / f"{a}.png") for _, a, _, _ in SLIDES]:
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
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", project, "--file", str(editable))

    front = [a for a in b.front if not a.get("__image__")]
    ids = [l["id"] for l in image_layers(b)] + [a["layerId"] for a in b.back + front]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"IDs de camada duplicados: {dup}")
    acts = []
    for a in b.back:           # cada um vai para o fundo da pilha
        acts.append(a)
    for a in front:            # cada um vai para o topo da pilha
        acts.append({**a, "insertIndex": 0})
    acts += b.anim + image_anim(b)
    edits = work / "edits.json"
    edits.write_text(json.dumps(acts, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "apply", "--project", project, "--actions", str(edits))
    print(json.dumps({"project": project, "fonts": fonts, "layers": len(acts)}))


if __name__ == "__main__":
    main()
