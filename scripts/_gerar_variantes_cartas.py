"""Gera 3 variantes de teste (A, B, C) das cartas 4 e 5 do carrossel (stories) a partir de _proposta_carrossel.py. Não toca nos arquivos finais."""
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BASE = (AQUI / "_proposta_carrossel.py").read_text(encoding="utf-8")

PILL = '''
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


def monta('''

A = '''    # ---------- carta 4 (A: foto mais presente, bloco maior) ----------
    c = cenas[3]
    foto(c, "Foto cenário 4 (fundo)", "c4-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Escurecer carta 4", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=44, front=False)
    c.dims.append(b.back.pop())
    logo(c, "Ícone parcelamento", "icone-parcelamento", 540, 600, 150, 180)
    titulo_grad(c, "PARCELAMENTO", "PARCELAMENTO", 118, 800, 380)
    titulo_grad(c, "FACILITADO", "FACILITADO", 118, 920, 640)
    sublinhado(c, "Linha sob título", 540, 995, 340, 1000)
    linha(c, "Sub 1", [("em equipamentos inovadores", WHITE, "medium")], 66, 1090, 1100)
    linha(c, "Sub 2", [("e resistentes", WHITE, "medium")], 66, 1170, 1300)

    # ---------- carta 5 (A) ----------
    c = cenas[4]
    foto(c, "Foto cenário 5 (fundo)", "c5-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Escurecer carta 5", c.start, SCENE, 0, 0, W, H, BLACK, 0, opacity=46, front=False)
    c.dims.append(b.back.pop())
    linha(c, "Solicite seu", [("SOLICITE SEU", WHITE, "medium")], 104, 690, 320)
    titulo_grad(c, "ORÇAMENTO", "ORÇAMENTO", 120, 815, 560)
    linha(c, "Sub 1", [("com consultoria gratuita", WHITE, "medium")], 66, 960, 900)
    linha(c, "Sub 2", [("e projeto personalizado", WHITE, "medium")], 66, 1040, 1080)
    by = 1200
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

'''

B = '''    # ---------- carta 4 (B: selos como nas peças B2B) ----------
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

'''

C = '''    # ---------- carta 4 (C: foto em cima, texto embaixo, como a carta 1) ----------
    c = cenas[3]
    foto(c, "Foto cenário 4 (fundo)", "c4-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Degradê carta 4", c.start, SCENE, 0, 0, W, H, WHITE, 0,
           gradient=grad(0, 760, 0, 1250, [(0, [0.03, 0.03, 0.035, 0.0]), (1, [0.03, 0.03, 0.035, 0.97])]), front=False)
    c.dims.append(b.back.pop())
    logo(c, "Ícone parcelamento", "icone-parcelamento", 540, 1015, 125, 180)
    titulo_grad(c, "PARCELAMENTO", "PARCELAMENTO", 112, 1185, 380)
    titulo_grad(c, "FACILITADO", "FACILITADO", 112, 1300, 640)
    sublinhado(c, "Linha sob título", 540, 1370, 320, 1000)
    linha(c, "Sub 1", [("em equipamentos inovadores", WHITE, "medium")], 62, 1450, 1100)
    linha(c, "Sub 2", [("e resistentes", WHITE, "medium")], 62, 1525, 1300)

    # ---------- carta 5 (C) ----------
    c = cenas[4]
    foto(c, "Foto cenário 5 (fundo)", "c5-fundo", 1080, H, 540, H / 2, zoom=7)
    b.rect(c.novo_id(), "Degradê carta 5", c.start, SCENE, 0, 0, W, H, WHITE, 0,
           gradient=grad(0, 700, 0, 1180, [(0, [0.03, 0.03, 0.035, 0.0]), (1, [0.03, 0.03, 0.035, 0.97])]), front=False)
    c.dims.append(b.back.pop())
    linha(c, "Solicite seu", [("SOLICITE SEU", WHITE, "medium")], 100, 1060, 320)
    titulo_grad(c, "ORÇAMENTO", "ORÇAMENTO", 116, 1180, 560)
    linha(c, "Sub 1", [("com consultoria gratuita", WHITE, "medium")], 62, 1305, 900)
    linha(c, "Sub 2", [("e projeto personalizado", WHITE, "medium")], 62, 1380, 1080)
    by = 1500
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

'''

DESFOQUE = {"A": (1.5, 3), "B": (3, 5), "C": (0, 1.5)}
for nome, secao in (("A", A), ("B", B), ("C", C)):
    s = BASE
    a = s.index("    # ---------- carta 4: parcelamento facilitado ----------")
    b = s.index("    barra_progresso(b, H, story)")
    s = s[:a] + secao + s[b:]
    s = s.replace("\ndef monta(", PILL, 1)
    s = s.replace('ROOT = LAB / "outputs" / "_proposta_carrossel"', f'ROOT = LAB / "outputs" / "_proposta_{nome}"')
    d4, d5 = DESFOQUE[nome]
    s = re.sub(r'(cobre\(1, 1080, H, 0\.5, "c4-fundo", espelha=True, desfoque=)[\d.]+', rf"\g<1>{d4}", s)
    s = re.sub(r'(cobre\(2, 1080, H, 0\.5, "c5-fundo", desfoque=)[\d.]+', rf"\g<1>{d5}", s)
    (AQUI / f"_prop_var_{nome}.py").write_text(s, encoding="utf-8")
    print("gerado", nome)
