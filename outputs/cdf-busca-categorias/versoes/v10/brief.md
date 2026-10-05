# CDF — Busca que vira descoberta

## V10 vertical — uma coisa de cada vez na órbita — 28/09/2026

- Mudança única: a cena das categorias agora tem duas fases. Fase 1: as seis categorias entram uma por vez (fade leve, destaque na própria entrada) enquanto o anel gira 60° e para. Fase 2: com o anel parado, as quatro condições passam uma de cada vez no hub. Nada se move na órbita enquanto o texto do hub troca.
- Os pontos de luz que percorriam o anel somem no fim da fase 1. O restante (abertura, busca, título, encerramento com domínio digitado) é igual à v09.

## V09 vertical — ajustes finais de abertura, título, hub e encerramento — 28/09/2026

- Master 1080 × 1920, 18 s, 60 fps. Fundo em gradiente do brandbook mantido.
- Abertura: volta ao cartão de navegador da v07, sem o anel de categorias, e maior (cerca de 67% da largura, centralizado), com logo, campo e botão ampliados. O cartão de busca da cena seguinte também cresce e passa a mostrar apoio e botão mais cedo, reduzindo o branco vazio.
- Título da órbita: “Monte a academia da sua casa.” no lugar de “Do cardio à força.”.
- Hub central: cápsula maior (380 × 240), logo menor e condição em 26 px com folga lateral; o teste de geometria agora mede a distância até a cápsula real.
- Categorias: entram uma por vez, com fade leve (uma a cada 0,62 s), e o anel gira como um conjunto. O destaque sequencial só começa depois que as seis estão na tela.
- Encerramento: “www.casadofitness.com.br” digitado caractere a caractere, com o acento amarelo aparecendo ao final.

## V08 vertical — gradiente do brandbook e órbita mais evidente — 28/09/2026

