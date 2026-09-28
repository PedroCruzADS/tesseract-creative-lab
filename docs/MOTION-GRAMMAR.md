# Motion grammar — Tesseract Creative Lab

Este documento define a linguagem de movimento padrão do Lab. Não é um estilo visual único; é um conjunto de restrições para evitar motion genérico, “PowerPoint animado” e decisões arbitrárias.

## Princípio

**Movimento deve transportar informação, foco ou continuidade.**

Uma animação que não muda leitura, hierarquia, estado ou contexto deve justificar sua existência.

## Continuidade entre cenas

Prefira transições por elemento compartilhado:

- botão cresce e vira painel;
- card vira frame de produto;
- círculo vira selo/oferta;
- imagem atravessa a transição e ocupa o próximo layout;
- cor nasce de um elemento da cena anterior e inunda a próxima;
- texto sai de máscara ou troca de estado dentro do mesmo container.

Hard cuts continuam permitidos quando servem ritmo, contraste ou performance. Fade não é proibido, mas nunca deve ser o fallback automático.

## Uma ação primária por vez

Cada beat visual deve ter um foco dominante.

Evite simultaneamente:
- zoom de câmera;
- entrada de headline;
- rotação de produto;
- troca de preço;
- partículas;
- transição de fundo.

Se tudo se move, nada recebe atenção.

## Beat map

Antes do motion final, registre:
- BPM ou grade temporal;
- beats/grupos usados;
- hook;
- reveal;
- payoff;
- condition/offer beat;
- CTA;
- transições;
- holds de leitura.

A música orienta a grade, mas **legibilidade vence densidade de beats**.

Não force evento em todo beat se isso reduzir compreensão do produto ou oferta.

## Câmera

- uma intenção por movimento;
- evite zoom-in seguido imediatamente por zoom-out sem motivo narrativo;
- não use câmera para compensar layout fraco;
- faça push-in quando ele aumenta foco;
- faça pull-back quando ele revela contexto;
- preserve produto e copy dentro das safe areas na maior escala.

## Springs e easing

- springs devem parecer massa, não brinquedo;
- overshoot pequeno por padrão;
- sem bounce repetido;
- entrada rápida + settle curto;
- arrasto direto deve seguir cursor/toque e só springar após release.

## Shared-element handoff

Quando um objeto muda de função entre cenas:
1. preserve posição/forma o suficiente para o olho reconhecer continuidade;
2. carregue cor ou label durante parte do morph;
3. troque conteúdo com máscara dedicada;
4. evite teleportes de um frame.

## Texto

- headline não entra enquanto outro texto ainda disputa o mesmo foco;
- containers que morfam precisam de timing separado para texto antigo e novo;
- texto longo deve usar linhas fixas quando cursor/câmera dependem de sua geometria;
- copy comercial precisa de hold real para leitura.

## Produtos físicos

- motion nunca altera geometria real do produto;
- não “melhore” componentes;
- não invente ângulo ausente;
- zoom e parallax devem trabalhar com o asset real;
- se o produto não suporta recorte convincente, mude a composição.

## Som

Quando houver áudio:
- use música/licença verificável ou trilha original;
- SFX alinhados ao evento pelo pico;
- click, impact, whoosh e success tone devem corresponder a ações reais;
- evite preencher cada movimento com som;
- master final alvo: -14 LUFS, true peak <= -1.5 dBTP, salvo brief diferente.

## Determinismo

Motion programático deve ser função do tempo/frame:
- sem timers dependentes de execução;
- sem estado acumulado entre frames;
- sem random sem seed;
- sem fetch volátil no render;
- assets congelados para o job.

O objetivo é permitir render isolado de qualquer frame, snapshot regression e QA reproduzível.

## Anti-template

Sinais de alerta:
- headline central + gradiente + fade;
- mesma entrada para todos os elementos;
- glows/partículas sem função;
- câmera continuamente respirando;
- cards que só “popam”;
- transições desconectadas do conteúdo;
- toda peça com o mesmo ritmo independentemente do produto.

O agente deve explicar qual informação cada movimento ajuda a comunicar.
