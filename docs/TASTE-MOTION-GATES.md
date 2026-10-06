# Taste + Motion Gates

Camada de direção e QA de motion do Tesseract Creative Lab. Ela absorve ideias úteis do motionmaxxing, mas foi adaptada para **performance ads de produto físico**. Os números abaixo são guardrails e sinais de revisão, não leis de estilo.

## Princípios

1. **Uma ideia por filme.** Efeito não substitui conceito.
2. **Um herói por frame.** Produto, prova ou mensagem principal domina a atenção.
3. **Produto real como prova.** Asset oficial tem prioridade sobre abstração ou UI inventada.
4. **Mundo construído.** Fundo = superfície + luz + profundidade/textura quando isso combina com a marca; não apenas uma cor chapada.
5. **Cada beat compra algo.** Storyboards de vídeo devem declarar `buys`: o que o espectador passa a entender depois daquele beat.
6. **Movimento tem função.** Entrada, saída, câmera e transição orientam foco, continuidade ou ritmo.
7. **Hardest beat first.** Construa e valide o momento visual mais difícil antes de terminar o filme.
8. **Landing desacelera; saída pode acelerar.** Bom default, nunca obrigação.
9. **Corte em movimento quando fizer sentido.** Evite o padrão repouso -> fade -> repouso em todos os beats.
10. **Marca premium não precisa gritar.** Para high-end, menos texto, mais produto, matéria, luz e silêncio podem carregar mais valor que HUDs e slogans.

## Anti-slop: sinais que exigem justificativa

O Creative Critic deve marcar quando aparecem sem função clara:

- brand/scene label permanente em canto;
- contador decorativo `01 / 05`, timecode, FPS/BPM/resolução;
- progress bar decorativa;
- kicker/eyebrow em caixa alta sobre toda headline;
- layout persistente "headline esquerda + card/produto direita";
- cards genéricos de UI, status dots, skeletons e dashboards inventados;
- headline digitada letra a letra fora de uma interação real;
- card pequeno flutuando em fundo vazio por vários segundos;
- transição quase sempre baseada em opacity/fade;
- mesmo objeto preso nas mesmas coordenadas por vários beats;
- sequência de slogans sem ganho de informação;
- CTA tipo rodapé de site segurado tempo demais;
- grain/glow/chrome/3D aplicado apenas porque "parece premium".

Simplicidade não é slop. Um quadro quase parado pode ser excelente se houver intenção, hierarquia e duração adequadas.

## Gates M0–M7

### M0 — Render válido — automático

O arquivo precisa decodificar, ter vídeo e duração positiva.

```bash
python scripts/motion_quality.py final.mp4 --json-out motion-qa.json
```

### M1 — Produto/prova legível — manual

No contact sheet e nos mid-change frames:
- produto/prova reconhecível em mobile;
- detalhe importante não depende de zoom mental;
- packshot não foi deformado, recolorido ou substituído;
- UI de equipamento é real ou explicitamente declarada como ilustração.

### M2 — Sem freeze acidental — automático + manual

`motion_quality.py` mede runs de frames quase idênticos. Default: **review** quando passa de 0,75 s.

Aceite stillness desenhada somente quando ela estiver anotada em `notes.md`. O gate existe para pegar render travado, animação que terminou cedo ou frame morto esquecido.

### M3 — Fechamento proporcional — automático + manual

O script estima o hold final. Default: **review** acima de 1,4 s.

Um final premium pode resolver em stillness, mas não deve parecer que o vídeo acabou e continuou tocando.

### M4 — Um herói por frame — manual

Dois assuntos fortes só convivem com hierarquia inequívoca. Em produto físico, equipamento costuma ser o herói; copy, preço ou condição entram como suporte quando o job exigir.

### M5 — Anti-page-chrome — fonte + manual

Rode o critic sobre o HTML/React/projeto e o contact sheet. Page chrome/HUD genérico, progress bar, contador, kicker, card de UI e typing gratuito devem ser eliminados ou justificados.

### M6 — Mundo coerente — manual

Cheque ground, luz, profundidade, textura e material. A peça não precisa ser "cinematográfica"; precisa parecer intencional e coerente com a marca.

### M7 — Beat buys — storyboard

Cada beat de vídeo registra:
- `role`: hook | proof | turn | close;
- `buys`: informação/crença adquirida;
- `hero`: assunto principal;
- `entry`, `exit`, `handoff`.

Se dois beats compram a mesma coisa, um deles provavelmente é redundante.

## Revisão obrigatória de frames

Para vídeo/motion:
1. renderize preview;
2. gere filmstrip/contact sheet;
3. observe pelo menos um frame intermediário por transição;
4. descreva cada frame principal em uma frase: **o que vejo / qual é o herói / isso parece slide?**;
5. rode M0/M2/M3;
6. julgue M1/M4/M5/M6;
7. corrija `block` e `revise` antes do final.

## A/B e taste

Quando houver duas soluções plausíveis, prefira comparação cega. Registre feedback do usuário em `notes.md` ou arquivo de taste do job como:

```text
data · job · versão A/B · preferência · motivo observável · regra estreita
```

Não generalize uma preferência local para todos os trabalhos.

## O que NÃO importar do motionmaxxing

- house style;
- eases/tempos como metas universais;
- estética SaaS/UI como padrão;
- regra de "movimento em quase todo frame" para filmes premium;
- 3D, grain, chrome ou color flood como assinatura fixa.

O Lab usa esses conceitos como ferramentas de direção e QA, preservando a gramática própria de cada marca.
