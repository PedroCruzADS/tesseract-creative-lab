# Visual reference QA

Quando uma peça existente foi aprovada como direção visual, ela vira **referência canônica**. O agente não recebe licença para reinterpretar a composição só porque o renderer mudou.

## Modos

### Direction reference
A referência inspira ritmo, mecanismo ou hierarquia. Mudança de composição é permitida.

### Visual lock
A referência define:
- macro layout;
- proporções;
- escala relativa;
- áreas de respiro;
- tipografia/weight;
- paleta;
- duração aproximada;
- ordem e duração dos beats;
- linguagem de transição.

Nesse modo, mudar de Tesseract para Remotion/HyperFrames/browser renderer **não autoriza redesign**.

## Gate obrigatório para visual lock

Antes de chamar um preview de aprovado:

1. renderizar o candidato real;
2. extrair keyframes equivalentes da referência e do candidato;
3. gerar `reference-vs-candidate.jpg`;
4. conferir lado a lado:
   - bounding boxes principais;
   - posição e escala do logo;
   - headline;
   - produto/cards;
   - hub/CTA;
   - densidade;
   - safe area;
   - background treatment;
   - sequência e pacing;
5. conferir duração;
6. usar SSIM apenas como sinal auxiliar, nunca como substituto de revisão visual.

Comando:

~~~bash
python scripts/visual_reference_qa.py \
  --reference path/reference.mp4 \
  --candidate path/preview.mp4 \
  --timestamps 0.5,2.5,5,7.5,10,12.5,15,17
~~~

## Critério de bloqueio

Bloqueie se:
- o candidato parecer outra peça;
- um componente dominante mudar de escala/posição sem nota de direção;
- tipografia de marca for substituída por fallback;
- um beat for removido/encurtado a ponto de mudar a leitura;
- produto real virar ícone/placeholder sem autorização;
- logo for aproximado ou redesenhado;
- o renderer trocar o design em vez de portar o design.

**Render técnico bem-sucedido não significa QA visual aprovado.**
