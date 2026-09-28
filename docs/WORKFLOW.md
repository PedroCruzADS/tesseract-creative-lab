# Workflow de produção

## 1. Fonte da verdade
Toda peça deve nascer de fontes verificáveis: assets locais, URL do produto, dados comerciais fornecidos pelo usuário ou snapshot salvo em `data/`.

Nunca inferir preço, desconto, parcelamento, frete, estoque, cupom ou benefício.

## 2. Ingestão
1. Criar uma pasta de trabalho com `scripts/new-creative.ps1`.
2. Salvar assets em `assets/<slug>/`.
3. Se houver URL, gerar snapshot com `scripts/product_snapshot.py`.
4. Preencher o brief usando `briefs/TEMPLATE.md`.

## 3. Produção
- aplicar a grade e o gate visual de `docs/COMPOSITION-QA.md` para cada formato;
- abrir no Claude Code/Codex;
- ler `AGENTS.md`;
- instalar/verificar Tesseract;
- criar `.tsrct`;
- importar assets reais;
- montar a peça;
- gerar preview + filmstrip;
- revisar;
- exportar MP4.

## 4. Variações
Depois de aprovar a master:
- variar hook;
- variar headline;
- variar CTA;
- adaptar 9:16, 4:5 e 1:1;
- preservar produto e condições.

## 5. Entrega
Uma pasta por peça em `outputs/<slug>/`, com todos os formatos juntos (ver `docs/NAMING.md`):
- MP4 (e GIF, se pedido) de cada formato na raiz: `<slug>_<formato>_vNN.mp4`;
- projetos `.tsrct` em `projeto/`;
- filmstrips em `previews/`;
- brief, snapshot comercial (`offer.json`) e notas da versão.

Ajustes finos regravam a versão atual. Nova versão arquiva a atual em `versoes/vNN/`.
