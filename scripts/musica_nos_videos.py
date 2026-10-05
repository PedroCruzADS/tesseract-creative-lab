"""Mistura a trilha simples (assets/audio/trilha-simples-17s.wav) nos vídeos de pecas/ e reúne tudo em pecas/videos-com-trilha/.

O vídeo não é recodificado (-c:v copy): só entra o áudio AAC, ajustado à duração de cada vídeo, com fade de saída de 1 s e ganho para -16 LUFS.
Os arquivos originais (sem áudio) são movidos para a pasta nova com o nome ajustado, depois de conferido o resultado.

Uso: python scripts/musica_nos_videos.py
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
PECAS = LAB.parent / "pecas"
TRILHA = LAB / "assets" / "audio" / "trilha-simples-17s.wav"
DESTINO = PECAS / "videos-com-trilha"
GANHO_DB = 1.3          # leva a trilha de -17,3 LUFS para cerca de -16 LUFS (pico fica abaixo de -1,5 dBFS)

ORIGENS = {  # arquivo atual -> nome novo
    "b2b-generalista-projetos/feed/feed_animado_60fps_1080x1080.mp4": "b2b-generalista_feed-1080x1080_texto-animado.mp4",
    "b2b-generalista-projetos/feed/feed_video-fundo_60fps_1080x1080.mp4": "b2b-generalista_feed-1080x1080_fundo-animado.mp4",
    "b2b-generalista-projetos/stories/stories_animado_60fps_1080x1920.mp4": "b2b-generalista_stories-1080x1920_texto-animado.mp4",
    "b2b-generalista-projetos/stories/stories_video-fundo_60fps_1080x1920.mp4": "b2b-generalista_stories-1080x1920_fundo-animado.mp4",
    "carrossel-pinheiros-tesseract/feed/carrossel-pinheiros_tesseract_feed_1080x1080_v07.mp4": "carrossel-pinheiros_feed-1080x1080_tesseract.mp4",
    "carrossel-pinheiros-tesseract/stories/carrossel-pinheiros_tesseract_stories_1080x1920_v07.mp4": "carrossel-pinheiros_stories-1080x1920_tesseract.mp4",
    "carrossel-pinheiros-video/feed/carrossel-pinheiros_feed_1080x1080.mp4": "carrossel-pinheiros_feed-1080x1080_fotos-originais.mp4",
    "carrossel-pinheiros-video/stories/carrossel-pinheiros_stories_1080x1920.mp4": "carrossel-pinheiros_stories-1080x1920_fotos-originais.mp4",
}


def duracao(arq: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(arq)], capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def main() -> None:
    DESTINO.mkdir(exist_ok=True)
    feitos = []
    for rel, novo in ORIGENS.items():
        src = PECAS / rel
        if not src.exists():
            print("não achei:", rel)
            continue
        dur = duracao(src)
        saida = DESTINO / novo
        af = f"volume={GANHO_DB}dB,afade=t=in:st=0:d=0.15,afade=t=out:st={max(dur - 1.0, 0):.3f}:d=1.0"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-i", str(TRILHA), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-af", af, "-t", f"{dur:.3f}", "-movflags", "+faststart", str(saida)], check=True)
        feitos.append((src, saida, dur))
        print(f"{novo}  {dur:.1f} s  {saida.stat().st_size // 1024} KB")
    # confere: vídeo com 1 faixa de vídeo e 1 de áudio, mesma duração
    for src, saida, dur in feitos:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(saida)],
                           capture_output=True, text=True, check=True)
        tipos = [linha.strip() for linha in r.stdout.strip().splitlines()]
        assert sorted(tipos) == ["audio", "video"], (saida.name, tipos)
        assert abs(duracao(saida) - dur) < 0.15, (saida.name, duracao(saida), dur)
    for src, _, _ in feitos:
        src.unlink()
    print("originais sem áudio removidos das pastas de origem:", len(feitos))


if __name__ == "__main__":
    main()
