# Notas — v01 (2026-09-23)

## Estrutura
- Projeto: Project.tsrct (Tesseract 0.2.0), canvas 1080x1080, 5 s.
- 4 camadas Image (ids 11-14) em cortes secos de 1250 ms, punch-in de escala 110% -> 100% (easing out, 450 ms) e leve recuo ate 98%.
- Faixa inferior escura (id 2), fundo branco (id 1), texto "CASA DO FITNESS" (id 3), nomes dos produtos (ids 21-24) com subida de 17 px em 300 ms.
- Fonte: Anton Regular (Google Fonts, OFL - fonts/OFL.txt), embutida no .tsrct.
- Montagem reproduzivel: .tesseract-work/build.py.

## Decisoes
- v01a tinha fade de opacidade: 1o frame ficava todo branco (ruim para miniatura de GIF). Trocado por corte seco.
- Punch-in reduzido de 114% para 110%: base da estacao quase tocava a faixa.

## Fontes de verdade
- Imagens e titulos: Merchant Center CDF, offer.json. Nomes encurtados para marca + modelo, sem alterar o fato.

## Limitacoes
- Sem logo oficial em assets/ -> marca escrita em texto, logo nao recriado.
- Tesseract exporta so MP4/ProRes; GIF convertido do MP4 final via ffmpeg (fps=15, scale 600, paleta 192 cores).
- Sem musica/som (GIF e mudo).
