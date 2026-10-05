# Carrossel de Pinheiros no Tesseract — v01 (01/10/2026)

Origem: anúncio "Estático - Carrossel" (120250004635270359), conta de Pinheiros, campanha [Leads] - [Cond, Acad, Hot] - Pinheiros; último carrossel com entrega (21/09/2026).

## O que foi mantido
- Cinco cartas, na mesma ordem e com o mesmo texto: Valorize seu condomínio com uma academia de verdade / Compre ou alugue / Equipamentos fitness com marcas líderes / Parcelamento facilitado para montar academia no seu condomínio / Solicite seu orçamento (Clique aqui).
- Elementos: nove logos de marcas (Speedo fitness, Tauka, Le Forzz, Mormaii, Schwinn, WaterRower, Nohrd, Bowflex, Body Bike), ícone do cartão do parcelamento, símbolo da Casa do Fitness, faixa laranja, botão.
- Os logos e o ícone foram recortados do carrossel original por chave de luminância (não há arquivos oficiais no workspace). Trocar por arquivos oficiais quando existirem.

## O que mudou
- Fotos de cenário novas: academia de hotel (projeto real da Casa do Fitness, do Instagram da marca), sem as fotos de condomínio do anúncio original.
- Tudo em camadas nativas e editáveis: texto (letra a letra nos títulos em degradê), formas, imagens, keyframes; transição com faixa diagonal da marca.
- Fundos das cartas 3, 4 e 5 escurecidos em camada nativa e levemente desfocados.

## Entrega
- feed 1080x1080 e stories 1080x1920, MP4 H.264 60 fps, 13 s.
- Projetos editáveis em projeto/*.tsrct; script em scripts/build_carrossel_pinheiros.py (assets por scripts/prep_carrossel_pinheiros_assets.py).

## v02 (01/10/2026) — revisão pedida
- Texto reto, sem itálico (o skew da v01 foi removido).
- Títulos em degradê numa camada só, com sobreposição de degradê nativa (sem letras soltas, sem artefatos).
- Faixa de transição diagonal removida; transição por fade com escurecimento. Faixa laranja da carta 2 entra deslizando, com sombra e um brilho que cruza.
- Cada carta fica 3,4 s (antes 2,6 s); vídeo de 17 s.
- Acabamento: barra de progresso do carrossel no pé, sublinhados em degradê sob os títulos, sombras suaves no texto, zoom lento nas fotos, logos entrando em sequência.
- Conferido pelos quadros dos MP4 exportados (feed e stories) e por quadros do projeto em resolução cheia. v01 arquivada em versoes/v01.

## v03 (01/10/2026) — alinhamento e acabamento
- Todos os blocos de texto no mesmo eixo vertical (stories 905 px, feed 515 px); carta 1 deixou o rodapé e foi para o centro.
- Textos e logos só com fade (sem deslocamento nem escala): elimina a tremulação do início.
- Export em 4K reduzido para 1080 (Lanczos, CRF 14): suaviza o serrilhado leve dos textos.
- Rodapé: degradê escuro e risquinhos laranja diagonais nos cantos (mesmo detalhe das peças B2B), com a barra de progresso por cima.
- Conferido por quadros dos MP4 exportados e por recorte em resolução cheia. v02 arquivada em versoes/v02.

## v04 (01/10/2026) — bordas, rodapé e topo
- Risquinhos laranja nos quatro cantos (traço fino como nas peças B2B), com desvanecimento em todas as bordas da imagem: sem corte reto.
- Degradê escuro suave (seis paradas) no topo e na base.
- Símbolo da CDF no topo, centralizado, fixo em todas as cartas (saiu do bloco da carta 5).
- Fotos da carta 2 com cantos arredondados e borda esfumada, entrando por baixo da faixa; altura menor para não tocar no símbolo.
- Fundo cinza da carta 2 com fade (antes aparecia de uma vez).
- Verificado por quadros dos MP4 exportados, por quadros de resolução cheia e por teste com brilho aumentado nas bordas.

## v05 (01/10/2026)
- Botão da carta 5: "CLIQUE AQUI" passa a "CLIQUE ABAIXO" (sem seta), para acompanhar o botão "Pedir cotação" da Meta. Nada mais mudou. v04 arquivada em versoes/v04.

## v06 (01/10/2026)
- Carta 2: fotos em sangria total (sem moldura cinza nem cantos arredondados), encontro das fotos no centro da faixa (sem vão), escurecimento leve, degradês que nascem da faixa e trilho escuro sob a faixa.
- Extremidades mais escuras em todas as cartas: degradês de topo e base mais fortes e longos, vinheta lateral de 190 px.
- Símbolo da CDF 25 px mais alto (stories y=267, feed y=63).
- Verificado por quadros dos MP4 exportados; v05 arquivada em versoes/v05.

## v07 (01/10/2026)
- Símbolo da CDF movido só na vertical: centro a 67 px do topo em todas as cartas (ponto marcado pelo usuário), centralizado em x=540, no feed e no stories. v06 arquivada em versoes/v06.

## v08 (01/10/2026)
- Só a carta inicial mudou: texto ampliado de 70 para 90 px no feed e de 88 para 104 px no stories. O bloco desceu e ganhou mais espaço entre linhas, mantendo distância do símbolo e da barra de progresso.
- Dois MP4 com trilha em `pecas/videos-com-trilha/` substituídos, com o mesmo áudio AAC e as demais cartas preservadas. Cópias anteriores e quadros de comparação em `outputs/carrossel_pinheiros_carta1_20261001/`. Nenhum anúncio foi alterado.
