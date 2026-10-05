# Notes

## Renderer decision
- HyperFrames 0.8.134; ver v03 abaixo e historico anterior.

## Hook visual e carrossel ampliado, 05/10/2026

- Revisao autorizada pelo usuario: virada de pagina retirada, pergunta digitada em 0,72 segundo, cupom visual com Ganhe / 5% OFF / na sua primeira compra e tres produtos reais abaixo. Entrada com deslocamento curto, luz sobre o cupom e movimento discreto das fotos.
- Carrossel centrado: Esteiras, Bicicletas, Musculacao, Acessorios, E muito mais. Musculacao usa recorte original `assets/cdf-merchant-teste/cutout/estacao-speedo-multi3.png`, copiado sem alteracao. Ultimo card combina tres produtos e logo oficial; sem novas ofertas.
- Mantidos 18 segundos, tipografia, paleta e margem de 250 px. Carrossel ampliado ocupa cerca de nove segundos; carrinho e institucional reposicionados. Sem musica nem render final. MP4 anterior intacto.
- Provas visuais em Stills/v03-visual-hook, v03-visual-hook-final e v03-visual-transition-final. Check sem erros na revisao; fotos repetidas por uso editorial geram avisos de descoberta duplicada. Texto digitado e animacoes dependem somente do timeline. Claim de 20 anos continua pendente de confirmacao comercial.

## Revisao moderna do preview, 05/10/2026

- Somente HTML, sem musica e sem render de producao. MP4 existente representa a versao anterior, preservada em Source/v03-18s-before-modern.
- Cartoes de 820 px centralizados em x=540. Abertura com 5% OFF em destaque, luz passando sobre o cupom e detalhes animados. Superficies com luz, profundidade, fundo em movimento lento e parallax dos produtos. Copy e fotos oficiais preservadas.
- Stills de sete estados em Stills/v03-modern, mais tres estados da abertura em Stills/v03-modern-hook, revisados visualmente. HyperFrames check passou sem erros; 28/28 testes de contraste. Aviso de sobreposicao projetada durante a virada e reutilizacao da TR3 no carrinho. Fonte editavel em projeto/filme; preview localhost:3043.

## V03 conforme briefing de 05/10/2026

- Render final verificado: 18,000 segundos, 540 frames, H.264 yuv420p, AAC stereo 48 kHz, 8.392.714 bytes, -14,9 LUFS, pico -1,3 dBTP. Reels: 12 PASS, zero FAIL e aviso opcional de legenda separada ausente. Sem fala; copy ja incorporada ao video. Contact sheet final inspecionada em `previews/filmstrip_v03_18s.png`. QA em `qa-v03.json`. MP4 na raiz e copia em Renders. Captura screenshot com GPU de hardware e um worker, adequada a memoria livre limitada. Nenhuma publicacao realizada.

- Entrega: 18 segundos, 1080x1920, 30 fps, MP4 com instrumental original de 104 BPM e Foley sintetizado. Sem voz, sem GIF. Bai Jamjuree e assets oficiais identicos aos fornecidos, verificados por SHA-256.
- HTML/GSAP deterministico, papel articulado em 18 faixas com a mesma textura e copy. Skills de contexto, humanizer, FFmpeg e contratos HyperFrames utilizados. Texto comercial literal, inclusive o travessao no item do carrinho.
- Seis stills em `Stills/v03/`, inspecionados. Cupom inteiro no campo; cartao deslocado 50 px para separar do titulo. Logo da folha em y=330 para preservar margem sob perspectiva. MAIS DE separado da caixa tipografica de 20 anos.
- HyperFrames check passou sem erros. Avisos: carrossel fora do canvas por desenho, contraste transitorio da legenda TR3 em fade de entrada, imagem TR3 repetida no carrinho. Estados legiveis sem sobreposicao; produtos em parallax translacional sem deformacao.
- Rascunho anterior preservado em `Source/v03-before-brief/`; projeto editavel em `projeto/filme/`. Preview: `http://localhost:3043/#project/filme`.
- Confirmar a afirmacao sobre 20 anos com o comercial antes de publicar. Oferta e cupom vieram do usuario. Sem outras condicoes comerciais ou alteracoes em plataformas.

