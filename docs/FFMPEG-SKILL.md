# FFmpeg no Lab

A [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) faz inspecao, cortes, montagem, legendas, audio, exportacao e verificacao local. Use para preparar footage e finalizar arquivos renderizados pelo Lab.

## Instalacao vigente

- Versao: `2.5.1`.
- Commit: `008333aaf6722083392eb6bd8bd67b59884a2a26`.
- Fonte completa: `.agents/skills/ffmpeg-skill/`, incluindo scripts, templates, referencias e licenca MIT.
- Codex: descoberta em `.agents/skills/` ao trabalhar no Lab.
- Workspace Ads: `.agents/skills/ffmpeg-skill` tambem aponta para a instalacao do Lab, permitindo descoberta a partir da raiz compartilhada.
- Claude: `.claude/skills/ffmpeg-skill` aponta para a mesma instalacao.

Leia `.agents/skills/ffmpeg-skill/SKILL.md` antes de usar os scripts. No Windows, o ponto de entrada abaixo usa o Python atual e preserva argumentos com espacos.

```powershell
python scripts/ffmpeg_skill.py probe "outputs/peca/peca_stories-9x16_v01.mp4" --compact
python scripts/ffmpeg_skill.py cut "entrada.mp4" --start 0 --end 3 -o "outputs/peca/previews/corte.mp4" --dry-run --json
python scripts/ffmpeg_skill.py check "outputs/peca/peca_stories-9x16_v01.mp4" --platform reels --json
python scripts/ffmpeg_skill.py look "outputs/peca/peca_stories-9x16_v01.mp4" --tiles 3x2
```

Para diagnosticar capacidades ou uma falha do ambiente:

```powershell
python scripts/ffmpeg_skill.py doctor --json
```

## Uso no fluxo criativo

1. Inspecione o arquivo antes de planejar cortes, crop, audio ou exportacao.
2. Planeje a operacao com `--dry-run --json`; use `render` com projeto JSON para tres ou mais etapas.
3. Preserve os originais. Escreva resultados nas pastas do job conforme `docs/NAMING.md`.
4. Confira duracao, resolucao, fps, codecs e audio. Se a imagem mudou, gere uma contact sheet e examine os frames.

As regras de marca, verdade comercial, storyboard, composicao e QA do Lab continuam valendo. Para Stories, mantenha a reserva de 250 px no header e footer definida no job; um preset social nao comprova esse espacamento. Preserve 60 fps quando o brief pedir: confira os parametros do preset antes de exportar. Gere GIF somente quando solicitado.

A skill executa operacoes de midia. Direcao visual e escolha de renderer seguem `docs/RENDERER-ROUTING.md`. Os scripts antigos do Lab continuam disponiveis; esta instalacao nao muda renders anteriores.

Atualizacoes devem ser deliberadas, com novo commit registrado e verificacao no ambiente local. A copia instalada nao acompanha `main` automaticamente.
