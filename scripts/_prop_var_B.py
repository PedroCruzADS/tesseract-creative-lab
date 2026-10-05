"""Carrossel de anúncio de Pinheiros refeito no Tesseract: mesmas cinco cartas e todos os elementos, com fotos de cenário novas.

v04: bordas das fotos arredondadas e suaves, degradê escuro suave em cima e embaixo, risquinhos laranja nos quatro cantos
sem corte reto, símbolo da CDF no topo.
v03: textos só com fade (sem tremulação), blocos centralizados no mesmo eixo, rodapé escuro com risquinhos laranja e supersampling 4K.
v02 (01/10/2026): texto reto (sem itálico), títulos em degradê numa única camada (sem letras soltas), faixas limpas, cartas com 3,4 s de leitura,
barra de progresso do carrossel, sombras suaves e acabamento em movimento.

Cartas (original: anúncio "Estático - Carrossel", conta de Pinheiros):
  1 Valorize seu condomínio com uma academia de verdade   2 Compre ou alugue   3 Equipamentos fitness com marcas líderes
  4 Parcelamento facilitado para montar academia no seu condomínio   5 Solicite seu orçamento (Clique aqui)

Uso: python scripts/build_carrossel_pinheiros.py [--formato feed|stories] [--preview-only]
Pré-requisito: python scripts/prep_carrossel_pinheiros_assets.py
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_cdf_mix import (BRAND, EASE_INOUT, EASE_OUT, LINEAR, Builder, grad, keys, run, tr)  # noqa: E402

LAB = Path(__file__).resolve().parents[1]
ASSETS = LAB / "assets" / "carrossel-pinheiros"
ROOT = LAB / "outputs" / "_proposta_B"
SLUG = "carrossel-pinheiros-cenarios"
VERSAO = 9
FORMATS = {"feed": (1080, "feed-1x1"), "stories": (1920, "stories-9x16")}
W = 1080
SOB = 44                       # px da foto que passam por baixo da faixa da carta 2 (a emenda fica escondida)
SCENE = 3400                 # ms por carta (leitura confortável)
N = 5
TOTAL = SCENE * N
FADE_IN, FADE_OUT = 420, 300
FONT_FILES = {"bold": "BaiJamjuree-Bold", "semibold": "BaiJamjuree-SemiBold", "medium": "BaiJamjuree-Medium"}
WHITE = [1, 1, 1, 1]
RED = [0.93, 0.07, 0.07, 1]
ORANGE = [1.0, 0.45, 0.0, 1]
AMBER = [1.0, 0.66, 0.0, 1]
DARK = [0.145, 0.145, 0.15, 1]
BLACK = [0.035, 0.035, 0.04, 1]
BASE_FOCO = 0.62            # topo da caixa de texto = centro - tamanho * BASE_FOCO
BRAND_STOPS = [(0.0, RED), (0.55, ORANGE), (1.0, AMBER)]


class Cena:
    """Ids, camadas de imagem e animações de uma carta."""

    def __init__(self, b: Builder, idx: int):
        self.b, self.idx = b, idx
        self.start = idx * SCENE
        self.nid = 1000 * (idx + 1)
        self.photos: list[dict] = []   # fotos de cenário
        self.logos: list[dict] = []    # logos e ícones (à frente das fotos)
        self.dims: list[dict] = []     # escurecimentos e degradês (entre fotos e logos)
        self.img_anim: list[dict] = []

    def novo_id(self) -> int:
        self.nid += 1
        return self.nid

    def entra(self, lid: int, atraso: int, cy: float | None = None, dy: float = 24, dur: int = 460) -> None:
        pts = [(0, 0, LINEAR)] + ([(atraso, 0, LINEAR)] if atraso else []) + [(atraso + 300, 100, EASE_OUT),
                                                                           (SCENE - FADE_OUT, 100, LINEAR), (SCENE - 20, 0, LINEAR)]
        self.b.anim.append(keys(lid, "opacity", pts))
        # sem deslocamento vertical: posições fracionárias durante a animação faziam o texto tremer


_estilo_id = [500]


def estilo(b: Builder, lid: int, payload: dict) -> None:
    _estilo_id[0] += 1
    b.anim.append({"type": "addFxLayerStyle", "compositionId": "main", "layerId": lid, "itemId": _estilo_id[0], "style": payload})


def sombra(b: Builder, lid: int, forte: bool = False) -> None:
    estilo(b, lid, {"type": "dropShadow", "enabled": True, "color": [0, 0, 0, 0.62 if forte else 0.48], "offset": [0, 4],
                    "blurRadius": 14 if forte else 10, "spreadRadius": 0, "blendMode": "normal"})


def medida(fonte: str, size: int, texto: str) -> float:
    return ImageFont.truetype(str(BRAND / "fonts" / f"{FONT_FILES[fonte]}.ttf"), size).getlength(texto)


def linha(c: Cena, nome: str, runs: list[tuple[str, list[float], str]], size: int, cy: float, atraso: int) -> None:
    """Linha centralizada; trechos de cores diferentes viram camadas de texto lado a lado (todas editáveis)."""
    b = c.b
    h = round(size * 1.4)
    topo = cy - size * BASE_FOCO
    if len(runs) == 1:
        t, col, fonte = runs[0]
        lid = c.novo_id()
        b.text(lid, f"{nome}: {t}", c.start, SCENE, 0, topo, W, h, t, fonte, size, col, "center")
        sombra(b, lid)
        c.entra(lid, atraso, cy=topo + h / 2)
        return
    larg = [medida(f, size, t) for t, _, f in runs]
    larg[-1] = medida(runs[-1][2], size, runs[-1][0].rstrip(" "))
    x = W / 2 - sum(larg) / 2
    for (t, col, fonte), lw in zip(runs, larg):
        lead = len(t) - len(t.lstrip(" "))
        x0 = x + (medida(fonte, size, " " * lead) if lead else 0)
        txt = t.strip(" ")
        tw = medida(fonte, size, txt)
        lid = c.novo_id()
        b.text(lid, f"{nome}: {txt}", c.start, SCENE, x0, topo, tw + 160, h, txt, fonte, size, col, "left")
        sombra(b, lid)
        c.entra(lid, atraso, cy=topo + h / 2)
        x += lw


def titulo_grad(c: Cena, nome: str, texto: str, size: int, cy: float, atraso: int, fonte: str = "bold") -> None:
    """Título em degradê vermelho -> laranja -> âmbar numa única camada (sobreposição de degradê nativa)."""
    b = c.b
    h = round(size * 1.4)
    topo = cy - size * BASE_FOCO
    tw = medida(fonte, size, texto)
    lid = c.novo_id()
    b.text(lid, nome, c.start, SCENE, 0, topo, W, h, texto, fonte, size, WHITE, "center")
    esq = (W - tw) / 2
    estilo(b, lid, {"type": "gradientOverlay", "enabled": True, "opacity": 1, "gradientType": "linear", "start": [esq, 0], "end": [esq + tw, 0],
                    "blendMode": "normal", "stops": [{"offset": o, "color": col} for o, col in BRAND_STOPS]})
    sombra(b, lid, forte=True)
    c.entra(lid, atraso, cy=topo + h / 2)


def sublinhado(c: Cena, nome: str, cx: float, y: float, w: int, atraso: int) -> None:
    lid = c.novo_id()
    c.b.rect(lid, nome, c.start, SCENE, cx - w / 2, y, w, 6, RED, 3, gradient=grad(0, 0, w, 0, [(o, col) for o, col in BRAND_STOPS]))
    c.entra(lid, atraso, dy=0)
    c.b.anim.append(keys(lid, "scaleX", [(0, 0, LINEAR)] + ([(atraso, 0, LINEAR)] if atraso else []) + [(atraso + 650, 100, EASE_OUT)]))


def foto(c: Cena, nome: str, asset: str, w: int, h: int, cx: float, cy: float, zoom: float = 0.0, entrada: str = "fade", atraso: int = 0) -> int:
    lid = c.novo_id()
    c.photos.append({"type": "Image", "id": lid, "name": nome, "activeRange": {"start": c.start, "duration": SCENE},
                     "transform": tr(cx, cy, (w / 2, h / 2)), "source": {"assetId": asset, "fit": "contain"}})
    saida = [(SCENE - FADE_OUT, 100, LINEAR), (SCENE - 20, 0, LINEAR)]
    if entrada == "lado":
        pts = [(0, 0, LINEAR), (atraso, 0, LINEAR), (atraso + 340, 100, EASE_OUT)] + saida
        c.img_anim.append(keys(lid, "positionX", [(0, cx - 180, LINEAR), (atraso, cx - 180, LINEAR), (atraso + 640, cx, EASE_OUT)]))
    else:
        pts = ([(0, 100, LINEAR)] if c.idx == 0 else [(0, 0, LINEAR), (FADE_IN, 100, EASE_OUT)]) + saida
    c.img_anim.append(keys(lid, "opacity", pts))
    if zoom:
        for ax in ("scaleX", "scaleY"):
            c.img_anim.append(keys(lid, ax, [(0, 100, LINEAR), (SCENE, 100 + zoom, LINEAR)]))
    return lid


def logo(c: Cena, nome: str, asset: str, cx: float, cy: float, escala: float, atraso: int) -> None:
    iw, ih = Image.open(ASSETS / "logos" / f"{asset}.png").size
    lid = c.novo_id()
    c.logos.append({"type": "Image", "id": lid, "name": nome, "activeRange": {"start": c.start, "duration": SCENE},
                    "transform": tr(cx, cy, (iw / 2, ih / 2), escala), "source": {"assetId": asset, "fit": "contain"}})
    c.img_anim.append(keys(lid, "opacity", [(0, 0, LINEAR), (atraso, 0, LINEAR), (atraso + 320, 100, EASE_OUT),
                                          (SCENE - FADE_OUT, 100, LINEAR), (SCENE - 20, 0, LINEAR)]))


def suaviza_bordas(im: Image.Image, raio: int = 44, pena: int = 14) -> Image.Image:
    """Cantos arredondados com borda levemente esfumada (alfa) em vez de retângulo seco."""
    from PIL import ImageDraw
    w, h = im.size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((pena, pena, w - pena - 1, h - pena - 1), radius=raio, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(pena * 0.55))
    rgba = im.convert("RGBA")
    rgba.putalpha(m)
    return rgba


def prepara_fotos(story: bool) -> dict[str, tuple[str, int, int]]:
    """Recorta as fotos de cenário por formato e devolve {asset: (arquivo, w, h)}."""
    H = 1920 if story else 1080
    saida = {}

    def cobre(n: int, w: int, h: int, foco: float, nome: str, espelha: bool = False, desfoque: float = 0, suave: bool = False) -> None:
        im = Image.open(ASSETS / "fotos" / f"cenario-{n}.jpg").convert("RGB")
        if espelha:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        esc = max(w / im.width, h / im.height)
        r = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
        x, y = (r.width - w) // 2, round((r.height - h) * foco)
        pasta = ROOT / ".tesseract-work" / ("stories" if story else "feed")
        pasta.mkdir(parents=True, exist_ok=True)
        arq = pasta / f"{nome}.jpg"
        rec = r.crop((x, y, x + w, y + h))
        if desfoque:
            rec = rec.filter(ImageFilter.GaussianBlur(desfoque))
        if suave:
            rec = suaviza_bordas(rec)
            arq = arq.with_suffix(".png")
            rec.save(arq)
        else:
            rec.save(arq, quality=94)
        saida[nome] = (str(arq), w, h)

    cobre(0, 1080, 1140 if story else 1080, 0.0, "c1-foto")
    yc, bh_ = (905, 170) if story else (515, 124)       # eixo comum e altura da faixa laranja
    yfaixa = yc - bh_ / 2
    cobre(1, 1080, round(yc), 0.35, "c2-topo")                                # sangria total: do topo até o centro da faixa
    cobre(4, 1080, round(H - yc), 0.60, "c2-base")                            # do centro da faixa até a base (as fotos se encontram sem vão)
    cobre(4, 1080, H, 0.95, "c3-fundo", desfoque=3)
    cobre(1, 1080, H, 0.5, "c4-fundo", espelha=True, desfoque=3)
    cobre(2, 1080, H, 0.5, "c5-fundo", desfoque=5)
    return saida


def _suave(x, a, b):
    import numpy as np
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def ornamentos(story: bool) -> dict[str, tuple[str, int, int]]:
    """Risquinhos laranja nos quatro cantos (mesmo detalhe das peças B2B). O desvanecimento acontece em todas as bordas da imagem,
    então não há corte reto: as linhas morrem aos poucos em direção ao centro do quadro."""
    import numpy as np
    w, h = (350, 250) if story else (270, 180)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    fase = ((xx + yy) / np.sqrt(2)) % 15
    linhas = np.clip(1.5 - np.abs(fase - 7.5) * 0.9, 0, 1)
    u = xx / (w - 1)                     # 0 no canto, 1 na borda interna
    v = (h - 1 - yy) / (h - 1)           # 0 na borda inferior, 1 na borda superior
    desvanece = (1 - _suave(u, 0.08, 1.0)) * (1 - _suave(v, 0.08, 1.0))
    alfa = (linhas * desvanece * 0.92 * 255).astype(np.uint8)
    img = np.zeros((h, w, 4), dtype=np.uint8)
    img[..., 0], img[..., 1], img[..., 2], img[..., 3] = 255, 112, 20, alfa
    bl = Image.fromarray(img, "RGBA")                        # canto inferior esquerdo
    pasta = ROOT / ".tesseract-work" / ("stories" if story else "feed")
    pasta.mkdir(parents=True, exist_ok=True)
    saida = {}
    for nome, im in (("orn-bl", bl), ("orn-br", bl.transpose(Image.FLIP_LEFT_RIGHT)),
                     ("orn-tl", bl.transpose(Image.FLIP_TOP_BOTTOM)),
                     ("orn-tr", bl.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))):
        im.save(pasta / f"{nome}.png")
        saida[nome] = (str(pasta / f"{nome}.png"), w, h)
    return saida


def barra_progresso(b: Builder, H: int, story: bool) -> None:
    """Cinco segmentos no pé do quadro; o da carta atual enche durante a leitura (indica o carrossel)."""
    seg, gap = 118, 14
    x0 = W / 2 - (N * seg + (N - 1) * gap) / 2
    y = 1668 if story else H - 52
    for i in range(N):
        x = x0 + i * (seg + gap)
        b.rect(7000 + i, f"Progresso base {i+1}", 0, TOTAL, x, y, seg, 6, [1, 1, 1, 0.22], 3)
        fill = 7100 + i
        t0 = i * SCENE
        b.rect(fill, f"Progresso {i+1}", t0, TOTAL - t0, x, y, seg, 6, RED, 3, gradient=grad(0, 0, seg, 0, [(0, RED), (1, AMBER)]))
        b.front[-1]["transform"]["anchorPoint"] = [0, 3]
        b.front[-1]["transform"]["position"] = [x, y + 3]
        b.anim.append(keys(fill, "scaleX", [(0, 0, LINEAR), (SCENE, 100, LINEAR)]))
        b.anim.append(keys(fill, "opacity", [(0, 100, LINEAR), (TOTAL - t0 - 260, 100, LINEAR), (TOTAL - t0 - 20, 0, LINEAR)]))


def pill(c: Cena, nome: str, texto: str, cx: float, cy: float, size: int, atraso: int, fonte: str = "semibold") -> None:
    """Selo arredondado com contorno (mesmo recurso dos selos das peças B2B)."""
    tw = medida(fonte, size, texto)
    h = round(size * 1.9)
    w = round(tw + size * 1.8)
    rid = c.novo_id()
    c.b.rect(rid, f"Selo {nome}", c.start, SCENE, cx - w / 2, cy - h / 2, w, h, [1, 1, 1, 0.08], h / 2)
    estilo(c.b, rid, {"type": "stroke", "enabled": True, "color": [1, 1, 1, 0.6], "width": 3, "position": "inside", "blendMode": "normal"})
    c.entra(rid, atraso, dy=0)
    linha(c, f"Selo {nome} texto", [(texto, WHITE, fonte)], size, cy, atraso)


def monta(b: Builder, story: bool, fotos: dict) -> list[dict]:
    H = b.H
    P = (lambda s, f: s if story else f)      # (valor nos stories, valor no feed)
    cenas = [Cena(b, i) for i in range(N)]
    YC = P(905, 515)                          # eixo vertical comum a todos os blocos de texto
    b.rect(9000, "Fundo preto", 0, TOTAL, 0, 0, W, H, BLACK, front=False)

    # ---------- carta 1: valorize seu condomínio ----------
    c = cenas[0]
    ph = fotos["c1-foto"][2]
    foto(c, "Foto cenário 1 (esteiras)", "c1-foto", 1080, ph, 540, ph / 2, zoom=7)
    b.rect(c.novo_id(), "Degradê carta 1", c.start, SCENE, 0, 0, W, H, WHITE, 0,
           gradient=grad(0, P(380, 250), 0, P(1010, 760), [(0, [0.03, 0.03, 0.035, 0.32]), (1, [0.03, 0.03, 0.035, 1])]), front=False)
    c.dims.append(b.back.pop())
    # A abertura usa escala e eixo próprios: ocupa a área útil sem competir
    # com o símbolo no topo nem com a barra de progresso no rodapé.
    tam, passo = P(104, 90), P(132, 116)
    cy0 = P(1080, 600) - 1.5 * passo
    linha(c, "Linha 1", [("VALORIZE SEU", WHITE, "medium")], tam, cy0, 200)
    linha(c, "Linha 2", [("CONDOMÍNIO", ORANGE, "bold"), (" COM", WHITE, "medium")], tam, cy0 + passo, 380)
    linha(c, "Linha 3", [("UMA ", WHITE, "medium"), ("ACADEMIA", ORANGE, "bold")], tam, cy0 + passo * 2, 560)
    linha(c, "Linha 4", [("DE VERDADE", WHITE, "medium")], tam, cy0 + passo * 3, 740)

    # ---------- carta 2: compre ou alugue ----------
    c = cenas[1]
    ft, fb = fotos["c2-topo"], fotos["c2-base"]
    bh = P(170, 124)
    yb = YC - bh / 2                          # a faixa fica no eixo comum
    foto(c, "Foto cenário 2a (sala de bikes)", "c2-topo", ft[1], ft[2], 540, ft[2] / 2, zoom=5)
    foto(c, "Foto cenário 2b (spinning)", "c2-base", fb[1], fb[2], 540, YC + fb[2] / 2, zoom=5)
    b.rect(c.novo_id(), "Escurecer carta 2", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=26, front=False)
    c.dims.append(b.back.pop())
    b.rect(c.novo_id(), "Trilho escuro da faixa", c.start, SCENE, 0, yb, W, bh, BLACK, 0, opacity=58, front=False)   # a emenda das fotos nunca aparece seca
    c.dims.append(b.back.pop())
    transicao = P(260, 170)                    # degradê escuro que nasce da faixa, para a emenda não ficar seca
    b.rect(c.novo_id(), "Degradê acima da faixa", c.start, SCENE, 0, yb - transicao, W, transicao, WHITE, 0,
           gradient=grad(0, 0, 0, transicao, [(0, [0.02, 0.02, 0.025, 0]), (0.5, [0.02, 0.02, 0.025, 0.22]), (1, [0.02, 0.02, 0.025, 0.55])]), front=False)
    c.dims.append(b.back.pop())
    b.rect(c.novo_id(), "Degradê abaixo da faixa", c.start, SCENE, 0, yb + bh, W, transicao, WHITE, 0,
           gradient=grad(0, 0, 0, transicao, [(0, [0.02, 0.02, 0.025, 0.55]), (0.5, [0.02, 0.02, 0.025, 0.22]), (1, [0.02, 0.02, 0.025, 0])]), front=False)
    c.dims.append(b.back.pop())
    faixa = c.novo_id()
    b.rect(faixa, "Faixa laranja", c.start, SCENE, 0, yb, W, bh, RED, 0, gradient=grad(0, 0, W, 0, [(0, RED), (0.62, ORANGE), (1, AMBER)]))
    sombra(b, faixa, forte=True)
    b.anim += [keys(faixa, "positionX", [(0, -W / 2, LINEAR), (300, -W / 2, LINEAR), (940, W / 2, EASE_OUT)]),
               keys(faixa, "opacity", [(0, 100, LINEAR), (SCENE - FADE_OUT, 100, LINEAR), (SCENE - 20, 0, LINEAR)])]
    brilho = c.novo_id()      # brilho que cruza a faixa depois de entrar
    b.rect(brilho, "Brilho da faixa", c.start, SCENE, -140, yb, 140, bh, WHITE, 0,
           gradient=grad(0, 0, 140, 0, [(0, [1, 1, 1, 0]), (0.5, [1, 1, 1, 0.34]), (1, [1, 1, 1, 0])]))
    b.anim.append(keys(brilho, "positionX", [(0, -70, LINEAR), (1100, -70, LINEAR), (1900, W + 70, EASE_INOUT)]))
    b.anim.append(keys(brilho, "opacity", [(0, 0, LINEAR), (1090, 0, LINEAR), (1110, 100, LINEAR), (1880, 100, LINEAR), (1900, 0, LINEAR)]))
    linha(c, "Compre ou alugue", [("COMPRE OU ALUGUE", WHITE, "bold")], P(76, 62), yb + bh / 2, 720)

    # ---------- carta 3: marcas líderes ----------
    c = cenas[2]
    foto(c, "Foto cenário 3 (fundo)", "c3-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Escurecer carta 3", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=78, front=False)
    c.dims.append(b.back.pop())
    K = P(1.0, 0.8)
    r3 = lambda y: YC + (y - 976) * K          # y original (stories) -> relativo ao centro do bloco
    linha(c, "Título 1", [("Equipamentos fitness com", WHITE, "medium")], P(56, 48), r3(590), 140)
    titulo_grad(c, "MARCAS LÍDERES", "MARCAS LÍDERES", P(98, 86), r3(693), 300)
    sublinhado(c, "Linha sob título", 540, r3(693) + P(66, 58), 360, 700)
    es = P(115, 105)
    esquerda = [("speedo-fitness", 333, 901), ("tauka", 321, 1125), ("leforz", 331, 1343)]
    direita = [("mormaii", 832, 829), ("schwinn", 832, 935), ("waterrower", 832, 1041), ("nohrd", 832, 1150),
               ("bowflex", 832, 1259), ("bodybike", 832, 1362)]
    for k, (nome, x, y) in enumerate(esquerda):
        logo(c, f"Logo {nome}", nome, x, r3(y), es, 780 + k * 150)
    for k, (nome, x, y) in enumerate(direita):
        logo(c, f"Logo {nome}", nome, x, r3(y), es, 840 + k * 130)

    # ---------- carta 4 (B: selos como nas peças B2B) ----------
    c = cenas[3]
    foto(c, "Foto cenário 4 (fundo)", "c4-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Escurecer carta 4", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=66, front=False)
    c.dims.append(b.back.pop())
    logo(c, "Ícone parcelamento", "icone-parcelamento", 540, 585, 130, 180)
    titulo_grad(c, "PARCELAMENTO", "PARCELAMENTO", 112, 770, 380)
    titulo_grad(c, "FACILITADO", "FACILITADO", 112, 885, 640)
    sublinhado(c, "Linha sob título", 540, 955, 320, 1000)
    linha(c, "Sub 1", [("em equipamentos inovadores", WHITE, "medium")], 62, 1035, 1100)
    linha(c, "Sub 2", [("e resistentes", WHITE, "medium")], 62, 1110, 1300)
    pill(c, "suporte", "Suporte técnico exclusivo", 540, 1235, 44, 1500)
    pill(c, "atendimento", "Atendimento especializado", 540, 1340, 44, 1700)

    # ---------- carta 5 (B) ----------
    c = cenas[4]
    foto(c, "Foto cenário 5 (fundo)", "c5-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Escurecer carta 5", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=70, front=False)
    c.dims.append(b.back.pop())
    linha(c, "Solicite seu", [("SOLICITE SEU", WHITE, "medium")], 100, 665, 320)
    titulo_grad(c, "ORÇAMENTO", "ORÇAMENTO", 116, 785, 560)
    pill(c, "consultoria", "Consultoria gratuita", 540, 960, 46, 900)
    pill(c, "projeto", "Projeto personalizado", 540, 1070, 46, 1100)
    by = 1235
    bw, bh2 = 470, 96
    borda = c.novo_id()
    b.rect(borda, "Botão borda", c.start, SCENE, 540 - bw / 2 - 3, by - bh2 / 2 - 3, bw + 6, bh2 + 6, RED, 52, gradient=grad(0, 0, bw, 0, [(0, RED), (1, AMBER)]))
    miolo = c.novo_id()
    b.rect(miolo, "Botão miolo", c.start, SCENE, 540 - bw / 2, by - bh2 / 2, bw, bh2, BLACK, 48)
    for lid in (borda, miolo):
        b.anim.append(keys(lid, "opacity", [(0, 0, LINEAR), (1450, 0, LINEAR), (1530, 100, LINEAR), (SCENE - FADE_OUT, 100, LINEAR), (SCENE - 20, 0, LINEAR)]))
        for ax in ("scaleX", "scaleY"):
            b.anim.append(keys(lid, ax, [(0, 84, LINEAR), (1450, 84, LINEAR), (1900, 100, EASE_OUT), (2300, 104, EASE_INOUT), (2700, 100, EASE_INOUT), (3100, 104, EASE_INOUT)]))
    linha(c, "Clique abaixo", [("CLIQUE ABAIXO", WHITE, "medium")], 42, by, 1550)

    barra_progresso(b, H, story)

    imgs, anim, dims = [], [], []
    for c in reversed(cenas):          # cartas mais novas ficam à frente; em cada carta: logos, fotos
        imgs += c.logos + c.photos
        anim += c.img_anim
        dims += [(d, c.photos[0]["id"]) for d in c.dims]
    b.anim += anim
    b.dim_acts = dims
    return imgs


def build(fmt: str) -> Path:
    height, tag = FORMATS[fmt]
    story = height > 1080
    work = ROOT / ".tesseract-work" / tag
    work.mkdir(parents=True, exist_ok=True)
    (ROOT / "projeto").mkdir(exist_ok=True)
    proj = ROOT / "projeto" / f"{tag}.tsrct"
    proj.unlink(missing_ok=True)
    project = str(proj)
    _estilo_id[0] = 500
    run("project", "create", "--project", project)
    fonts = {}
    for key, f in FONT_FILES.items():
        r = json.loads(run("project", "import-font", "--project", project, "--file", str(BRAND / "fonts" / f"{f}.ttf")).strip().splitlines()[-1])
        face = r["faces"][0]
        fonts[key] = (face.get("typographicFamilyName") or r["fontFamily"], face.get("typographicStyleName") or r["fontStyle"])
    fotos = prepara_fotos(story)
    for nome, (arq, _, _) in fotos.items():
        run("project", "import-asset", "--project", project, "--file", arq, "--asset-id", nome, "--kind", "image")
    for arq in sorted((ASSETS / "logos").glob("*.png")):
        run("project", "import-asset", "--project", project, "--file", str(arq), "--asset-id", arq.stem, "--kind", "image")
    orn = ornamentos(story)
    for nome, (arq, _, _) in orn.items():
        run("project", "import-asset", "--project", project, "--file", arq, "--asset-id", nome, "--kind", "image")
    b = Builder(height, fonts)
    imgs = monta(b, story, fotos)
    ow, oh = orn["orn-bl"][1], orn["orn-bl"][2]
    simb_w, simb_h = Image.open(ASSETS / "logos" / "cdf-simbolo.png").size
    esc = 21 if story else 16
    frente_img = [
        {"type": "Image", "id": 7901, "name": "Risquinhos inferior esquerdo", "activeRange": {"start": 0, "duration": TOTAL},
         "transform": tr(ow / 2, height - oh / 2, (ow / 2, oh / 2)), "source": {"assetId": "orn-bl", "fit": "contain"}},
        {"type": "Image", "id": 7902, "name": "Risquinhos inferior direito", "activeRange": {"start": 0, "duration": TOTAL},
         "transform": tr(W - ow / 2, height - oh / 2, (ow / 2, oh / 2)), "source": {"assetId": "orn-br", "fit": "contain"}},
        {"type": "Image", "id": 7903, "name": "Risquinhos superior esquerdo", "activeRange": {"start": 0, "duration": TOTAL},
         "transform": tr(ow / 2, oh / 2, (ow / 2, oh / 2)), "source": {"assetId": "orn-tl", "fit": "contain"}},
        {"type": "Image", "id": 7904, "name": "Risquinhos superior direito", "activeRange": {"start": 0, "duration": TOTAL},
         "transform": tr(W - ow / 2, oh / 2, (ow / 2, oh / 2)), "source": {"assetId": "orn-tr", "fit": "contain"}},
    ]
    imgs = frente_img + imgs
    # degradês escuros suaves (curva em várias paradas, sem borda visível) no topo e na base
    k = [0.0, 0.05, 0.18, 0.40, 0.68, 0.92]
    b.dim_global = []
    for lid, nome, y0, gh, inverte in ((7800, "Degradê escuro do rodapé", height - (720 if story else 400), 720 if story else 400, False),
                                       (7801, "Degradê escuro do topo", 0, 520 if story else 290, True)):
        vals = k[::-1] if inverte else k
        paradas = [(i / (len(k) - 1), [0.025, 0.025, 0.03, vals[i]]) for i in range(len(k))]
        b.rect(lid, nome, 0, TOTAL, 0, y0, W, gh, WHITE, 0, gradient=grad(0, 0, 0, gh, paradas), front=False)
        b.dim_global.append(b.back.pop())
    # vinheta lateral: bordas esquerda e direita escurecem aos poucos
    lw = 190
    for lid, nome, x0, de in ((7802, "Vinheta lateral esquerda", 0, 0.62), (7803, "Vinheta lateral direita", W - lw, 0.0)):
        stops = [(0, [0.02, 0.02, 0.025, 0.62]), (0.4, [0.02, 0.02, 0.025, 0.22]), (1, [0.02, 0.02, 0.025, 0])]
        if lid == 7803:
            stops = [(0, [0.02, 0.02, 0.025, 0]), (0.6, [0.02, 0.02, 0.025, 0.22]), (1, [0.02, 0.02, 0.025, 0.62])]
        b.rect(lid, nome, 0, TOTAL, x0, 0, lw, height, WHITE, 0, gradient=grad(0, 0, lw, 0, stops), front=False)
        b.dim_global.append(b.back.pop())
    editable = work / "editable.json"
    run("project", "checkout", "--project", project, "--output", str(editable))
    doc = json.loads(editable.read_text(encoding="utf-8"))
    doc["dimensions"] = {"width": W, "height": height}
    doc["duration"] = TOTAL / 1000
    doc["composition"]["layers"] = imgs
    ids = [l["id"] for l in imgs] + [a["layerId"] for a in b.back + b.front]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise SystemExit(f"IDs duplicados: {dup}")
    editable.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "commit", "--project", project, "--file", str(editable))
    ordem = [l["id"] for l in imgs]
    # escurecimentos: logo acima da foto da própria carta (abaixo dos logos), do maior índice para o menor
    dims = sorted(((ordem.index(pid), a) for a, pid in b.dim_acts), key=lambda t: -t[0])
    acts = [{**a, "insertIndex": i} for i, a in dims]
    acts += [{**g, "insertIndex": len(frente_img)} for g in b.dim_global]
    acts += [a for a in b.back if a["layerId"] != 9000] + [a for a in b.back if a["layerId"] == 9000]
    acts += [{**a, "insertIndex": 0} for a in b.front] + b.anim
    (work / "edits.json").write_text(json.dumps(acts, ensure_ascii=False, indent=1), encoding="utf-8")
    run("project", "apply", "--project", project, "--actions", str(work / "edits.json"))
    return proj


def render(fmt: str, proj: Path, preview_only: bool) -> None:
    height, tag = FORMATS[fmt]
    (ROOT / "previews").mkdir(exist_ok=True)
    stamps = []
    for k in range(N):
        s = k * SCENE
        stamps += [s + 240, s + 700, s + 1500, s + 2900]
    tile = ("270", "270") if fmt == "feed" else ("216", "384")
    run("filmstrip", "--project", str(proj), "--timestamps-ms", *[str(t) for t in stamps], "--tile-width", tile[0], "--tile-height", tile[1],
        "--items-per-row", "8", "--output", str(ROOT / "previews" / f"filmstrip_{tag}_v{VERSAO:02d}.png"))
    if preview_only:
        return
    mp4 = ROOT / f"{SLUG}_{tag}_v{VERSAO:02d}.mp4"
    grande = ROOT / ".tesseract-work" / tag / "export_4k.mp4"
    run("export", "--project", str(proj), "--resolution", "4k", "--fps", "60", "--output", str(grande))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(grande), "-vf", f"scale={W}:{height}:flags=lanczos", "-c:v", "libx264",
                    "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--formato", choices=list(FORMATS), action="append")
    ap.add_argument("--preview-only", action="store_true")
    a = ap.parse_args()
    for fmt in a.formato or list(FORMATS):
        p = build(fmt)
        render(fmt, p, a.preview_only)
        print(f"{fmt}: ok")


if __name__ == "__main__":
    main()
