# Convenção de nomes e pastas

## Uma pasta por peça

`outputs/<slug>/` — o slug descreve a peça, sem data, formato ou versão no nome.

Exemplo: `outputs/cdf-mix-produtos/`, `outputs/esteira-b55-black-november/`

Todos os formatos da peça (feed, stories, etc.) ficam na mesma pasta.

## Estrutura

```text
outputs/<slug>/
  <slug>_feed-4x5_vNN.mp4        entregáveis da versão ATUAL
  <slug>_feed-4x5_vNN.gif
  <slug>_stories-9x16_vNN.mp4
  <slug>_stories-9x16_vNN.gif
  projeto/<formato>.tsrct        projetos editáveis
  Storyboards/                  variantes e storyboard da versão
  Stills/                       stills aprovados antes do motion
  Renders/                      renders e intermediários retidos
  Source/                       código/fonte específico do job
  request.json                  parâmetros e fontes versionados
  previews/filmstrip_<formato>.png
  brief.md                       brief vigente
  offer.json                     snapshot comercial usado
  notes.md                       mudanças, decisões, conflitos da versão
  build_snapshot.py              cópia do gerador que produziu a versão
  versao.txt                     vNN atual
  versoes/vNN/                   versões anteriores, mesma estrutura, incluindo snapshot da oferta
  .tesseract-work/<formato>/     intermediários (fora do git)
```

A raiz contém **somente** a versão atual. Nunca criar pasta nova por formato ou por versão.

## Formatos

| Tag | Canvas |
|---|---|
| `feed-4x5` | 1080×1350 |
| `stories-9x16` | 1080×1920 |
| `quadrado-1x1` | 1080×1080 |

## Versões

- Ajuste fino pedido sobre a versão atual → regravar a mesma `vNN` no lugar.
- Mudança de conceito, nova oferta ou pedido explícito de nova versão → arquivar a atual em `versoes/vNN` e criar `vNN+1` (`--nova-versao` nos builders; `python scripts/lab_versions.py --slug <slug> --new-version` prepara um job genérico).
- Versões arquivadas não são editadas nem sobrescritas.

## Variações (testes A/B)

Variação de hipótese é um formato extra dentro da mesma peça, com sufixo: `<slug>_feed-4x5_hook-b_vNN.mp4` (`_hook-a`, `_hook-b`, `_cta-a`, `_price-focus`, `_benefit-focus`).

Evite nomes como `final-final2.mp4`.
