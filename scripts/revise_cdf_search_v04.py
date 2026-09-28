"""Vertical CDF search film v04, built natively with the local Tesseract CLI."""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

from animate_cdf_search import sound
from build_cdf_mix import Builder, EASE_INOUT, EASE_OUT, LINEAR, grad, keys, tr
from build_cdf_search_storyboard import BRAND, LAB, OUT, PRODUCTS, RED, run

WORK = OUT / ".tesseract-work" / "v04"
PROJECT = WORK / "stories-9x16-v04.tsrct"
FINAL = OUT / "cdf-busca-categorias_stories-9x16_v04.mp4"
BLACK = [0.055, 0.055, 0.065, 1]
GREY = [0.43, 0.44, 0.47, 1]
WHITE = [1, 1, 1, 1]
PAPER = [0.975, 0.97, 0.965, 1]
ROSE = [0.976, 0.90, 0.91, 1]
SLATE = [0.88, 0.89, 0.90, 1]
DURATION = 19.0


def add_image(doc, asset, lid, name, start, duration, x, y, size, scale):
    doc["composition"]["layers"].insert(0, {
        "type": "Image", "id": lid, "name": name,
        "activeRange": {"start": start, "duration": duration},
        "transform": tr(x, y, (size / 2, size / 2), scale),
        "source": {"assetId": asset, "fit": "contain"},
    })


