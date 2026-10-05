# Notas — filme v05

- Solicitação: clique de 1 s antes da cena atual, sem aceleração exagerada; órbita redesenhada, com alinhamento rigoroso dos produtos novos e antigos.
- Causa corrigida: v04 dividia por dois a âncora já expressa em meia largura/altura, deslocando imagem e logo. V05 usa as dimensões reais de cada asset oficial e verifica seu encaixe no card.
- Cards agora têm 236×234 px, área de imagem, acento e label internos. Anel com raio 400 px; bloco central menor e ofertas abaixo da marca, sem colisão. Roteiro segue com seis produtos oficiais e gradiente discreto.
- QA geométrico em `previews/layout_qa_v05.json`; filmstrip e frames integrais revisados. O arquivo v04 foi arquivado em `versoes/v04/` antes da nova versão.
- MP4 final inspecionado em 0,75 s, 8,5 s e 17,8 s; `ffprobe` confirmou 1080×1920, H.264/AAC, 60 fps, 20,0 s. Nenhum produto foi redesenhado ou substituído.

## Histórico v04

- Hipótese: uma única busca mais pausada comunica melhor a chegada à CDF; a órbita de seis produtos substitui o quadro redundante de categorias.
- Novo 9:16 recomposto para Meta, sem esticar a master quadrada. Margens internas conservadoras de 250 px no topo/rodapé. Confirmar a prévia do placement antes de veicular.
- Gradientes suaves substituem o branco chapado. Produtos reais e logo oficial preservados. O fundo branco dos dois packshots novos é original da imagem do catálogo.
- Quatro condições aparecem sequencialmente, com asterisco e nota curta na peça. A garantia é da estrutura de modelos selecionados; frete grátis tem elegibilidade/valor mínimo. Revalidar condições antes de publicar.
- Fontes: homepage e páginas de produto CDF capturadas em 28/09/2026; detalhes em `offer.json`. Novos assets oficiais em `assets/cdf-busca-categorias/`.
- v03 quadrada preservada em `versoes/v03/`. Nenhuma campanha, site ou plataforma foi alterada.
- QA final: filmstrip e frames extraídos do MP4 revisados (abertura, órbita/condição e encerramento); `ffprobe` confirmou H.264/AAC, 1080×1920, 60 fps, 19,0 s. Produto e label não se sobrepõem na escala revisada.

## Histórico v03

- Revisão solicitada pelo usuário: transições menos apressadas, novo quadro de entrada no navegador e busca por "equipamentos fitness para casa".
- Duração ampliada de 15 para 18 s para manter o tempo de leitura existente e acomodar 3 s completos de órbita das quatro categorias. Produtos, cartões e rótulos percorrem juntos 90°; equipamentos permanecem na orientação correta.
- v03: 1080×1080, 60 fps, 1080 frames, H.264 yuv420p e AAC estéreo. Master Tesseract 2160×2160 reduzido por Lanczos; o método de suavização das bordas da v02 foi mantido.
- v02 preservada em `versoes/v02/`; a raiz contém somente o MP4 atual. Filmstrip e frames extraídos do MP4 final foram revisados. Sem alteração de assets originais, oferta, site ou campanhas.

- Storyboard v01 aprovado pelo usuário e arquivado em `versoes/v01/`.
- Trilha e SFX são originais, sintetizados localmente; sem faixa de terceiros e sem voz.
- Páginas da CDF deliberadamente reimaginadas para o vídeo, sem representar captura fiel do site.
- Produtos reais usados como imagem, mas sem alegação de disponibilidade atual.
- Tesseract CLI local `0.2.0`; assets originais preservados.
- QA: filmstrip da versão final, previews do Tesseract e frames extraídos do MP4 revisados; `ffprobe` confirmou vídeo e áudio de 15 s.
- Não foram aplicados preços, parcelamento, PIX, cupom ou estoques. Produto e destino comercial devem ser confirmados novamente antes da veiculação.
