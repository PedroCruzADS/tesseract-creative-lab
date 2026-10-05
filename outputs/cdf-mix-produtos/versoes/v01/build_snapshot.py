"""Monta o GIF-teste: 4 produtos CDF (Merchant Center), 1080x1080, 5s."""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".tesseract-work"
TSRCT = os.path.join(os.environ["LOCALAPPDATA"], "Tesseract", "bin", "tsrct.cmd")
PROJECT = str(ROOT / "Project.tsrct")

W = H = 1080
DURATION_MS = 5000
SLIDE_MS = 1250
BAR_Y, BAR_H = 910, 170
DARK = [0.07, 0.07, 0.08, 1]
WHITE = [1, 1, 1, 1]

SLIDES = [
    ("esteira-speedo-tr7", 1000, "ESTEIRA SPEEDO TR7"),
    ("bike-mormaii-motion-s", 1000, "BICICLETA MORMAII MOTION-S"),
    ("eliptico-starke-sh30", 1000, "ELÍPTICO STARKE SH30"),
    ("estacao-speedo-multi3", 960, "ESTAÇÃO SPEEDO MULTI 3"),
]
IMG_CENTER_Y = 495
IMG_TARGET_PX = 760


def run(*args):
    out = subprocess.run([TSRCT, *args], capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit(f"tsrct {' '.join(args)} falhou:\n{out.stdout}\n{out.stderr}")
    return out.stdout


def tr(pos, anchor=(0, 0), scale=100, opacity=100):
    return {"anchorPoint": list(anchor), "position": list(pos), "scale": [scale, scale],
            "rotation": 0, "opacity": opacity}


def kf(kid, t, value, ease="out"):
    easing = ({"type": "cubicBezier", "x1": 0.16, "y1": 1, "x2": 0.3, "y2": 1}
              if ease == "out" else {"type": "linear"})
    return {"id": kid, "layerTime": t, "value": {"type": "float", "value": value}, "easing": easing}


def commit_document():
    editable = WORK / "editable.json"
    run("project", "checkout", "--project", PROJECT, "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    doc["dimensions"] = {"width": W, "height": H}
    doc["duration"] = DURATION_MS / 1000
    layers = []
    for i, (asset, px, _) in enumerate(SLIDES):
        base_scale = IMG_TARGET_PX / px * 100
        layers.append({
            "type": "Image", "id": 11 + i, "name": f"Produto {i + 1} - {asset}",
            "activeRange": {"start": i * SLIDE_MS, "duration": SLIDE_MS},
            "transform": tr((W / 2, IMG_CENTER_Y), (px / 2, px / 2), base_scale),
            "source": {"assetId": asset, "fit": "contain"},
        })
    doc["composition"]["layers"] = layers
    doc["composition"].pop("dynamics", None)
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", PROJECT, "--file", str(editable))


def actions():
    acts = [
        {"type": "createFxRectLayer", "compositionId": "main", "layerId": 1, "name": "Fundo branco",
         "activeRange": {"start": 0, "duration": DURATION_MS}, "transform": tr((0, 0)),
         "rect": {"size": [W, H], "fillColor": WHITE}},
        {"type": "createFxRectLayer", "compositionId": "main", "layerId": 2, "name": "Faixa inferior",
         "insertIndex": 0, "activeRange": {"start": 0, "duration": DURATION_MS}, "transform": tr((0, BAR_Y)),
         "rect": {"size": [W, BAR_H], "fillColor": DARK}},
        {"type": "createFxTextLayer", "compositionId": "main", "layerId": 3, "name": "Marca (texto)",
         "insertIndex": 0, "activeRange": {"start": 0, "duration": DURATION_MS}, "transform": tr((40, 30)),
         "sourceText": {"text": "CASA DO FITNESS", "fontFamily": "Anton", "fontStyle": "Regular",
                        "fontSize": 44, "fillColor": DARK, "justification": "center",
                        "boxText": True, "boxPosition": [0, 0], "boxSize": [W - 80, 70]}},
    ]
    for i, (asset, px, name) in enumerate(SLIDES):
        start = i * SLIDE_MS
        img_id, txt_id = 11 + i, 21 + i
        base = IMG_TARGET_PX / px * 100
        acts.append({
            "type": "createFxTextLayer", "compositionId": "main", "layerId": txt_id,
            "name": f"Nome produto {i + 1}", "insertIndex": 0,
            "activeRange": {"start": start, "duration": SLIDE_MS},
            "transform": tr((40, BAR_Y + 45)),
            "sourceText": {"text": name, "fontFamily": "Anton", "fontStyle": "Regular", "fontSize": 64,
                           "fillColor": WHITE, "justification": "center", "boxText": True,
                           "boxPosition": [0, 0], "boxSize": [W - 80, 100]}})
        for axis in ("scaleX", "scaleY"):
            acts.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                         "property": {"layerId": img_id, "propertyType": axis},
                         "keyframes": [kf(f"p{i}-{axis}-a", 0, base * 1.10, "lin"),
                                       kf(f"p{i}-{axis}-b", 450, base),
                                       kf(f"p{i}-{axis}-c", SLIDE_MS, base * 0.98, "lin")]})
        acts.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                     "property": {"layerId": txt_id, "propertyType": "positionY"},
                     "keyframes": [kf(f"t{i}-y-a", 0, BAR_Y + 62, "lin"),
                                   kf(f"t{i}-y-b", 300, BAR_Y + 45)]})
    path = WORK / "edits.json"
    path.write_text(json.dumps(acts, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "apply", "--project", PROJECT, "--actions", str(path))


if __name__ == "__main__":
    commit_document()
    actions()
    print(run("project", "inspect", "--project", PROJECT)[:600])