## Director notes


## Rodada 1 (05/10/2026) — 3 direções em still, só TR3
- Renderer: HyperFrames 0.8.134 (layout + produto recortado + tipografia); stills via `hyperframes snapshot --at 4.5`.
- Fonte da verdade: briefing 12 (5% OFF na primeira compra, cupom PRIMEIRACOMPRA, aplicado no carrinho) + nome do produto no catálogo Meta CDF (TR3 "Dobrável Residencial"). Nenhum preço, Pix, parcela ou frete na peça.
- Ainda a validar no carrinho: elegibilidade e cumulatividade do cupom (nota do briefing).
- Referência Black Friday usada só como gramática: parede escura, tubos de neon, produto grande com sombra de piso, chips.
- A: neon na parede (herda a BF). B: ticket de cupom em campo vermelho sólido. C: demonstração do cupom no carrinho, estúdio claro.
- Produto: foto do catálogo (id 158297), recorte por flood fill no fundo branco; sem recriar produto.

## Rodada 2 (05/10/2026) — direção A escolhida
- Ajustes: card do cupom reto e alinhado à margem de 72 px; logo movida para o rodapé como assinatura (fora do topo, dentro da safe area); recorte da TR3 refeito (3x, contorno suavizado, sem halo branco); sem repetição (cupom só no card, "Aplique no carrinho" só uma vez; chip "cupom no carrinho" removido).
- Variações, uma hipótese cada: A2 = cupom como letreiro de neon (ideia vinda da busca de referências de neon em parede de tijolo); A3 = Motion-S no lugar da TR3 (tag "Conexão Bluetooth" vem do nome do produto).
- Busca na web trouxe só bancos de imagem/templates genéricos; a única ideia aproveitada foi o neon-sign na parede.
- Limite conhecido: foto-fonte da TR3 tem 1000 px; em zoom 3x fica macia. Para peça final, pedir foto maior ao comercial.

## Rodada 3 (05/10/2026) — 4 propostas novas (as anteriores A/A2/A3/D foram excluídas a pedido)
- V1 editorial: papel creme, "5" serifado gigante, canhoto de cupom. Fontes extras: Playfair Display + Anton (OFL, via @fontsource) além da Bai Jamjuree.
- V2 adesivo pop: amarelo com halftone, produto com recorte die-cut, burst vermelho, cupom em adesivo com fita.
- V3 cromo: "5%" cromado, piso espelhado, feixes de luz, OFF em neon, cupom em placa de metal com LED.
- V4 carrinho: esteira dentro de um carrinho ilustrado, cupom como etiqueta pendurada na alça.
- Fonte da verdade: igual à rodada 1 (briefing 12 + nome do produto no catálogo). Nenhum preço, Pix, parcela ou frete.
- Fontes e assets: assets/primeira-compra-cupom/{product,fonts}.

## Rodada 4 (05/10/2026) — linguagem minimalista da marca
- Pedido: moderno, pé no chão, minimalista; referência = site casadofitness.com.br (lido no navegador em 05/10).
- Sistema extraído do site: fundo branco/cinza claro, Bai Jamjuree preto, vermelho #e60a14 nas etiquetas OFF, botão redondo com gradiente laranja→vermelho (ícone de sacola), cards com borda fina e raio ~20 px, amarelo-limão #dfe03a só no banner de home.
- M1 branco, M2 cinza com etiqueta vermelha e barra preta de cupom, M3 gradiente laranja/limão. Só Bai Jamjuree; sem fontes extras.
- As rodadas 1 a 3 (neon, editorial, adesivo, cromo, carrinho) foram excluídas a pedido.

