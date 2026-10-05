# Notas — v02 (2026-09-23)

## Mudanças vs v01
- Fundo preto com faixa diagonal vermelha e textura do símbolo da marca (7%); produto em card branco arredondado.
- Logo oficial no topo e no card final. Tipografia da marca (Bai Jamjuree Bold/SemiBold/Medium).
- Preço: "de" riscado (quando existe), 18x sem juros em destaque, pill vermelha com valor no PIX.
- Selo "FRETE GRÁTIS*" + nota de rodapé só nos itens acima de R$ 10 mil (Esteira TR7 e Estação Multi 3).
- Card final: benefícios, CTA "COMPRE AGORA" com pulso, URL.

## Fontes de verdade (offer.json)
- Preços/parcelas/PIX: API de catálogo do site em 23/09/2026 ~10:25, conferidos contra o Merchant Center (batem).
- Frete grátis > R$ 10 mil: banner do site + política configurada no Merchant Center.
- Nenhum % de desconto calculado; só valores publicados.

## Conflitos / decisões
- Banner do site diz "5% OFF no PIX ou boleto", mas o checkout não dá desconto no boleto -> peça cita só PIX.
- Recorte automático do fundo branco falhou (fundo preso dentro da estrutura dos aparelhos) -> produto mantido em card branco, foto 100% original.
- Logo branco = SVG oficial com preenchimento trocado para branco (versão monocromática, sem redesenho).

## Validade
- Preços mudam: rodapé "Preços válidos em 23/09/2026". Refazer snapshot antes de subir se passar da data.

## Reproduzir
- python scripts/build_cdf_mix_v02.py feed|stories (cria nova pasta; não sobrescreve).
- GIF: ffmpeg fps=15, largura 720, paleta 256 cores, a partir do Project.mp4.
