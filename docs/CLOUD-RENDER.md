# Cloud render

O GitHub Actions é o ambiente cloud do Lab para HyperFrames e Remotion. Tesseract CLI continua reservado ao fluxo local/híbrido quando o job exigir footage, máscaras, retiming ou acabamento específico.

## Contrato

Um criativo cloud-renderable deve incluir:

    outputs/<slug>/cloud-render.sh

O script recebe estas variáveis:

- CREATIVE_SLUG
- CREATIVE_FORMAT: 9x16, 4x5 ou 1x1
- CREATIVE_QUALITY: preview ou final
- TESSERACT_CLOUD=1

E deve produzir obrigatoriamente:

    .cloud-render/preview.mp4

O workflow completa o bundle com poster.jpg, filmstrip.jpg, metadata.json e summary.md.

## Como visualizar

1. Abra Actions no GitHub.
2. Escolha Cloud Render Preview.
3. Clique em Run workflow.
4. Informe o slug, formato e preview/final.
5. Abra a execução concluída.
6. Em Artifacts, baixe tesseract-<slug>-<formato>-<quality>.
7. Extraia e reproduza preview.mp4. No celular, o MP4 é o caminho mais direto; filmstrip.jpg serve para revisão rápida de composição.

## Regra para agentes

Quando Claude Code/Codex criar um projeto HyperFrames ou Remotion destinado à nuvem, ele também deve gerar cloud-render.sh. O script deve instalar apenas dependências do projeto, usar assets versionados e renderizar deterministicamente para o caminho exigido.

Preview deve priorizar velocidade. Final pode aumentar bitrate, subframes/motion blur e QA.

Artifacts são o baseline porque funcionam mesmo em repositório privado. Uma galeria pública/Pages deve ser uma etapa separada e somente para peças explicitamente publicáveis.
