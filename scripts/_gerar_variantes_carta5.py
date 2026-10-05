"""Variantes D/E/F só da carta 5, na mesma linguagem da carta 4 (variante B). Só teste."""
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
ICONE = AQUI.parent / "assets" / "carrossel-pinheiros" / "logos" / "icone-orcamento.png"


def desenha_icone() -> None:
    s = 4
    im = Image.new("RGBA", (192 * s, 192 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = (255, 255, 255, 255)
    d.rounded_rectangle((34 * s, 28 * s, 158 * s, 184 * s), 16 * s, fill=w)
    d.rounded_rectangle((66 * s, 12 * s, 126 * s, 44 * s), 10 * s, fill=w, outline=(0, 0, 0, 0))
    d.rounded_rectangle((76 * s, 20 * s, 116 * s, 36 * s), 6 * s, fill=(0, 0, 0, 0))
    for y in (78, 110, 142):
        d.rounded_rectangle((54 * s, (y - 6) * s, 72 * s, (y + 6) * s), 3 * s, fill=(0, 0, 0, 0))
        d.rounded_rectangle((82 * s, (y - 5) * s, 138 * s, (y + 5) * s), 5 * s, fill=(0, 0, 0, 0))
    im.resize((192, 192), Image.LANCZOS).save(ICONE)


BTN = '''    by = {by}
    bw, bh2 = {bw}, {bh}
    borda = c.novo_id()
    b.rect(borda, "Botão borda", c.start, SCENE, 540 - bw / 2 - 3, by - bh2 / 2 - 3, bw + 6, bh2 + 6, RED, 52, gradient=grad(0, 0, bw, 0, [(0, RED), (1, AMBER)]))
    miolo = c.novo_id()
    b.rect(miolo, "Botão miolo", c.start, SCENE, 540 - bw / 2, by - bh2 / 2, bw, bh2, {fill}, 48)
    for lid in (borda, miolo):
        b.anim.append(keys(lid, "opacity", [(0, 0, LINEAR), (1450, 0, LINEAR), (1530, 100, LINEAR), (SCENE - FADE_OUT, 100, LINEAR), (SCENE - 20, 0, LINEAR)]))
        for ax in ("scaleX", "scaleY"):
            b.anim.append(keys(lid, ax, [(0, 84, LINEAR), (1450, 84, LINEAR), (1900, 100, EASE_OUT), (2300, 104, EASE_INOUT), (2700, 100, EASE_INOUT), (3100, 104, EASE_INOUT)]))
    linha(c, "Clique abaixo", [("CLIQUE ABAIXO", WHITE, "medium")], {fs}, by, 1550)

'''
HEAD = '''    # ---------- carta 5 ({n}) ----------
    c = cenas[4]
    foto(c, "Foto cenário 5 (fundo)", "c5-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Escurecer carta 5", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=66, front=False)
    c.dims.append(b.back.pop())
'''
D = HEAD.format(n="D") + '''    logo(c, "Ícone orçamento", "icone-orcamento", 540, 585, 130, 180)
    titulo_grad(c, "SOLICITE SEU", "SOLICITE SEU", 112, 770, 320)
    titulo_grad(c, "ORÇAMENTO", "ORÇAMENTO", 112, 885, 560)
    sublinhado(c, "Linha sob título", 540, 955, 320, 900)
    linha(c, "Sub 1", [("com consultoria gratuita", WHITE, "medium")], 62, 1035, 1000)
    linha(c, "Sub 2", [("e projeto personalizado", WHITE, "medium")], 62, 1110, 1150)
''' + BTN.format(by=1290, bw=520, bh=104, fill="BLACK", fs=44)
E = HEAD.format(n="E") + '''    logo(c, "Ícone orçamento", "icone-orcamento", 540, 585, 130, 180)
    titulo_grad(c, "SOLICITE SEU", "SOLICITE SEU", 112, 770, 320)
    titulo_grad(c, "ORÇAMENTO", "ORÇAMENTO", 112, 885, 560)
    sublinhado(c, "Linha sob título", 540, 955, 320, 900)
    pill(c, "consultoria", "Consultoria gratuita", 540, 1050, 48, 1000)
    pill(c, "projeto", "Projeto personalizado", 540, 1160, 48, 1200)
''' + BTN.format(by=1330, bw=520, bh=104, fill="BLACK", fs=44)
F = HEAD.format(n="F") + '''    logo(c, "Ícone orçamento", "icone-orcamento", 540, 560, 130, 180)
    linha(c, "Solicite seu", [("SOLICITE SEU", WHITE, "medium")], 92, 735, 320)
    titulo_grad(c, "ORÇAMENTO", "ORÇAMENTO", 128, 865, 560)
    sublinhado(c, "Linha sob título", 540, 950, 360, 900)
    linha(c, "Sub 1", [("com consultoria gratuita", WHITE, "medium")], 62, 1035, 1000)
    linha(c, "Sub 2", [("e projeto personalizado", WHITE, "medium")], 62, 1110, 1150)
    pill(c, "cta", "CLIQUE ABAIXO", 540, 1290, 52, 1500, "bold")

'''
desenha_icone()
BASE = (AQUI / "_prop_var_B.py").read_text(encoding="utf-8")
for nome, sec in (("D", D), ("E", E), ("F", F)):
    s = BASE
    a = s.index("    # ---------- carta 5 (B) ----------")
    z = s.index("    barra_progresso(b, H, story)")
    s = s[:a] + sec + s[z:]
    s = s.replace('"outputs" / "_proposta_B"', f'"outputs" / "_proposta_{nome}"')
    (AQUI / f"_prop_var_{nome}.py").write_text(s, encoding="utf-8")
    print("gerado", nome)
