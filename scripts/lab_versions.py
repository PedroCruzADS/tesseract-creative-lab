"""Layout de saída do lab: uma pasta por peça, raiz = versão atual, anteriores em versoes/.

outputs/<slug>/
  <slug>_<formato>_vNN.mp4|.gif    entregáveis da versão atual (todos os formatos)
  projeto/<formato>.tsrct          projetos editáveis
  previews/filmstrip_<formato>.png
  brief.md  offer.json  notes.md  build_snapshot.py  versao.txt
  versoes/vNN/                     versões anteriores, mesma estrutura
  .tesseract-work/<formato>/       intermediários (ignorado no git)
"""
from __future__ import annotations

import shutil
from pathlib import Path

ARCHIVED = ("projeto", "previews", "fonts", "brief.md", "offer.json", "notes.md",
            "build_snapshot.py", "versao.txt")


def current_version(root: Path) -> int:
    f = root / "versao.txt"
    return int(f.read_text(encoding="utf-8").strip().lstrip("v")) if f.exists() else 0


def archive_current(root: Path, slug: str) -> int:
    """Move a versão atual para versoes/vNN e devolve o número da próxima versão."""
    n = current_version(root)
    if n == 0:
        return 1
    dest = root / "versoes" / f"v{n:02d}"
    if dest.exists():
        raise SystemExit(f"{dest} já existe; não vou sobrescrever uma versão arquivada.")
    dest.mkdir(parents=True)
    for f in root.glob(f"{slug}_*_v{n:02d}.*"):
        shutil.move(str(f), dest / f.name)
    for name in ARCHIVED:
        src = root / name
        if src.name == "brief.md" and src.exists():
            shutil.copy(src, dest / name)  # brief continua valendo para a próxima
        elif src.exists():
            shutil.move(str(src), dest / name)
    return n + 1


def prepare(root: Path, slug: str, new_version: bool) -> int:
    """Garante a estrutura e decide a versão: regrava a atual ou abre a próxima."""
    root.mkdir(parents=True, exist_ok=True)
    n = archive_current(root, slug) if new_version else max(current_version(root), 1)
    for d in ("projeto", "previews", ".tesseract-work"):
        (root / d).mkdir(exist_ok=True)
    for f in root.glob(f"{slug}_*_v{n:02d}.*"):
        f.unlink()  # só arquivos gerados da própria versão que está sendo regravada
    (root / "versao.txt").write_text(f"v{n:02d}\n", encoding="utf-8")
    return n
