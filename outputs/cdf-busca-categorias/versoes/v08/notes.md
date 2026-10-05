# Notas — filme v08

- Origem: o Pedro apontou a seta bugada e pediu uma abordagem melhor para o primeiro quadro, mais evidência na rotação das categorias e o fundo no gradiente do brandbook.
- Seta: a v07 usava duas formas sem relação (contorno e miolo desalinhados). Agora há uma seta única, com contorno gerado por deslocamento uniforme do miolo.
- Primeiro quadro: anel das seis categorias em volta do cartão (posições em elipse, fora do cartão) para o produto aparecer no primeiro segundo e antecipar a órbita. O primeiro produto deixa de aparecer só em 5,3 s. O ritmo da busca não mudou.
- Gradiente: preto → vermelho → laranja (amarelo no canto) em todas as cenas. Como o anel da órbita era desenhado com recorte na cor do fundo, virou disco translúcido. Rules de acento e condição em amarelo do brandbook. O contraste do texto branco foi conferido nos frames (título no topo escuro, aviso legal e domínio em zona vermelha).
- Giro: 84° por cena, mesma geometria segura: QA de 121 estados com cards a 85 px, card-hub a 22 px, margem 65 px (`previews/layout_qa_v08.json`).
- Conferi filmstrip e frames do MP4 em 0,0 s, 0,8 s, 3,9 s, 7,6 s, 11,8 s e 16,5 s. `ffprobe`: H.264 yuv420p 1080×1920, 60 fps, AAC 48 kHz estéreo, 18,0 s.
- v07 arquivada em `versoes/v07/` com hash idêntico; a raiz contém só a v08.
- Pendências: revisar movimento e trilha com o vídeo tocando; conferir de novo as condições comerciais antes de veicular. Nenhuma plataforma alterada.

## Histórico v07

- Origem: o Pedro pediu uma crítica quadro a quadro da v06 e depois cobrou que os pontos fossem corrigidos na hora. A v07 aplica todos.
- Decisão de roteiro (minha, reversível): três frases de marca em 18 s diluíam a mensagem. Mantive “Seu próximo treino começa aqui.” na busca e “Sua saúde, nosso impulso.” no fim; “Tudo para se mover.” ficou só como tagline do hub e a manchete da órbita virou “Do cardio à força.”.
- QA geométrico em `previews/layout_qa_v07.json`: 121 estados da órbita, cards a 85 px, card-hub a 22 px, margem segura de 65 px (o validador barrou o halter em escala 16,5; ficou 16). Filmstrip e frames do MP4 (0,9 s, 3,9 s, 8,5 s, 12,2 s, 16,5 s) revisados.
- `ffprobe` do MP4: H.264 yuv420p 1080×1920, 60 fps, AAC 48 kHz estéreo, 18,0 s. v06 arquivada em `versoes/v06/` com hash conferido; a raiz contém só a v07.
- Ainda não feito: (1) produto visível já no primeiro segundo. O primeiro produto aparece em 5,3 s porque a busca digitada em ritmo legível foi pedida antes; (2) revisão do movimento e da trilha com o vídeo tocando, só conferi quadros parados.
- Condições comerciais iguais às de `offer.json`; revalidar antes de veicular. Nenhuma plataforma alterada.

## Histórico v06

- Solicitação em andamento no fim da v05: melhorar quadros, continuidade, microinterações e a órbita em 60 fps, mantendo hierarquia, espaçamento e área segura.
- v06: movimento contínuo nas três cenas, cards da órbita menores, sequência das condições sob a marca e encerramento preservados. Duração 18 s (v05: 20 s).
- QA geométrico em `previews/layout_qa_v06.json` (121 estados de órbita, 30°): cards a 85 px, card-hub a 22 px, margem segura de 65 px. Filmstrip e frames do MP4 (0,75 s, 4,2 s, 8,5 s, 12,4 s, 17,8 s) revisados. A entrada e a saída das condições foram checadas em quadros intermediários.
- `ffprobe` do MP4 final: H.264 yuv420p 1080×1920, 60 fps, AAC 48 kHz estéreo, 18,0 s.
- v05 arquivada em `versoes/v05/` com hash conferido; a raiz contém só o MP4 atual. Projeto Tesseract editável atualizado em `projeto/stories-9x16.tsrct`.
- Trilha e efeitos: síntese original local, sem voz e sem faixa de terceiros. Nenhuma plataforma alterada.
- Finalizada por Claude em 28/09/2026 a pedido do usuário: a reserva do Codex estava aberta com projeto e prévias prontos e sem MP4; exportei o MP4 com o script do Codex e fiz o QA.

## Histórico v05

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
