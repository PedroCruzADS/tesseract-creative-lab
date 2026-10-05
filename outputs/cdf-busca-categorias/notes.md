# Notas — filme v12

## Revisão v12 — 29/09/2026

- Feedback do Pedro: a órbita está boa, mas o centro da cena de categorias segue básico. Escopo deliberadamente limitado ao hub; preservar abertura, cards, órbita, ordem das condições e fechamento da v11.
- Direção selecionada: painel editorial em camadas (`Storyboards/storyboard_v12.json`), com superfície grafite, aro de contraste, glint discreto, logo oficial íntegro, condição separada em palavra/número principal e linha de apoio, e 4 microsegmentos de progresso. As duas outras direções foram rejeitadas por risco de reduzir legibilidade ou duplicar visualmente a órbita.
- Fonte comercial: `offer.json` copiado da v11, snapshot de 28/09/2026. Nenhum claim novo; revalidar no site antes de veicular. Renderer Tesseract CLI 0.2.0 para preservar o projeto editável e todas as camadas da v11.
- QA final: o painel externo fica a no mínimo 22 px dos cards em 121 posições amostradas; cards mantêm 85 px de separação e 65 px de margem segura (`previews/layout_qa_v12.json`). Previews da introdução e das quatro condições, filmstrip, stills e frames extraídos do MP4 foram revisados. O pequeno fundo oval interno do primeiro preview foi retirado e a linha secundária ganhou respiro. `ffprobe`: H.264 1080×1920 a 60 fps, AAC 48 kHz, 18,0 s. `validate-job.py` passou.
- v11 arquivada em `versoes/v11/` pelo versionador do Lab antes da exportação. Abertura e encerramento da v11 não foram redesenhados; a composição do encerramento foi conferida visualmente no MP4. Nenhuma plataforma alterada.

## Revisão v11 — 29/09/2026

- Pedido: modernizar abertura e quadros de categoria, remover aparência chapada e evitar que a órbita congele durante as condições sem dividir a atenção do usuário.
- Renderer: Tesseract CLI local 0.2.0, mantendo projeto editável. A animação continua determinística e exportada em 60 fps.
- Três alternativas de storyboard em `Storyboards/storyboard_v11.json`; selecionada “Interface em camadas” por preservar a narrativa já aprovada. O primeiro passe com disco escuro foi rejeitado na própria revisão visual; o segundo ainda pesava no centro; o terceiro usa guia orbital fino, sombras suaves e movimento comercial de 12° em 4,9 s.
- Fontes de repertório: Apple HIG Motion (movimento deve orientar, sem distrair), Apple Spatial Layout (profundidade com hierarquia, não no texto), Google Design “Making Motion Meaningful” (continuidade e arcos), Adobe Motion Graphics (timing e follow-through). URLs registradas no storyboard. Nenhum asset/copy de terceiros incorporado.
- Corrigido bug herdado: a opacidade animada das sombras dos cards subia para 100% apesar do valor inicial menor, produzindo borda preta dura. No v11, sombras terminam em 12%, borda em 55% e destaque em 28%.
- Estado comercial: as quatro condições permanecem conforme `offer.json` capturado em 28/09/2026, com ressalva `*Consulte condições no site.`; revalidar página/eligibilidade antes de veicular. Nenhuma plataforma alterada.
- QA final: `previews/layout_qa_v11.json` validou 121 estados de uma órbita de 72°; distância mínima card-hub 55,2 px, entre cards 85 px, margem segura 65 px. Cinco stills em `Stills/`; filmstrip e frames extraídos do MP4 em `previews/mp4_v11_*.png` revisados. `ffprobe`: H.264 yuv420p, 1080×1920, 60 fps, AAC 48 kHz, 18,0 s. `scripts/validate-job.py` passou no diretório do Lab.
- QA do corte em 5,5 s: a primeira renderização deixou um quadro quase vazio; o título e o hub agora entram legíveis desde o primeiro frame, com logo e tagline alinhados. O frame do MP4 final foi inspecionado em `previews/mp4_v11_5.50_final.png`.
- A v10 foi copiada para `versoes/v10/` com SHA-256 idêntico (`E3E0D9458B36BC1C9A59A8349784332A3EB614DE3842F0B61245D95B942F1400`); o MP4 antigo foi removido somente da raiz depois dessa conferência. O projeto editável e o filmstrip atuais são v11.

## Histórico v10

- Origem: o Pedro observou que a atenção se dividia entre a órbita e as condições no centro e pediu uma coisa de cada vez. Só a cena das categorias foi mexida.
- Linha do tempo da cena (0 = 5,5 s do filme): categorias em 0,3 s, 0,8 s, 1,3 s, 1,8 s, 2,3 s e 2,8 s; giro do anel de 60° até 4,2 s e parado depois; condições de 4,0 s a 8,6 s (1,15 s cada) com o anel imóvel; tagline do hub volta de 8,6 s a 9,1 s.
- Geometria: `previews/layout_qa_v10.json` (121 estados, 60°): card-hub 55 px, cards 85 px, margem segura 65 px.
- Conferi filmstrip e frames do MP4 em 8,0 s e 10,9 s (anel parado com condição no hub). `ffprobe`: H.264 yuv420p 1080×1920, 60 fps, AAC 48 kHz, 18,0 s.
- v09 arquivada em `versoes/v09/` com hash idêntico; raiz só com a v10. Pendências: revisar movimento e trilha com o vídeo tocando; revalidar condições comerciais antes de veicular. Nenhuma plataforma alterada.

## Histórico v09

- Origem: pedidos do Pedro sobre a v08 (voltar ao quadro inicial sem o anel, cartão de pesquisa maior, título menos genérico, hub sem colar nas bordas, categorias em fade sequencial, domínio digitado). Ele falou em 5 categorias; o filme tem 6 (esteiras, bicicletas, acessórios, musculação, remo e elípticos) e todas aparecem em sequência.
- Título: “Monte a academia da sua casa.” é chamada de benefício, sem dado comercial. Trocável se preferir outra frase.
- Hub: além de aumentar a cápsula, o gate de geometria passou a usar a distância até a cápsula (o retângulo antigo reprovava por causa dos cantos arredondados). Resultado em `previews/layout_qa_v09.json`: card-hub 55 px, cards 85 px, margem segura 65 px, 121 estados da órbita.
- Categorias: o giro agora é único para o anel (antes cada card girava a partir do seu atraso), o que evita aproximação entre cards durante a entrada em fade. Entradas em 0,3 s, 0,9 s, 1,5 s, 2,2 s, 2,8 s e 3,4 s da cena.
- Domínio digitado: 55 ms por caractere a partir de 1,1 s do encerramento; largura medida com a fonte Bai Jamjuree Bold para o texto terminar centralizado.
- Conferi filmstrip e frames do MP4 em 0,0 s, 0,8 s, 2,6 s, 6,4 s, 8,9 s, 10,7 s, 16,2 s e 17,8 s. `ffprobe`: H.264 yuv420p 1080×1920, 60 fps, AAC 48 kHz estéreo, 18,0 s.
- v08 arquivada em `versoes/v08/` com hash idêntico; raiz só com a v09.
- Pendências: revisar movimento e trilha com o vídeo tocando; revalidar condições comerciais antes de veicular. Nenhuma plataforma alterada.

## Histórico v08

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
