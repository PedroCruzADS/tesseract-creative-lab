# Notas — v03 (2026-09-23)

## Revisão comercial e motion — 23/09/2026
- Entrega atual somente MP4, sem conversão para GIF. GIFs anteriores foram preservados apenas no backup `.tesseract-work/backup_pre_depor_20260923/`.
- Validade de preços até 30/09/2026 informada pelo usuário; prazo não encontrado nas páginas consultadas. Antes da veiculação, confirmar se valores permanecem válidos. Evidência em `validacao_comercial_20260923.md`.
- Incluídos `de` e `por` nos três produtos que têm preço anterior publicado. TR7 não tem `de`: exibe apenas o preço atual, sem inventar desconto.
- Mantido o parcelamento como argumento principal e o PIX como alternativa secundária. Valores do snapshot conferidos com páginas/listagens oficiais; consulta direta em tempo real ao site bloqueada por Cloudflare, conforme evidência.
- Eliminada deriva lateral do produto durante o zoom: centro x=540 constante no período de leitura, aumento discreto de 2% ancorado no centro; deslocamento lateral apenas na transição de saída.
- Preview, filmstrip e frames integrais de feed/stories revisados antes do export.

## Revisão de área segura e hierarquia (23/09/2026)
- Pedido do usuário: em Meta 9:16, reservar 250 px no topo e no rodapé contra overlays de perfil e CTA. No canvas 1080×1920, todo conteúdo essencial ficou entre y=250 e y=1670; fundo/textura podem ultrapassar. No feed 4:5, mantidas margens próprias do formato.
- Parcelamento permanece a oferta principal. A faixa vermelha horizontal do PIX foi trocada por linha secundária com acento vermelho curto, preservando o valor e a condição comercial.
- Stories teve logo, card, produto, oferta e aviso legal redistribuídos para a nova área útil; feed recebeu apenas o tratamento PIX.
- Preview/filmstrip e frame integral de produto conferidos antes do render final. MP4/GIF v03 reexportados; backup anterior em `.tesseract-work/backup_pre_safezone_pix_20260923/`.
- Repertório externo triado e regra reutilizável em `docs/COMPOSITION-QA.md`. Preços/condições continuam baseados no snapshot de 23/09/2026; revalidar antes de veicular.

## Refinamento Codex na própria v03 (23/09/2026)
- Direção visual, copy, quatro produtos, oferta e ritmo da versão Opus preservados.
- Card e imagem redistribuídos por formato; stories passou a aproveitar mais altura útil.
- Nome, condição, preço e PIX alinhados numa grade estável entre os produtos, inclusive quando não há preço anterior.
- Faixa PIX alinhada à largura do card; abertura e encerramento rebalanceados; aviso legal afastado das bordas do feed e de stories.
- Prévia e filmstrip revisados antes da exportação. MP4 final: feed 1080×1350 e stories 1080×1920, ambos 30 fps/10 s/300 frames. GIFs reexportados da mesma master.
- Backup recuperável da v03 anterior em `.tesseract-work/backup_pre_codex_20260923/`. Critérios gerais documentados em `docs/COMPOSITION-QA.md`.

## Mudanças vs v02 (pedido: mais lento, 10 s, ajustes finos)
- Duração 6,5 s -> 10 s: gancho 1,5 s, cada produto 1,8 s, card final 1,3 s.
- Saída de cada produto: desliza para a esquerda + fade (antes era corte seco); textos saem juntos.
- Gancho sai com fade em vez de cortar.
- 1º produto espera 320 ms o card branco chegar (antes a foto aparecia fora do card).
- Leve zoom contínuo (104%) enquanto o produto está parado; rodapé legal 22 -> 25 px; pulso do CTA mais longo.

Reproduzir: python scripts/build_cdf_mix.py (regrava a atual) | --nova-versao (arquiva e cria a próxima). Esta versão foi gerada por build_snapshot.py.

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

- GIF: ffmpeg fps=15, largura 720, paleta 256 cores, a partir do Project.mp4.
