# Agent instructions — Tesseract Creative Lab

Você está em um laboratório de produção de criativos de performance para e-commerce, com foco atual na Casa do Fitness.

O objetivo é produzir peças editáveis e verificáveis, não demonstrar uma ferramenta específica. Tesseract, HyperFrames e Remotion são renderers disponíveis; escolha a rota que melhor atende ao job.

## Antes de qualquer criação

Leia, nesta ordem:
1. `docs/WORKFLOW.md`
2. `docs/RENDERER-ROUTING.md`
3. `docs/OFFER-TRUTH.md`
4. `docs/QA-PAID-MEDIA.md`
5. `docs/COMPOSITION-QA.md` quando aplicável
6. `docs/MOTION-GRAMMAR.md` para vídeo/motion
7. `docs/COPY-GUARDRAILS.md`
8. `docs/REFERENCE-SOURCES.md` quando houver referência
9. o brief específico
10. o snapshot comercial associado, quando existir
11. `docs/REFERENCE-DIRECTION.md` se houver referências

Inspecione visualmente os assets autorizados.

## Regras obrigatórias

- Não invente fatos comerciais ou técnicos.
- Não gere substituto de IA para um produto real quando o asset real estiver disponível.
- Não altere cor, proporção, componentes ou características do produto.
- Não redesenhe logos.
- Nunca calcule ou assuma desconto, parcela, PIX, frete, cupom, urgência ou estoque sem fonte.
- Se a fonte estiver ausente ou conflitante, omita a afirmação ou registre o conflito.
- Preserve assets originais e projetos anteriores.
- Priorize legibilidade mobile e hierarquia de performance.
- Mantenha elementos editáveis sempre que o renderer permitir.
- Referências podem orientar pacing, enquadramento, densidade, tipografia, câmera e transições. Não copie marca, copy, música, ilustrações proprietárias ou uma sequência inteira frame a frame.
- Antes de animação final, gere **3 direções de storyboard** com hipóteses realmente diferentes.
- Depois da escolha de direção, gere **um still por cena** e corrija composição antes de animar.
- Durante a revisão, prefira notas específicas de direção: tempo, escala, eixo, corte, câmera, easing, foco e hierarquia. Evite "make it better".

## Fonte da verdade

Ordem:
1. instrução explícita do usuário para a campanha;
2. snapshot comercial versionado;
3. informação claramente presente no asset autorizado;
4. omitir.

Registre timestamp/URL quando usar dados capturados de página.

## Roteamento de renderer

Para inspecao, cortes, montagem, legendas, audio, exportacao e QA de arquivos, leia `.agents/skills/ffmpeg-skill/SKILL.md` e `docs/FFMPEG-SKILL.md`. Use `python scripts/ffmpeg_skill.py <ferramenta> <argumentos>` no Windows. A skill complementa os renderers e segue as regras comerciais e de composicao deste Lab.

Use `docs/RENDERER-ROUTING.md`.

Resumo:
- **Tesseract**: footage real, compositing, máscaras, retiming, edição/acabamento.
- **HyperFrames**: motion design determinístico, HTML/CSS/GSAP, iteração rápida e snapshots.
- **Remotion**: React, componentes, parametrização, lotes e templates multi-formato.
- **Hybrid**: gere motion programático e finalize/componha no Tesseract.
- **21st.dev**: biblioteca opcional para cenas que representem produto de software/UI. Não é requisito para anúncios de produto físico.

Não force um renderer só porque está instalado.

## Fluxo obrigatório

1. Verifique ambiente com `scripts/check-environment.ps1`.
2. Leia brief + snapshot + request.
3. Inspecione assets e referências.
4. Decomponha referências em atributos, não em cópia literal.
5. Gere 3 storyboards.
6. Se não houver escolha humana explícita, selecione a direção que melhor satisfaz o brief e registre a justificativa factual em `notes.md`.
7. Gere stills de todas as cenas.
8. Corrija storyboard/composição antes de animar.
9. Escolha renderer e registre a decisão.
10. Construa a master.
11. Gere preview/filmstrip/snapshots adequados ao renderer.
12. Rode o Creative Critic com `prompts/creative-critic.txt` e corrija flags `block`/`revise` justificadas.
13. Faça QA visual e comercial.
14. Aplique notas de direção específicas.
15. Exporte master.
16. Só então crie adaptações 9:16, 4:5 e 1:1 e variações de hipótese.
17. Retenha brief, snapshot, storyboard, stills, projeto/código e notas.

## Particularidades por renderer

### Tesseract
- Rode localmente em ambiente suportado.
- Use as skills oficiais e a versão de CLI disponível.
- Nunca edite `.tsrct` como JSON/ZIP bruto.
- Use comandos de projeto suportados pelo CLI.
- Gere preview e filmstrip antes do MP4.

### HyperFrames
- Requer Node.js 22+ e FFmpeg.
- Use as skills oficiais (`npx hyperframes skills update`).
- Rode `npx hyperframes doctor`.
- Antes de construir um efeito do zero, pesquise o catálogo.
- Rode lint/check/snapshot antes do render.
- Prefira mídia local congelada no job para evitar drift de URL.

### Remotion
- Use as skills oficiais do Remotion.
- Mantenha componentes parametrizáveis e dados comerciais fora do markup quando possível.
- Gere stills/Studio preview antes do render final.
- Use Remotion quando a reutilização do template, React ou batch rendering tiver vantagem real.

## Cloud render

Quando o projeto puder ser renderizado por HyperFrames ou Remotion em Linux, ele deve nascer cloud-renderable.

- Leia `docs/CLOUD-RENDER.md`.
- Gere `outputs/<slug>/cloud-render.sh` junto com o código da peça.
- O script deve respeitar `CREATIVE_FORMAT` e `CREATIVE_QUALITY`.
- O output obrigatório é `.cloud-render/preview.mp4`.
- Não dependa de Tesseract CLI no GitHub Actions.
- Não busque assets voláteis durante o render; use mídia congelada/versionada no job.
- Preview prioriza iteração; final só depois dos gates de QA.
- O workflow deve conseguir gerar poster, filmstrip e metadata sem intervenção manual.

## Variações

Depois da master:
- mude uma hipótese por vez;
- registre exatamente o que mudou;
- adapte composição por aspect ratio em vez de esticar/cortar;
- preserve a fonte comercial da master.

## Entrega

Estrutura obrigatória em `docs/NAMING.md`: **uma pasta por peça** (`outputs/<slug>/`), todos os formatos juntos, raiz só com a versão atual e anteriores em `versoes/vNN/`. Nunca crie pasta nova por formato ou versão.

A versão final deve conter, quando aplicável:
- entregáveis atuais `<slug>_<formato>_vNN.mp4` (e `.gif` se pedido);
- projeto editável (`projeto/<formato>.tsrct` ou código do renderer);
- `Storyboards/storyboard.json` e `Stills/`;
- previews/filmstrips;
- `brief.md`, `request.json`, `offer.json`, `notes.md` e `versao.txt`.

Ajuste fino regrava a versão atual; nova versão arquiva a atual em `versoes/vNN/` usando `scripts/lab_versions.py`.

Ao final, informe:
- renderer usado;
- MP4;
- projeto/código editável;
- fontes de verdade;
- referências usadas e quais atributos foram extraídos;
- variação/hipótese;
- limitações ou conflitos.
