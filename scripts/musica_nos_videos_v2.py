"""Mistura a trilha original nos 6 vídeos atuais (B2B x4 + carrossel x2) e atualiza pecas/videos-com-trilha/ (versões antigas vão para versoes/)."""
import json, shutil, subprocess, time
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
PECAS = LAB.parent / "pecas"
TRILHA = LAB / "assets" / "audio" / "trilha-simples-20s.wav"
DEST = PECAS / "videos-com-trilha"
CAR = LAB / "outputs" / "carrossel-pinheiros-cenarios"
B2B = PECAS / "b2b-generalista-projetos"
ORIGENS = {
    B2B / "feed/feed_animado_60fps_1080x1080.mp4": "b2b-generalista_feed-1080x1080_texto-animado.mp4",
    B2B / "feed/feed_video-fundo_60fps_1080x1080.mp4": "b2b-generalista_feed-1080x1080_fundo-animado.mp4",
    B2B / "stories/stories_animado_60fps_1080x1920.mp4": "b2b-generalista_stories-1080x1920_texto-animado.mp4",
    B2B / "stories/stories_video-fundo_60fps_1080x1920.mp4": "b2b-generalista_stories-1080x1920_fundo-animado.mp4",
    CAR / "carrossel-pinheiros-cenarios_feed-1x1_v11.mp4": "carrossel-pinheiros_feed-1080x1080_tesseract.mp4",
    CAR / "carrossel-pinheiros-cenarios_stories-9x16_v11.mp4": "carrossel-pinheiros_stories-1080x1920_tesseract.mp4",
}

ORIGENS = {k: v for k, v in ORIGENS.items() if 'carrossel' in v}   # só o carrossel mudou (v10)

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(p)],capture_output=True,text=True,check=True).stdout and json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(p)],capture_output=True,text=True).stdout)["format"]["duration"])

stamp = time.strftime("%Y%m%d_%H%M")
(DEST / "versoes").mkdir(exist_ok=True)
tmp = DEST / "_novos"; tmp.mkdir(exist_ok=True)
for src, nome in ORIGENS.items():
    d = dur(src)
    af = f"volume=1.3dB,afade=t=in:st=0:d=0.15,afade=t=out:st={max(d-1,0):.3f}:d=1.0"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-i",str(TRILHA),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-af",af,"-t",f"{d:.3f}","-movflags","+faststart",str(tmp/nome)],check=True)
    assert abs(dur(tmp/nome) - d) < 0.15
for nome in ORIGENS.values():
    atual = DEST / nome
    if atual.exists():
        shutil.move(str(atual), str(DEST / "versoes" / f"{atual.stem}_antes-{stamp}.mp4"))
    shutil.move(str(tmp / nome), str(atual))
tmp.rmdir()
for nome in ORIGENS.values():
    print(nome, round((DEST/nome).stat().st_size/1e6,1), "MB")
