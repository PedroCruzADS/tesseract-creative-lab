"""Vertical CDF search film v05: measured product cards and one-second click."""
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

WORK = OUT / ".tesseract-work" / "v05"
PROJECT = WORK / "stories-9x16-v05.tsrct"
FINAL = OUT / "cdf-busca-categorias_stories-9x16_v05.mp4"
BLACK = [0.055, 0.055, 0.065, 1]
GREY = [0.43, 0.44, 0.47, 1]
WHITE = [1, 1, 1, 1]
PAPER = [0.975, 0.97, 0.965, 1]
ROSE = [0.976, 0.90, 0.91, 1]
SLATE = [0.88, 0.89, 0.90, 1]
DURATION = 20.0


def validate_orbit_layout(orbit):
    """Geometry gate: source pixels, labels and cards must stay in their slots."""
    source = {
        "treadmill": ((881,883),(3,2,879,881)),
        "bike": ((934,866),(5,3,931,864)),
        "dumbbell": ((1000,1000),(42,209,964,782)),
        "station": ((775,910),(2,2,772,908)),
        "rower": ((1000,1000),(44,264,957,622)),
        "elliptical": ((810,922),(2,2,808,920)),
    }
    hub=(338,836,742,1080)
    min_hub_gap=999
    min_card_gap=999
    min_canvas_margin=999
    for step in range(31):
        delta=3*step/30
        cards=[]
        for asset,label,angle,anchor,scale in orbit:
            rad=math.radians(angle+delta)
            cx=540+400*math.cos(rad)
            cy=960+400*math.sin(rad)
            box=(cx-118,cy-119,cx+118,cy+115)
            cards.append(box)
            min_canvas_margin=min(min_canvas_margin,box[0],1080-box[2],box[1]-250,1670-box[3])
            dx=max(hub[0]-box[2],box[0]-hub[2],0)
            dy=max(hub[1]-box[3],box[1]-hub[3],0)
            min_hub_gap=min(min_hub_gap,math.hypot(dx,dy))
            (sw,sh),(nx0,ny0,nx1,ny1)=source[asset]
            offset=0 if asset=="rower" else -26
            image=(cx-anchor[0]*scale/100,
                   cy+offset-anchor[1]*scale/100,
                   cx+(sw-anchor[0])*scale/100,
                   cy+offset+(sh-anchor[1])*scale/100)
            if image[0]<box[0]+8 or image[2]>box[2]-8 or image[1]<box[1]+5 or image[3]>box[3]-5:
                raise RuntimeError(f"Source image escapes card: {asset}: {image} vs {box}")
            product_bottom=cy+offset+(ny1-anchor[1])*scale/100
            if product_bottom>cy+62:
                raise RuntimeError(f"Product pixels collide with label: {asset}")
        for i in range(len(cards)):
            for j in range(i+1,len(cards)):
                a,b=cards[i],cards[j]
                dx=max(a[0]-b[2],b[0]-a[2],0)
                dy=max(a[1]-b[3],b[1]-a[3],0)
                min_card_gap=min(min_card_gap,math.hypot(dx,dy))
    report={"sampled_orbit_states":31,"min_hub_gap_px":round(min_hub_gap,1),
            "min_card_gap_px":round(min_card_gap,1),
            "min_safe_canvas_margin_px":round(min_canvas_margin,1),
            "source_native_anchor":True,"source_nonwhite_pixels_clear_labels":True}
    if min_hub_gap<12 or min_card_gap<12 or min_canvas_margin<30:
        raise RuntimeError(f"Orbit layout gate failed: {report}")
    (WORK/"layout_qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    return report


def add_image(doc, asset, lid, name, start, duration, x, y, anchor, scale):
    doc["composition"]["layers"].insert(0, {
        "type": "Image", "id": lid, "name": name,
        "activeRange": {"start": start, "duration": duration},
        "transform": tr(x, y, anchor, scale),
        "source": {"assetId": asset, "fit": "contain"},
    })


def archive_v04():
    folder = OUT / "versoes" / "v04"
    for rel in (
        "cdf-busca-categorias_stories-9x16_v04.mp4",
        "projeto/stories-9x16.tsrct",
        "previews/filmstrip_stories-9x16.png",
        "brief.md", "notes.md", "offer.json", "versao.txt",
    ):
        src, dst = OUT / rel, folder / rel
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def build():
    archive_v04()
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
    b.rect(205,"Outer orbit ring",4500,11100,107,527,866,866,[.91,.85,.87,1],433)
    b.rect(206,"Orbit ring inner cutout",4500,11100,110,530,860,860,[.965,.949,.95,1],430)
    b.rect(207,"Hub shadow",4500,11100,336,840,408,248,[.70,.68,.69,1],124,opacity=29)
    b.rect(208,"Hub brand capsule",4500,11100,338,836,404,244,RED,122,
           gradient=grad(338,836,742,1080,[(0,[.98,.13,.18,1]),(1,[.72,.01,.06,1])]))
    b.text(209,"Hub category intro",4500,11100,349,982,382,40,
           "TUDO PARA SE MOVER", "semibold",25,WHITE,"center")
    orbit = [
        ("treadmill","ESTEIRAS",-90,(440,441),17),
        ("bike","BICICLETAS",-30,(467,433),17),
        ("dumbbell","ACESSÓRIOS",30,(500,500),17.5),
        ("station","MUSCULAÇÃO",90,(388,455),17),
        ("rower","REMO",150,(500,500),19),
        ("elliptical","ELÍPTICOS",210,(405,461),16),
    ]
    validate_orbit_layout(orbit)
    anim=[]
    for i,(asset,label,angle,anchor,scale) in enumerate(orbit):
        rad=math.radians(angle)
        cx=540+400*math.cos(rad)
        cy=960+400*math.sin(rad)
        base=220+i*10
        b.rect(base,"Orbit card shadow",4500,11100,cx-119,cy-111,238,234,[.77,.72,.74,1],40,opacity=28)
        b.rect(base+1,"Orbit card",4500,11100,cx-118,cy-119,236,234,WHITE,40)
        b.rect(base+3,"Card accent",4500,11100,cx-91,cy-92,43,5,RED,3)
        b.text(base+2,f"Orbit {label}",4500,11100,cx-105,cy+66,210,43,label,"bold",24,BLACK,"center")
        # Source-native images: true pixel-centre anchors, no generated substitutes.
        y_offset = 0 if asset == "rower" else -26
        add_image(doc,asset,500+i,f"Orbit product {label}",4500,11100,cx,cy+y_offset,anchor,scale)
    offers=["ATÉ 18X SEM JUROS","GARANTIA DE 2 ANOS*","5% OFF NO PIX","FRETE GRÁTIS*"]
    for i,offer in enumerate(offers):
        st=7100+i*1120
        b.rect(310+i*2,f"Condition pill {i}",st,1120,358,1027,364,72,WHITE,36)
        b.text(311+i*2,f"Condition {i}",st,1120,368,1042,344,44,
               offer,"bold",25,RED,"center")
    b.text(330,"Offer note",7100,6400,145,1530,790,46,"*Consulte condições no site.","medium",24,GREY,"center")

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

    # Existing story begins after the requested one-second, deliberate click.
    for action in b.front:
        action["activeRange"]["start"] += 1000
    for layer in doc["composition"]["layers"]:
        layer["activeRange"]["start"] += 1000
    b.rect(700,"Click opening backdrop",0,1000,0,0,1080,1920,PAPER,
           gradient=grad(0,0,1080,1920,[(0,WHITE),(.7,[.97,.95,.95,1]),(1,ROSE)]))
    b.rect(701,"Click opening shadow",0,1000,282,610,516,650,SLATE,42,opacity=45)
    b.rect(702,"Click opening browser",0,1000,286,600,508,650,WHITE,42)
    b.rect(703,"Click opening toolbar",0,1000,286,600,508,70,PAPER,38)
    for lid,x,c in ((704,320,RED),(705,345,SLATE),(706,370,SLATE)):
        b.rect(lid,"Click window dot",0,1000,x,633,12,12,c,6)
    b.text(707,"Click brand",0,1000,325,780,430,60,"CASA DO FITNESS","bold",39,BLACK,"center")
    b.rect(708,"Click search field",0,1000,335,930,410,80,[.97,.97,.97,1],40)
    b.text(709,"Click search hint",0,1000,356,952,370,42,"Pesquisar equipamentos","medium",26,GREY)
    b.rect(710,"Click target",0,1000,455,1080,170,88,RED,43)
    b.text(711,"Click target text",0,1000,456,1104,168,44,"ABRIR","bold",29,WHITE,"center")
    b.rect(712,"Click pulse",640,360,444,1069,192,110,RED,54,opacity=24)
    b.rect(713,"Click pulse inset",640,360,452,1077,176,94,WHITE,46,opacity=95)
    b.shape(714,"Cursor shadow",0,1000,
            [(792,1145),(792,1075),(808,1093),(822,1087),(830,1099),
             (813,1105),(825,1130),(811,1137),(801,1113)],
            grad(0,0,1,1,[(0,BLACK),(1,BLACK)]),front=True)
    b.shape(715,"Cursor white inlay",0,1000,
            [(796,1135),(796,1086),(808,1100),(821,1095),(824,1100),
             (808,1105),(819,1127),(812,1130),(801,1105)],
            grad(0,0,1,1,[(0,WHITE),(1,WHITE)]),front=True)

    actions=WORK/"layers.json"
    actions.write_text(json.dumps([{**a,"insertIndex":0} for a in b.front],ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(actions))
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    actual=json.loads(edit.read_text(encoding="utf-8"))
    actual["composition"]["layers"] = doc["composition"]["layers"] + actual["composition"]["layers"]
    add_image(actual,"logo-white",600,"Orbit CDF logo",5500,11100,540,925,(1200,164),16)
    add_image(actual,"logo-white",601,"End CDF logo",16600,3400,540,616,(1200,164),20)
    priority_ids={220+i*10+j for i in range(6) for j in (2,3)} | {710,711,714,715}
    priority=[v for v in actual["composition"]["layers"] if v["id"] in priority_ids]
    actual["composition"]["layers"] = priority + [v for v in actual["composition"]["layers"] if v["id"] not in priority_ids]
    edit.write_text(json.dumps(actual,ensure_ascii=False),encoding="utf-8")
    run("project","commit","--project",str(PROJECT),"--file",str(edit))
    # Animated browser entrance, subtle product float, and final resolve.
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    layer_map={v["id"]:v for v in json.loads(edit.read_text(encoding="utf-8"))["composition"]["layers"]}
    for lid in (714,715):
        anim += [keys(lid,"positionX",[(0,0,LINEAR),(650,-222,LINEAR),(1000,-222,LINEAR)]),
                 keys(lid,"positionY",[(0,0,LINEAR),(650,25,LINEAR),(1000,25,LINEAR)])]
    for lid in (712,713):
        anim.append(keys(lid,"opacity",[(0,0,LINEAR),(80,100,EASE_OUT),(190,50,LINEAR),(360,0,LINEAR)]))
    for lid in (*range(102,115),160,161,162):
        x,y=layer_map[lid]["transform"]["position"]
        anim += [keys(lid,"positionY",[(0,y+75,LINEAR),(820,y,EASE_OUT),(4200,y,LINEAR)]),
                 keys(lid,"opacity",[(0,100,LINEAR),(4350,100,LINEAR)])]
    for i in range(6):
        angle=orbit[i][2]
        cx=540+400*math.cos(math.radians(angle))
        cy=960+400*math.sin(math.radians(angle))
        for lid in (220+i*10,221+i*10,222+i*10,223+i*10,500+i):
            x,y=layer_map[lid]["transform"]["position"]
            dx,dy=x-cx,y-cy
            delay=550+i*220
            def orbit_xy(delta, radius=400):
                a=math.radians(angle+delta)
                return 540+radius*math.cos(a)+dx,960+radius*math.sin(a)+dy
            sx,sy=orbit_xy(-5,418)
            ex,ey=orbit_xy(3)
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
    stamps=[0,350,680,950,1100,1900,3300,4900,5600,6500,7600,8500,9600,10700,11800,13000,14500,16000,16800,17800,19500]
    run("filmstrip","--project",str(PROJECT),"--timestamps-ms",*map(str,stamps),
        "--tile-width","270","--tile-height","480","--items-per-row","6",
        "--output",str(OUT/"previews"/"filmstrip_stories-9x16_v05.png"))
    for t in (0.35,0.75,1.15,3.2,6.7,8.5,10.4,13.2,17.8):
        run("preview","--project",str(PROJECT),"--time",str(t),
            "--output",str(OUT/"previews"/f"v05_{t:.2f}.png"))


def export():
    silent=WORK/"silent_2160p60.mp4"
    run("export","--project",str(PROJECT),"--output",str(silent),"--fps","60","--resolution","4k")
    score=WORK/"trilha-original-v05.wav"
    sound(duration=DURATION,typing=(2.05,4.65),transitions=(5.5,16.6),output=score)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(score),
                    "-map","0:v:0","-map","1:a:0","-vf","scale=1080:1920:flags=lanczos+accurate_rnd,format=yuv420p",
                    "-c:v","libx264","-preset","medium","-crf","16","-c:a","aac","-b:a","192k",
                    "-ar","48000","-ac","2","-af","loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-t",str(DURATION),"-movflags","+faststart",str(FINAL)],check=True)
    if not FINAL.exists() or FINAL.stat().st_size<100000:
        raise RuntimeError("v05 output missing")
    shutil.copy2(PROJECT,OUT/"projeto"/"stories-9x16.tsrct")
    shutil.copy2(OUT/"previews"/"filmstrip_stories-9x16_v05.png",
                 OUT/"previews"/"filmstrip_stories-9x16.png")
    shutil.copy2(WORK/"layout_qa.json",OUT/"previews"/"layout_qa_v05.json")
    (OUT/"versao.txt").write_text("v05\n",encoding="utf-8")
    print(FINAL)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage",choices=("preview","export"),default="preview")
    args=parser.parse_args()
    build() if args.stage=="preview" else export()
