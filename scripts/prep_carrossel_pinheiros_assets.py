"""Prepara os assets do carrossel de Pinheiros no Tesseract (logos das marcas e ícone vindos do carrossel original; fotos de cenário novas).

- Logos e ícone do cartão: recortados dos cartões originais do anúncio (versão 9:16) por chave de luminância (branco -> alfa), mantendo todos os elementos.
- Fotos de cenário: projeto real (academia de hotel) do Instagram da marca, recortadas por formato (cover).
Saída: assets/carrossel-pinheiros/{logos,fotos}/
"""
from pathlib import Path

import numpy as np
from PIL import Image

LAB = Path(__file__).resolve().parents[1]
WS = LAB.parent
CARDS = WS / "pecas" / "carrossel-pinheiros-video" / "fonte" / "laminas"
FOTOS_SRC = WS / "outputs" / "ref_criativos_b2b_20261001"
OUT = LAB / "assets" / "carrossel-pinheiros"

# zonas aproximadas (x0, y0, x1, y1) na lâmina 9:16 de 941x1672 ("marcas líderes", 8e36ae95.jpg)
LOGO_ZONAS = {
    "speedo-fitness": (95, 720, 485, 860),
    "tauka": (115, 940, 445, 1020),
    "leforz": (115, 1135, 460, 1205),
    "mormaii": (600, 700, 845, 745),
    "schwinn": (610, 795, 840, 840),
    "waterrower": (625, 885, 825, 925),
    "nohrd": (625, 975, 830, 1030),
    "bowflex": (620, 1075, 835, 1118),
    "bodybike": (620, 1165, 830, 1208),
}


def chave_branco(im: Image.Image, lo: int = 110, hi: int = 185) -> Image.Image:
    """Branco -> alfa pela luminância; cor final branca."""
    g = np.asarray(im.convert("L"), dtype=np.float32)
    alfa = np.clip((g - lo) / (hi - lo), 0, 1)
    saida = np.zeros((*g.shape, 4), dtype=np.uint8)
    saida[..., :3] = 255
    saida[..., 3] = (alfa * 255).astype(np.uint8)
    return Image.fromarray(saida, "RGBA")


def recorta_logo(im: Image.Image, zona: tuple[int, int, int, int]) -> Image.Image:
    rgba = chave_branco(im.crop(zona))
    caixa = rgba.getchannel("A").point(lambda v: 255 if v > 90 else 0).getbbox()
    pad = 4
    x0, y0, x1, y1 = caixa
    return rgba.crop((max(0, x0 - pad), max(0, y0 - pad), min(rgba.width, x1 + pad), min(rgba.height, y1 + pad)))


def cobre(im: Image.Image, w: int, h: int, foco_y: float = 0.5) -> Image.Image:
    esc = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = round((r.height - h) * foco_y)
    return r.crop((x, y, x + w, y + h))


def main() -> None:
    (OUT / "logos").mkdir(parents=True, exist_ok=True)
    (OUT / "fotos").mkdir(parents=True, exist_ok=True)
    marcas = Image.open(CARDS / "8e36ae95.jpg").convert("RGB")
    for nome, zona in LOGO_ZONAS.items():
        recorta_logo(marcas, zona).save(OUT / "logos" / f"{nome}.png")
    # ícone do cartão de parcelamento (1080x1920, 5092ef14.jpg), zona acima do título
    parcela = Image.open(CARDS / "5092ef14.jpg").convert("RGB")
    recorta_logo(parcela, (400, 640, 700, 830)).save(OUT / "logos" / "icone-parcelamento.png")
    # ícone da marca (símbolo branco) já existe no brand kit; copiado para o carrossel
    simb = Image.open(WS / "pecas" / "b2b-generalista-projetos" / "fonte" / "logo-icone.png").convert("RGBA")
    simb.save(OUT / "logos" / "cdf-simbolo.png")
    # fotos de cenário: academia de hotel (projeto real). 0 = fileira de esteiras, 1 = sala de bikes reclináveis,
    # 2 = escada + esteiras, 3 = sala de spinning com forro curvo, 4 = spinning + escada
    fotos = {n: Image.open(FOTOS_SRC / f"car_rj_01-21_{n}.jpg").convert("RGB") for n in range(5)}
    for n, im in fotos.items():
        im.save(OUT / "fotos" / f"cenario-{n}.jpg", quality=95)


if __name__ == "__main__":
    main()
    for p in sorted((OUT / "logos").glob("*.png")):
        print(p.name, Image.open(p).size)
