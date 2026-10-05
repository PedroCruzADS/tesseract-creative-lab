import re
from pathlib import Path
A = Path(__file__).resolve().parent
s = (A / "_prop_var_E.py").read_text(encoding="utf-8")
s = s.replace('"outputs" / "_proposta_E"', '"outputs" / "carrossel-pinheiros-cenarios"')
a = s.index("    # ---------- carta 4 (B: selos")
z = s.index("    barra_progresso(b, H, story)")
sec = s[a:z]
# cota vertical: stories mantém o valor aprovado; feed comprime em torno do eixo
sec = sec.replace("(B: selos como nas peças B2B)", "(selos como nas peças B2B)").replace("carta 5 (E)", "carta 5")
def fy(m):  # y absoluto -> Y(y)
    return f"Y({m.group(1)})"
# linhas com (..., size, y, atraso): reescreve explicitamente
sec = re.sub(r'titulo_grad\(c, ("[^"]+"), ("[^"]+"), 112, (\d+), (\d+)\)', r'titulo_grad(c, \1, \2, P(112, 95), Y(\3), \4)', sec)
sec = re.sub(r'logo\(c, ("[^"]+"), ("[^"]+"), 540, 585, (\d+), 180\)', lambda m: f'logo(c, {m.group(1)}, {m.group(2)}, 540, Y(585), P({m.group(3)}, {round(int(m.group(3))*0.85)}), 180)', sec)
sec = re.sub(r'sublinhado\(c, "Linha sob título", 540, (\d+), 320, (\d+)\)', r'sublinhado(c, "Linha sob título", 540, Y(\1), P(320, 272), \2)', sec)
sec = re.sub(r'(linha\(c, "Sub \d", \[\([^)]*\)\], )62, (\d+), (\d+)\)', r'\1P(62, 53), Y(\2), \3)', sec)
sec = re.sub(r'pill\(c, ("[^"]+"), ("[^"]+"), 540, (\d+), (\d+), (\d+)\)', r'pill(c, \1, \2, 540, Y(\3), P(\4, \4 - 8), \5)', sec)
sec = sec.replace("by = 1330", "by = Y(1330)").replace("bw, bh2 = 520, 104", "bw, bh2 = P(520, 440), P(104, 88)")
sec = sec.replace('[("CLIQUE ABAIXO", WHITE, "medium")], 44, by', '[("CLIQUE ABAIXO", WHITE, "medium")], P(44, 38), by')
head = "    Y = lambda y: y if story else YC + (y - 951) * 0.8   # stories: eixo aprovado; feed: bloco comprimido em torno do eixo\n"
s = s[:a] + head + sec + s[z:]
(A / "build_carrossel_pinheiros.py").write_text(s, encoding="utf-8")