## Rodada 5 (05/10/2026) — filme no padrão do cdf-busca-categorias
- Diagnóstico: as rodadas 1 a 4 eram estáticos tentando resolver um briefing de vídeo. O padrão aprovado (cdf-busca-categorias) é filme: cenas com uma ideia, cursor, digitação, 60 fps, gradiente do brandbook, cards brancos, painel grafite com texto amarelo.
- v01: 15 s, 1080x1920, 60 fps, HyperFrames 0.8.134. Cenas: produto + cupom já na tela; benefício funcional (Dobrável, Uso residencial, do nome do produto); carrinho com digitação de PRIMEIRACOMPRA e clique em APLICAR; fechamento com 5% OFF, cupom, slogan do site e domínio digitado.
- Fonte da verdade: briefing 12 + nome do produto no catálogo Meta CDF. Sem preço, Pix, parcela ou frete. Validar cupom no carrinho antes de veicular.
- Pendências: trilha/efeitos (sem áudio), Feed 4:5, Motion-S, GIF (3 a 6 s em loop), revisão do movimento com o vídeo tocando.
- Processo: pulei os 3 storyboards do fluxo do lab nesta versão; registrar como dívida.

## Rodada 6 (05/10/2026) — v02 menos redundante e sem tremulação
- Feedback do Pedro: ideia boa; cards redundantes; corrigir tremulações.
- Redundância: 5% OFF, "na primeira compra" e o código apareciam 4 vezes. Agora: abertura "Na sua primeira compra tem cupom." + código (briefing); meio com quatro condições, uma por vez, no painel grafite; "5% OFF" só aparece quando o cupom é aplicado no carrinho; fechamento com slogan do site e o cupom.
- Informações novas (fonte: home casadofitness.com.br lida em 05/10/2026 + nome do produto): Dobrável; até 18x sem juros*; assistência técnica em todo o Brasil; garantia exclusiva. Ressalva "*Consulte condições no site." Não usados de propósito: garantia de 2 anos (só modelos selecionados), frete grátis (acima de R$10.000, a TR3 não alcança), 5% OFF no Pix (confunde com o cupom).
- Tremulação: causa 1, domínio digitado re-centralizava a cada letra (margem esquerda variava de 231 a 447 px); corrigido com bloco de largura fixa (margem constante 205 px em 48 quadros). Causa 2, balanço lento em y/rotação 3D do produto e dos cards; trocado por respiração só de escala. will-change/force3D nos elementos móveis. tl.call (não seguro em render paralelo) trocado por tweens.
- v01 em versoes/v01. v02: 18 s, 1080x1920, 60 fps, sem áudio.

## Rodada 7 (05/10/2026) — v03 com o roteiro do Pedro
- Roteiro dado pelo Pedro: 1) página sendo virada ("Ainda não comprou com a gente? Ganhe 5% OFF na sua primeira compra."); 2) carrossel de produtos passando de lado como Meta Ads (esteira, bicicleta, acessórios); 3) carrinho, menos redundante; 4) fechamento puramente institucional (Casa do Fitness, slogan, site digitado, mais de 20 anos de história).
- v03: 19 s, 1080x1920, 60 fps. Página em 3D com sombra projetada e virada de 18° a 180°; primeiro quadro já com a página em curva. Carrossel: Esteiras (Speedo TR3), Bicicletas (Mormaii Motion-S), Acessórios (Bowflex SelectTech), com gesto de arrastar e pontos de progresso. Carrinho: cupom digitado, clique, "Cupom aplicado" sem repetir o 5%. Fechamento sem cupom.
- Fonte da verdade: briefing 12 (cupom, 5% OFF primeira compra), instrução explícita do Pedro ("mais de 20 anos de história" — não conferi em fonte pública, validar com comercial/institucional antes de veicular), nomes dos produtos do catálogo/site. Sem preço, Pix, parcela, frete ou garantia.
- Assets novos: assets/primeira-compra-cupom/product/halter.png (recorte do halter Bowflex a partir de assets/cdf-busca-categorias).
- QA: lint sem erro; margem esquerda do domínio digitado constante (205 px) em 53 quadros. Sem áudio.
- v02 arquivada em versoes/v02.