- Master 1080 × 1920, 18 s, 60 fps. Mesmo roteiro e condições da v07.
- Fundo: gradiente do brandbook (preto → vermelho #E50914 → laranja #FA3312, com toque amarelo #E4E854) nas quatro cenas. Cartões brancos ganham contraste; hub preto com a condição em amarelo; títulos e textos em branco.
- Primeiro quadro: as seis categorias já aparecem em volta do cartão de navegador, anunciando a órbita; o anel some junto com o clique. Sem frase nova.
- Órbita: giro de 84° ao longo da cena (antes 30°) e destaque sequencial por categoria (escala 1,07 e anel amarelo), no sentido do giro.
- Cursor refeito com contorno preto uniforme e miolo branco (o anterior saía deformado); termina fora do texto dos botões.

## V07 vertical — revisão crítica — 28/09/2026

- Master 1080 × 1920, 18 s, 60 fps. Roteiro e condições da v06 mantidos; correções vindas de revisão quadro a quadro.
- Abertura: cartão de navegador maior, com o logo oficial em pílula vermelha já no primeiro quadro; cursor termina na borda do botão, sem cobrir o texto.
- Busca: logo oficial no cartão, lupa no lugar do “>”, texto de apoio maior e mais escuro; cursor termina fora do texto de ENCONTRAR.
- Órbita: título único “Do cardio à força.”; a condição comercial passa a ocupar a marca (branco sobre vermelho, 29 px) no lugar da pílula que se sobrepunha ao hub; a tagline “Tudo para se mover.” volta antes e depois das condições; nomes dos cards 24 px, aviso legal 28 px e mais escuro; fundo e sombras com mais contraste para os cards brancos; remo maior.
- Encerramento: removido o “CASA DO FITNESS” repetido; círculo vermelho fora do texto; domínio em 50 px com acento; bloco reposicionado no centro da área segura.

## V06 vertical — movimento contínuo — 28/09/2026

- Master 1080 × 1920, 18 s, 60 fps. Mesmo roteiro da v05 (clique de 1 s, busca por “equipamentos fitness para casa”, órbita de seis produtos, quatro condições em sequência, encerramento “Sua saúde, nosso impulso.”), com mais respiro entre os quadros.
- Cards menores e mais afastados das bordas; a órbita percorre 30° durante a cena, sem parar, e as condições entram uma por vez sob a marca.
- Controle geométrico em 121 estados da órbita: menor distância entre cards 85 px, card-hub 22 px, margem de segurança horizontal 65 px. Fontes de imagem oficiais, sem redesenho de produto ou logo.
- Condições comerciais e ressalvas iguais às da v04/v05 (`offer.json`); revalidar antes de publicar.

## V05 vertical — revisão de alinhamento — 28/09/2026

- Primeiro segundo: cartão de navegador da CDF, cursor em deslocamento linear e clique para abrir a busca em tela maior; sem aceleração forte.
- Órbita dos seis produtos refeita com âncoras nos centros reais de cada imagem, tamanho e posição próprios por categoria. Todos os produtos e labels ficam dentro de cards consistentes e separados do hub.
- Resto da narrativa, condições, fontes comerciais e fechamento da v04 preservados. Master passa a 20 segundos por causa da abertura adicional.
- Controle geométrico em 31 estados da órbita, com margens seguras e verificação do conteúdo não branco de cada imagem contra as labels.

## V04 vertical — 28/09/2026

- Master 1080 × 1920, 19 s, para Reels/Stories. Conteúdo essencial entre y=250 e y=1670 (regra interna conservadora).
- Abertura única de navegador e busca por “equipamentos fitness para casa”, com digitação em ritmo legível; sem quadro redundante de categorias após a órbita.
- Seis produtos reais orbitam a marca: esteira, bicicleta, elíptico, estação de musculação, remo e halteres. “Muito mais” foi substituído por “Musculação” na categoria; o fechamento contempla acessórios e demais linhas.
- Condições, uma por vez: “Até 18x sem juros”, “Garantia de 2 anos*”, “5% OFF no Pix” e “Frete grátis*”. Na arte, apenas a ressalva compacta “*Consulte condições no site.”
- Fechamento: “Sua saúde, nosso impulso.”, logo oficial e domínio.
- Interface visual é uma releitura editorial, não uma captura literal do site.

## Objetivo
Vídeo de marca e categorias para e-commerce: a entrada no navegador antecede a busca por "equipamentos fitness para casa"; a pesquisa revela a Casa do Fitness e passa por Esteiras, Bicicletas, Elípticos e muito mais.

## Formato e duração
- Master quadrado 1080 × 1080, 18 segundos na v03 para preservar a leitura após adicionar a abertura e a órbita.
- Quatro stills de aprovação antes da animação e do MP4.
- Movimento inspirado no prompt fornecido: câmera sempre em deslocamento, blur direcional proporcional à velocidade, cartões de categorias e corte de impacto na entrada da marca.
- Identidade CDF prevalece sobre a paleta azul/Inter da referência: preto, branco, vermelho e Bai Jamjuree. Logotipo sempre em arquivo oficial.

## Copy
- Busca: "equipamentos fitness para casa".
- Resposta: "Seu treino começa aqui." / "Da primeira corrida à academia completa: encontre o equipamento certo para o seu momento."
- Categorias: "Esteiras", "Bicicletas", "E muito mais."
- Encerramento pretendido: logo oficial e domínio CDF.

## Assets autorizados
- Logo e fontes de `assets/casa-do-fitness-brand/`.
- Recortes oficiais locais de Speedo TR7, Mormaii Motion-S, Starke SH30 e Speedo Multi 3 em `assets/cdf-merchant-teste/cutout/`; origem catalogada em `assets/cdf-merchant-teste/source.json`.
- Nenhum preço, desconto, estoque, garantia ou condição comercial é afirmado.

## Estado
Master animado v03 concluído em 18 s. A abertura mostra o navegador entrando; os quatro produtos orbitam o logo por 3 s completos, cada um vinculado à sua categoria. É uma interface CDF reimaginada para o vídeo, não uma reprodução literal do site. A trilha instrumental e os efeitos são síntese original sem voz.
