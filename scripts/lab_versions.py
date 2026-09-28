"""Layout de saída do lab: uma pasta por peça, raiz = versão atual, anteriores em versoes/.

outputs/<slug>/
  <slug>_<formato>_vNN.mp4|.gif    entregáveis da versão atual (todos os formatos)
    projeto/<formato>.tsrct          projetos editáveis
    Storyboards/ Stills/ Renders/ Source/ request.json
  previews/filmstrip_<formato>.png
  brief.md  offer.json  notes.md  build_snapshot.py  versao.txt
  versoes/vNN/                     versões anteriores, mesma estrutura
  .tesseract-work/<formato>/       intermediários (ignorado no git)
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ARCHIVED = (
    "projeto",
    "Storyboards",
    "Stills",
    "Renders",
    "Source",
    "previews",
    "fonts",
    "brief.md",
    "request.json",
    "offer.json",
    "notes.md",
    "build_snapshot.py",
    "versao.txt",
)


def _is_link(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or (is_junction is not None and is_junction())


def current_version(root: Path) -> int:
    f = root / "versao.txt"
    if _is_link(f):
        raise SystemExit(f"Não vou ler versão através de link/junction: {f}")
    return int(f.read_text(encoding="utf-8").strip().lstrip("v")) if f.exists() else 0


def archive_current(root: Path, slug: str) -> int:
    """Move a versão atual para versoes/vNN e devolve o número da próxima versão."""
    if _is_link(root) or _is_link(root.parent):
        raise SystemExit(f"Não vou arquivar através de link/junction: {root}")
    n = current_version(root)
    if n == 0:
        return 1
    request_source = root / "request.json"
    request_data = None
    if request_source.exists():
        import json

        if _is_link(request_source):
            raise SystemExit(f"Não vou arquivar request.json por link/junction: {request_source}")
        request_data = json.loads(request_source.read_text(encoding="utf-8-sig"))
        if not isinstance(request_data, dict):
            raise SystemExit(f"{request_source} deve conter um objeto JSON; versão atual não foi movida.")
        snapshot = request_data.get("offer_snapshot")
        if snapshot is not None and not isinstance(snapshot, str):
            raise SystemExit(f"offer_snapshot deve ser texto; versão atual não foi movida.")
    version_outputs = list(root.glob(f"{slug}_*_v{n:02d}.*"))
    archive_sources = [root / name for name in ARCHIVED if name != "brief.md"]
    if any(_is_link(path) for path in [*version_outputs, *archive_sources]):
        raise SystemExit(f"Não vou arquivar arquivos ou pastas por links/junctions em {root}.")
    dest = root / "versoes" / f"v{n:02d}"
    if _is_link(root / "versoes"):
        raise SystemExit(f"Não vou arquivar através de link/junction: {root / 'versoes'}")
    if _is_link(dest):
        raise SystemExit(f"Não vou sobrescrever versão arquivada por link/junction: {dest}")
    if dest.exists():
        raise SystemExit(f"{dest} já existe; não vou sobrescrever uma versão arquivada.")
    dest.mkdir(parents=True)
    for f in version_outputs:
        shutil.move(str(f), dest / f.name)
    for name in ARCHIVED:
        src = root / name
        if src.name == "brief.md" and src.exists():
            shutil.copy(src, dest / name)  # brief continua valendo para a próxima
        elif src.exists():
            shutil.move(str(src), dest / name)
    request = dest / "request.json"
    if request.exists() and request_data is not None:
        import json

        snapshot = request_data.get("offer_snapshot")
        if snapshot:
            snapshot_path = Path(snapshot)
            if not snapshot_path.is_absolute() and snapshot_path.parts[:2] == ("outputs", slug):
                relative_snapshot = Path(*snapshot_path.parts[2:])
                request_data["offer_snapshot"] = str(
                    Path("outputs") / slug / "versoes" / f"v{n:02d}" / relative_snapshot
                ).replace("\\", "/")
        request.write_text(json.dumps(request_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        next_request = dict(request_data)
        if snapshot:
            next_request["offer_snapshot"] = snapshot
        (root / "request.json").write_text(
            json.dumps(next_request, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return n + 1


def prepare(root: Path, slug: str, new_version: bool) -> int:
    """Garante a estrutura e decide a versão: regrava a atual ou abre a próxima."""
    if _is_link(root) or _is_link(root.parent):
        raise SystemExit(f"Não vou preparar uma peça através de link/junction: {root}")
    root.mkdir(parents=True, exist_ok=True)
    n = archive_current(root, slug) if new_version else max(current_version(root), 1)
    request = root / "request.json"
    if new_version and not request.exists():
        import json

        template = Path(__file__).resolve().parents[1] / "schemas" / "creative-request.example.json"
        data = json.loads(template.read_text(encoding="utf-8"))
        data["product_slug"] = slug
        data["offer_snapshot"] = f"outputs/{slug}/offer.json"
        data["assets_dir"] = f"assets/{slug}"
        data["references"] = []
        request.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for d in (
        "projeto",
        "Storyboards",
        "Stills",
        "Renders",
        "Source",
        "previews",
        ".tesseract-work",
    ):
        (root / d).mkdir(exist_ok=True)
    for f in root.glob(f"{slug}_*_v{n:02d}.*"):
        f.unlink()  # só arquivos gerados da própria versão que está sendo regravada
    (root / "versao.txt").write_text(f"v{n:02d}\n", encoding="utf-8")
    return n


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or archive a Tesseract Creative Lab output version.")
    parser.add_argument("--slug", required=True, help="Piece slug used by the output folder")
    parser.add_argument("--new-version", action="store_true", help="Archive the current version and prepare the next one")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug) or re.fullmatch(
        r"(?:con|prn|aux|nul|com[1-9]|lpt[1-9])", args.slug
    ):
        parser.error("slug invalido: use letras minusculas, numeros e hifens; nomes reservados do Windows nao sao permitidos")
    root = Path("outputs") / args.slug
    version = prepare(root, args.slug, new_version=args.new_version)
    print(f"Prepared {root} v{version:02d}")


if __name__ == "__main__":
    main()