## Rodada 8 (05/10/2026) — v04 no projeto do Studio
- Pedido do Pedro: cena 1 prende atenção já com o cupom na tela; cena 2 carrossel com informação da categoria no lugar de "Comprar agora"; cena 3 melhorada de fato; cena 4 com as sugestões (20 anos direto, painel do slogan maior).
- Cena 1: ticket com 5% OFF e o código PRIMEIRACOMPRA visíveis desde o primeiro quadro; pergunta digitada em duas linhas de largura fixa; miniaturas de produtos removidas (repetiam o carrossel).
- Cena 2: cinco cartas sem botão; cada uma com dois chips de informação, todos vindos de nome de produto/URL/menu do site: Esteiras (Dobrável, Uso residencial), Bicicletas (Spinning, Conexão Bluetooth), Musculação (Estação de musculação, Com leg press), Acessórios (Halteres reguláveis, De 2 a 24 kg), E muito mais (Elípticos, Remo, Escada, Seminovos).
- Cena 3: carrinho com item, campo com foco, digitação, clique com spinner e check desenhado, faixa "Cupom aplicado", linha de desconto e barra de total que encolhe (abstrato, sem números); empurrão de câmera lento.
- Cena 4: "20 anos" entra direto em branco; painel do slogan 860x176.
- Projeto era do Codex (revisões v03 acabamento moderno e hook); reescrevi index.html, modern.css e modern.js; paper.js ficou sem uso. v03 em Renders preservado.

## Exportação v04 (05/10/2026)
- Render final: primeira-compra-cupom_stories-9x16_v04.mp4, 18 s, 1080x1920, 60 fps, H.264 yuv420p, AAC estéreo 48 kHz, -14,3 LUFS, pico -1,6 dBFS. Cópia em Renders/.
- Áudio: base instrumental original de 104 BPM (do v03) + Foley de interface nos tempos do v04 (digitação, viradas do carrossel, clique, confirmação, golpe do "20 anos"), `projeto/make_audio_v04.py`. Sem voz nem amostras de terceiros.
- QA: `hyperframes check` sem erros; filmstrip do MP4 final inspecionado (previews/filmstrip_v04.png); `qa-v04.json`.
- v03 arquivado em versoes/v03 (MP4 + QA). O versionador do lab (`scripts/lab_versions.py`) quebrou ao copiar `projeto/filme/.thumbnails` do Studio (caminhos longos no Windows) e o código-fonte do v03 não foi arquivado; está no histórico do HyperFrames (`npx hyperframes history`) e em Source/. Vale excluir `.thumbnails` da cópia no script.
- Antes de veicular: confirmar "Mais de 20 anos de história" e a elegibilidade/cumulatividade do cupom no carrinho. Nenhuma plataforma alterada.

## v05 (05/10/2026) — refinamentos aplicados
- Alinhamento: topo único em y 340 (logo/título) nas quatro cenas; dois tamanhos de logo (360 e 650); "5% OFF" alinhado à margem do ticket; chips das cartas em 31 px sem estourar.
- Redundância: tirei a subfrase "Para montar a sua academia" e o logo da última carta (bloco centrado na vertical, quatro categorias maiores); carrinho sem "1 unidade" e sem o brilho amarelo no campo (sucesso = check no botão + faixa + linha de desconto).
- Ritmo: abertura +0,5 s e cada carta +0,3 s; filme de 19,8 s. Áudio refeito nos novos tempos (`projeto/make_audio_v05.py`), -15,0 LUFS, pico -1,8 dBFS.
- Decisão deixada de fora: "-5%" na barra de desconto do carrinho (repetiria o número). Opcional se o Pedro quiser reforçar o ganho.
- v04 arquivado em versoes/v04 (MP4, QA, index.html, áudio e script). O modern.css/js do v04 não foram arquivados (já tinham sido editados quando copiei) e podem ser recuperados pelo histórico do HyperFrames.