def archive_v03():
    folder = OUT / "versoes" / "v03"
    for rel in (
        "cdf-busca-categorias_quadrado-1x1_v03.mp4",
        "projeto/quadrado-1x1.tsrct",
        "previews/filmstrip_quadrado-1x1.png",
        "brief.md", "notes.md", "versao.txt",
    ):
        src, dst = OUT / rel, folder / rel
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def build():
    archive_v03()
    WORK.mkdir(parents=True, exist_ok=True)
    (OUT / "previews").mkdir(exist_ok=True)
    if PROJECT.exists():
        raise RuntimeError(f"Work project already exists: {PROJECT}")
    run("project", "create", "--project", str(PROJECT))
    fonts = {}
    for key, filename in (("bold", "BaiJamjuree-Bold"),
                          ("semibold", "BaiJamjuree-SemiBold"),
                          ("medium", "BaiJamjuree-Medium")):
        r = json.loads(run("project", "import-font", "--project", str(PROJECT),
                           "--file", str(BRAND / "fonts" / f"{filename}.ttf")).strip().splitlines()[-1])
        face = r["faces"][0]
        fonts[key] = (face.get("typographicFamilyName") or r["fontFamily"],
                      face.get("typographicStyleName") or r["fontStyle"])
    assets = {
        "logo-white": BRAND / "logo" / "logo-header-white.png",
        "treadmill": PRODUCTS / "esteira-speedo-tr7.png",
        "bike": PRODUCTS / "bike-mormaii-motion-s.png",
        "elliptical": PRODUCTS / "eliptico-starke-sh30.png",
        "station": PRODUCTS / "estacao-speedo-multi3.png",
        "dumbbell": LAB / "assets" / "cdf-busca-categorias" / "halter-bowflex-552-par.jpg",
        "rower": LAB / "assets" / "cdf-busca-categorias" / "remo-mormaii-vway.jpg",
    }
    for asset, path in assets.items():
        run("project", "import-asset", "--project", str(PROJECT),
            "--file", str(path), "--asset-id", asset, "--kind", "image")
    edit = WORK / "editable.json"
    run("project", "checkout", "--project", str(PROJECT), "--output", str(edit))
    doc = json.loads(edit.read_text(encoding="utf-8"))
    doc["dimensions"] = {"width": 1080, "height": 1920}
    doc["duration"] = DURATION
    edit.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    run("project", "commit", "--project", str(PROJECT), "--file", str(edit))

    b = Builder(1920, fonts)
    # S1: a single browser/search beat; no redundant opening slogans or pages.
    b.rect(100, "Browser faded backdrop", 0, 4500, 0, 0, 1080, 1920, PAPER,
           gradient=grad(0, 0, 1080, 1920, [(0, WHITE), (.55, [0.965,.95,.95,1]), (1, ROSE)]))
    b.rect(101, "Browser soft red haze", 0, 4500, 750, 1100, 500, 750, ROSE, 250, opacity=20)
    b.rect(102, "Browser shadow", 0, 4500, 72, 350, 936, 1060, SLATE, 53)
    b.rect(103, "Browser window", 0, 4500, 75, 338, 930, 1060, WHITE, 50)
    b.rect(104, "Browser toolbar", 0, 4500, 75, 338, 930, 96, PAPER, 49)
    for lid,x,c in ((105,115,RED),(106,143,SLATE),(107,171,SLATE)):
        b.rect(lid,"Browser control",0,4500,x,377,13,13,c,7)
    b.rect(108,"Address field",0,4500,270,361,603,49,WHITE,24)
    b.text(109,"Address",0,4500,300,367,548,37,"Pesquisar", "medium",25,GREY)
    b.text(110,"Browser eyebrow",0,4500,150,535,780,46,"CASA DO FITNESS", "semibold",30,RED,"center")
    b.text(111,"Browser question",0,4500,130,604,820,156,"Seu próximo treino\ncomeça aqui.","bold",66,BLACK,"center")
    b.rect(112,"Search shadow",0,4500,126,856,828,125,SLATE,59)
    b.rect(113,"Search box",0,4500,130,850,820,125,WHITE,59)
    b.text(114,"Search icon",0,4500,170,882,56,58,">","bold",49,RED)
    phrase = "equipamentos fitness para casa"
    for i in range(1,len(phrase)+1):
        start = 1050 + int((i-1)*84)
        end = 1050 + i*84 if i<len(phrase) else 4440
        b.text(120+i,f"Typed {i}",start,end-start,245,888,660,54,
               phrase[:i],"medium",37,BLACK)
    b.text(160,"Browser supporting",0,4500,155,1050,770,94,
           "Esteiras, bicicletas, musculação, acessórios...", "medium",30,GREY,"center")
    b.rect(161,"Search action",0,4500,369,1220,342,80,RED,39)
    b.text(162,"Search action text",0,4500,370,1236,340,45,"ENCONTRAR", "bold",31,WHITE,"center")

    # S2: six product cards orbit a fixed, branded hub. Four benefits take turns.
    b.rect(200,"Orbit atmospheric background",4500,11100,0,0,1080,1920,PAPER,
           gradient=grad(0,0,1000,1920,[(0,[.985,.97,.97,1]),(.52,[.95,.95,.95,1]),(1,[.92,.88,.89,1])]))
    b.rect(201,"Orbit top haze",4500,11100,-130,220,540,540,ROSE,270,opacity=23)
    b.rect(202,"Orbit bottom haze",4500,11100,720,1180,550,550,ROSE,275,opacity=23)
    b.text(203,"Orbit title",4500,11100,90,303,900,78,"Tudo para se mover.","bold",59,BLACK,"center")
    b.text(204,"Orbit subline",4500,11100,112,386,856,52,
           "Do cardio à força. E muito mais.","medium",31,GREY,"center")
    b.rect(205,"Outer orbit ring",4500,11100,83,501,914,914,[.91,.86,.87,1],457)
    b.rect(206,"Orbit ring inner cutout",4500,11100,87,505,906,906,[.963,.945,.947,1],453)
    b.rect(207,"Hub shadow",4500,11100,282,834,516,246,[.7,.68,.69,1],123,opacity=32)
    b.rect(208,"Hub brand capsule",4500,11100,287,829,506,236,RED,118,
           gradient=grad(287,829,793,1065,[(0,[.98,.12,.17,1]),(1,[.72,.01,.06,1])]))
    b.text(209,"Hub category intro",4500,11100,226,1125,628,50,
           "ESCOLHA O SEU MOVIMENTO", "semibold",28,BLACK,"center")
    orbit = [
        ("treadmill","ESTEIRAS",-90,440,17),
        ("bike","BICICLETAS",-30,467,17),
        ("dumbbell","ACESSÓRIOS",30,1000,16),
        ("station","MUSCULAÇÃO",90,500,15),
        ("rower","REMO",150,1000,16),
        ("elliptical","ELÍPTICOS",210,440,17),
    ]
    anim=[]
    for i,(asset,label,angle,size,scale) in enumerate(orbit):
        rad=math.radians(angle)
        cx=540+421*math.cos(rad)
        cy=957+421*math.sin(rad)
        base=220+i*10
        b.rect(base,"Orbit card shadow",4500,11100,cx-103,cy-102,206,206,[.78,.76,.77,1],44,opacity=34)
        b.rect(base+1,"Orbit card",4500,11100,cx-100,cy-108,200,200,WHITE,42)
        b.text(base+2,f"Orbit {label}",4500,11100,cx-115,cy+123,230,48,label,"bold",24,BLACK,"center")
        # Staggered emergence and a measured 11-degree revolution; no frantic spin.
        add_image(doc,asset,500+i,f"Orbit product {label}",4500,11100,cx,cy-8,size,scale)
    offers=["ATÉ 18X SEM JUROS","GARANTIA DE 2 ANOS*","5% OFF NO PIX","FRETE GRÁTIS*"]
    for i,offer in enumerate(offers):
        st=7100+i*1120
        b.rect(310+i*2,f"Condition pill {i}",st,1120,329,1185,422,76,WHITE,38)
        b.text(311+i*2,f"Condition {i}",st,1120,339,1200,402,48,
               offer,"bold",28,RED,"center")
    b.text(330,"Offer note",7100,6400,145,1545,790,46,"*Consulte condições no site.","medium",24,GREY,"center")

    # S3: preserved clean end-card logic, now within the vertical safe area.
    b.rect(400,"End graphite gradient",15600,3400,0,0,1080,1920,BLACK,
           gradient=grad(0,0,1080,1920,[(0,[.13,.12,.13,1]),(.55,[.04,.04,.05,1]),(1,[.10,.015,.03,1])]))
    b.rect(401,"End red halo",15600,3400,610,320,580,580,RED,290,opacity=17)
    b.text(402,"End eyebrow",15600,3400,100,750,880,48,"CASA DO FITNESS","semibold",31,[1,.48,.5,1],"center")
    b.text(403,"End slogan",15600,3400,95,936,890,174,
           "Sua saúde,\nnosso impulso.","bold",72,WHITE,"center")
    b.text(404,"End categories",15600,3400,116,1170,848,112,
           "Esteiras • Bicicletas • Musculação\nAcessórios e muito mais", "medium",30,[.78,.78,.80,1],"center")
    b.text(405,"End domain",15600,3400,104,1443,872,54,
           "casadofitness.com.br","semibold",37,WHITE,"center")

    actions=WORK/"layers.json"
    actions.write_text(json.dumps([{**a,"insertIndex":0} for a in b.front],ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(actions))
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    actual=json.loads(edit.read_text(encoding="utf-8"))
    actual["composition"]["layers"] = doc["composition"]["layers"] + actual["composition"]["layers"]
    add_image(actual,"logo-white",600,"Orbit CDF logo",4500,11100,450,940,1200,17)
    add_image(actual,"logo-white",601,"End CDF logo",15600,3400,420,616,1200,20)
    edit.write_text(json.dumps(actual,ensure_ascii=False),encoding="utf-8")
    run("project","commit","--project",str(PROJECT),"--file",str(edit))
    # Animated browser entrance, subtle product float, and final resolve.
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    layer_map={v["id"]:v for v in json.loads(edit.read_text(encoding="utf-8"))["composition"]["layers"]}
    for lid in (*range(102,115),160,161,162):
        x,y=layer_map[lid]["transform"]["position"]
        anim += [keys(lid,"positionY",[(0,y+75,LINEAR),(820,y,EASE_OUT),(4200,y,LINEAR)]),
                 keys(lid,"opacity",[(0,0,LINEAR),(220,100,EASE_OUT),(4350,100,LINEAR)])]
    for i in range(6):
        angle=orbit[i][2]
        cx=540+421*math.cos(math.radians(angle))
        cy=957+421*math.sin(math.radians(angle))
        for lid in (220+i*10,221+i*10,222+i*10,500+i):
            x,y=layer_map[lid]["transform"]["position"]
            dx,dy=x-cx,y-cy
            delay=550+i*220
            def orbit_xy(delta, radius=421):
                a=math.radians(angle+delta)
                return 540+radius*math.cos(a)+dx,957+radius*math.sin(a)+dy
            sx,sy=orbit_xy(-12,470)
            ex,ey=orbit_xy(28)
            anim += [keys(lid,"positionX",[(0,sx,LINEAR),(delay,x,EASE_OUT),(11100,ex,LINEAR)]),
                     keys(lid,"positionY",[(0,sy,LINEAR),(delay,y,EASE_OUT),(11100,ey,LINEAR)]),
                     keys(lid,"opacity",[(0,0,LINEAR),(delay*.55,0,LINEAR),(delay+380,100,EASE_OUT),(11100,100,LINEAR)])]
    for lid in (207,208,600):
        x,y=layer_map[lid]["transform"]["position"]
        anim += [keys(lid,"positionY",[(0,y+60,LINEAR),(850,y,EASE_OUT),(11100,y,LINEAR)]),
                 keys(lid,"opacity",[(0,0,LINEAR),(430,100,EASE_OUT),(11100,100,LINEAR)])]
    for lid in (402,403,404,405,601):
        x,y=layer_map[lid]["transform"]["position"]
        anim += [keys(lid,"positionY",[(0,y+70,LINEAR),(750,y,EASE_OUT),(3400,y,LINEAR)]),
                 keys(lid,"opacity",[(0,0,LINEAR),(550,100,EASE_OUT),(3400,100,LINEAR)])]
    animfile=WORK/"animations.json"
    animfile.write_text(json.dumps(anim,ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(animfile))
    stamps=[0,800,1700,2900,4100,4700,5600,6800,7500,8600,9700,10800,12000,13600,15100,16100,17000,18500]
    run("filmstrip","--project",str(PROJECT),"--timestamps-ms",*map(str,stamps),
        "--tile-width","270","--tile-height","480","--items-per-row","6",
        "--output",str(OUT/"previews"/"filmstrip_stories-9x16_v04.png"))
    for t in (2.9,6.8,8.5,10.4,13.2,17.2):
        run("preview","--project",str(PROJECT),"--time",str(t),
            "--output",str(OUT/"previews"/f"v04_{t:.1f}.png"))


def export():
    silent=WORK/"silent_2160p60.mp4"
    run("export","--project",str(PROJECT),"--output",str(silent),"--fps","60","--resolution","4k")
    score=WORK/"trilha-original-v04.wav"
    sound(duration=DURATION,typing=(1.05,3.65),transitions=(4.5,15.6),output=score)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(score),
                    "-map","0:v:0","-map","1:a:0","-vf","scale=1080:1920:flags=lanczos+accurate_rnd,format=yuv420p",
                    "-c:v","libx264","-preset","medium","-crf","16","-c:a","aac","-b:a","192k",
                    "-ar","48000","-ac","2","-af","loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-t",str(DURATION),"-movflags","+faststart",str(FINAL)],check=True)
    if not FINAL.exists() or FINAL.stat().st_size<100000:
        raise RuntimeError("v04 output missing")
    shutil.copy2(PROJECT,OUT/"projeto"/"stories-9x16.tsrct")
    shutil.copy2(OUT/"previews"/"filmstrip_stories-9x16_v04.png",
                 OUT/"previews"/"filmstrip_stories-9x16.png")
    (OUT/"versao.txt").write_text("v04\n",encoding="utf-8")
    print(FINAL)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage",choices=("preview","export"),default="preview")
    args=parser.parse_args()
    build() if args.stage=="preview" else export()
