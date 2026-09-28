# Composição e QA visual — Tesseract Creative Lab

Aplicável a estáticos, GIFs e vídeos, em feed 1:1/4:5 e stories 9:16. É um critério de revisão, não um template rígido: a marca, o brief, o produto e as especificações atuais do placement têm prioridade. Leia junto de `WORKFLOW.md`, `OFFER-TRUTH.md` e `QA-PAID-MEDIA.md`.

## Primeiro: a grade, depois o acabamento

- Defina margens externas, área segura da interface, colunas, card principal e uma escala de espaçamentos antes de posicionar textos. Não coloque conteúdo essencial no limite do canvas.
- Alinhe elementos relacionados pela mesma borda ou eixo: produto/card, nome, condição, preço, PIX e CTA. Se vários produtos dividem um vídeo, mantenha as âncoras de nome, preço, oferta e aviso legal na mesma posição entre cenas; uma condição ausente não deve deslocar os demais elementos.
- Dê ao produto área dominante sem cortar componentes nem distorcer a imagem. Use o espaço do card de modo intencional; verifique a maior escala da animação, não só o frame estático.
- Reserve espaços diferentes para funções diferentes: marca, produto, oferta e aviso legal. Respiro cria hierarquia; vazio grande sem função e blocos comprimidos são ambos defeitos.
- Trate faixas, pílulas e cards como componentes de uma grade. Suas bordas devem conversar com os outros blocos; evite uma faixa de oferta arbitrariamente curta ou desalinhada.
- Preço principal, preço anterior, parcela e PIX precisam de prioridade visual inequívoca. Texto de apoio e aviso legal devem continuar legíveis em celular, com contraste suficiente, mas sem competir com a oferta.
- Não corrija desequilíbrio apenas aumentando tudo. Ajuste primeiro posição, largura, espaçamento e relação entre blocos; preserve logo oficial, produto e verdade comercial.

## Adaptação por formato

- Componha 1:1, 4:5 e 9:16 separadamente. Não centralize simplesmente uma peça horizontal/quadrada dentro de stories nem estique/corte a master.
- Para criativos Meta 9:16 de 1080×1920, reserve **250 px no topo e 250 px no rodapé** como regra interna conservadora: logo, perfil/assinatura, headline, produto indispensável, preço, condição, CTA e aviso legal devem caber entre y=250 e y=1670. Fundo, textura e elementos puramente decorativos podem sangrar até as bordas. Confira a prévia de Stories e Reels, pois os overlays variam por placement e interface; 250 px não é especificação universal da Meta.
- Em feed, confira também o corte em grade/preview e a leitura do anúncio em tamanho reduzido. O aviso legal precisa de margem de verdade, não apenas de alguns pixels visíveis no arquivo aberto.
- Não transfira os 250 px literalmente para feed 1:1 ou 4:5; use área segura específica do formato e prévia do placement. Aplicá-los ao 4:5 consumiria uma parcela desproporcional da área útil.
- Use coordenadas específicas por formato para card, imagem, tipografia e fechamento. O produto pode crescer em 9:16, mas a composição inteira deve ser redistribuída para aproveitar a altura.

## Hierarquia comercial

- Quando o parcelamento for o argumento principal, mostre primeiro a condição (por exemplo, `18x sem juros de`) e o valor da parcela com maior peso tipográfico. O PIX entra abaixo como alternativa secundária, ainda legível.
- Evite uma faixa horizontal sólida de PIX com a mesma largura do card quando ela competir com o preço principal. Prefira texto em linha, um acento curto, ou um componente compacto de menor contraste/peso. O conteúdo comercial não muda com o tratamento visual.
- Não crie CTA desenhado dentro da peça se ele puder ser confundido com o botão nativo da plataforma. Na peça final, confirme se o CTA visual tem função editorial e não colide com o CTA do placement.

## Motion e consistência

- Revise abertura, entrada de cada produto, estado estável, saída, transição e fechamento. Cheque se nenhuma imagem aparece fora do card durante a entrada e se nenhum texto permanece após a saída do item.
- Mantenha tempo de leitura suficiente para produto e condição; o hook deve ser compreendido nos primeiros 1–1,5 s. O CTA final deve permanecer estável e legível antes do loop.
- Um zoom discreto deve manter o produto ancorado no centro durante a leitura, salvo intenção narrativa explícita. Não anime posição lateral junto com a escala por acidente; reserve o slide para entrada/saída. Cheque o frame de maior escala contra as bordas do card. Movimento não pode ocultar item, marca, preço ou aviso legal.
- Em série de produtos, mesma grade e timing produzem comparação fácil; adapte só o necessário às proporções reais de cada item e à presença de preço anterior.

## Gate de aprovação

1. Conferir snapshot comercial e assets oficiais, incluindo validade da oferta. Não reutilizar preço, frete ou parcela antigos por serem visualmente atraentes.
2. Gerar preview em resolução integral e filmstrip com abertura, cada produto e encerramento. Inspecionar também a miniatura/tamanho mobile.
3. Conferir padding nas quatro bordas, alinhamentos repetidos, áreas seguras, contraste, texto menor, logo e produto em sua maior escala.
4. Conferir MP4/GIF final — dimensões, duração, frames, loop e ausência de cortes. O preview do projeto não substitui o QA do arquivo exportado.
5. Registrar em `notes.md` o que mudou, o que foi mantido, fonte comercial, formatos testados e qualquer limitação. Ajuste fino autorizado regrava a versão atual; preservar cópia recuperável antes da substituição.

## Aprendizado do mix CDF v03 — 23/09/2026

No refinamento de `outputs/cdf-mix-produtos/`, a direção visual do Opus foi mantida. A primeira rodada alinhou as condições e ampliou a ocupação do card; a revisão seguinte mostrou que a pílula PIX, embora alinhada, competia com o parcelamento. Ela virou uma linha secundária com acento curto. O 9:16 foi recomposto para manter todo conteúdo crítico dentro dos 250 px reservados no topo e no rodapé. Essas soluções são exemplos, não medidas universais para outros criativos.

## Referências externas triadas em 23/09/2026

O [post indicado pelo usuário](https://x.com/Manixh02/status/2102686747952041989) lista cinco bibliotecas. Úteis como repertório de mecanismo, nunca como fonte de identidade, oferta ou licença de assets:

| Fonte | Uso no laboratório | Limite |
|---|---|---|
| [transitions.dev](https://transitions.dev/) | Referência de timing, reveal, troca de estados e microtransições; traduzir o princípio para Tesseract/Remotion. | Exemplos são de interface web, não templates prontos para anúncio. Evitar motion gratuito. |
| [godly.design](https://godly.design/) | Referência de hierarquia, respiro, enquadramento e CTA para estudar composição. | Curadoria de web/UI; não importar marca, copy ou layout literalmente. |
| [backgrounds.supply](https://backgrounds.supply/) | Inspiração eventual de profundidade, textura e tratamento de fundo. | Usar só se combinar com o brandbook e não reduzir contraste; verificar direitos antes de incorporar qualquer asset. |
| [animos.app](https://animos.app/) | Referência exploratória de apresentação/motion. | É voltado a showcases de design; validar utilidade e termos antes de usar materiais. |
| [deck.gallery](https://deck.gallery/) | Repertório para apresentações, brandbooks e narrativa de slides. | Menos direto para criativos pagos de produto; parte do acervo exige assinatura. |
