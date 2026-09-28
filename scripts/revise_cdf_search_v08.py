"""Vertical CDF search film v08: gradiente do brandbook, anel de categorias na abertura, órbita mais evidente, cursor refeito."""
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

WORK = OUT / ".tesseract-work" / "v08"
PROJECT = WORK / "stories-9x16-v08.tsrct"
FINAL = OUT / "cdf-busca-categorias_stories-9x16_v08.mp4"
BLACK = [0.055, 0.055, 0.065, 1]
GREY = [0.43, 0.44, 0.47, 1]
WHITE = [1, 1, 1, 1]
PAPER = [0.975, 0.97, 0.965, 1]
ROSE = [0.976, 0.90, 0.91, 1]
SLATE = [0.88, 0.89, 0.90, 1]
DURATION = 18.0
ORBIT_DEG = 84
INK = [0.03, 0.03, 0.04, 1]
DARKRED = [0.30, 0.015, 0.05, 1]
BRAND_RED = [0.898, 0.035, 0.078, 1]      # #E50914
BRAND_ORANGE = [0.98, 0.20, 0.07, 1]      # #FA3312
BRAND_YELLOW = [0.894, 0.91, 0.33, 1]     # #E4E854
ARROW = [(0, 0), (0, 16.5), (4.0, 12.9), (6.9, 19.2), (9.6, 18.0), (6.7, 11.8), (11.6, 11.7)]


def offset_polygon(poly, d):
    """Contorno externo com quinas em esquadro (miter), para o cursor ter borda preta uniforme."""
    n = len(poly)
    area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n)) / 2
    sign = 1 if area > 0 else -1
    out = []
    for i in range(n):
        p0, p1, p2 = poly[i - 1], poly[i], poly[(i + 1) % n]

        def normal(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = math.hypot(dx, dy)
            return (dy / length * sign, -dx / length * sign)
        n1, n2 = normal(p0, p1), normal(p1, p2)
        k = 1 + n1[0] * n2[0] + n1[1] * n2[1]
        out.append((round(p1[0] + (n1[0] + n2[0]) / k * d, 1), round(p1[1] + (n1[1] + n2[1]) / k * d, 1)))
    return out


def cursor(b, outline_id, inlay_id, dur, x, y, scale=2.9, border=2.4):
    inner = [(round(x + px * scale, 1), round(y + py * scale, 1)) for px, py in ARROW]
    b.shape(outline_id, "Cursor outline", 0, dur, offset_polygon(inner, border),
            grad(0, 0, 1, 1, [(0, BLACK), (1, BLACK)]), front=True)
    b.shape(inlay_id, "Cursor inlay", 0, dur, inner, grad(0, 0, 1, 1, [(0, WHITE), (1, WHITE)]), front=True)


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
    hub=(360,850,720,1070)
    min_hub_gap=999
    min_card_gap=999
    min_canvas_margin=999
    for step in range(121):
        delta=ORBIT_DEG*step/120
        cards=[]
        for asset,label,angle,anchor,scale in orbit:
            rad=math.radians(angle+delta)
            cx=540+375*math.cos(rad)
            cy=960+375*math.sin(rad)
            box=(cx-100,cy-105,cx+100,cy+105)
            cards.append(box)
            min_canvas_margin=min(min_canvas_margin,box[0],1080-box[2],box[1]-250,1670-box[3])
            dx=max(hub[0]-box[2],box[0]-hub[2],0)
            dy=max(hub[1]-box[3],box[1]-hub[3],0)
            min_hub_gap=min(min_hub_gap,math.hypot(dx,dy))
            (sw,sh),(nx0,ny0,nx1,ny1)=source[asset]
            offsets={"treadmill":-22,"bike":-22,"dumbbell":-20,
                     "station":-21,"rower":0,"elliptical":-22}
            offset=offsets[asset]
            image=(cx-anchor[0]*scale/100,
                   cy+offset-anchor[1]*scale/100,
                   cx+(sw-anchor[0])*scale/100,
                   cy+offset+(sh-anchor[1])*scale/100)
            if image[0]<box[0]+5 or image[2]>box[2]-5 or image[1]<box[1]+5 or image[3]>box[3]-5:
                raise RuntimeError(f"Source image escapes card: {asset}: {image} vs {box}")
            product_bottom=cy+offset+(ny1-anchor[1])*scale/100
            if product_bottom>cy+61:
                raise RuntimeError(f"Product pixels collide with label: {asset}")
        for i in range(len(cards)):
            for j in range(i+1,len(cards)):
                a,b=cards[i],cards[j]
                dx=max(a[0]-b[2],b[0]-a[2],0)
                dy=max(a[1]-b[3],b[1]-a[3],0)
                min_card_gap=min(min_card_gap,math.hypot(dx,dy))
    report={"sampled_orbit_states":121,"orbit_degrees":ORBIT_DEG,"min_hub_gap_px":round(min_hub_gap,1),
            "min_card_gap_px":round(min_card_gap,1),
            "min_safe_canvas_margin_px":round(min_canvas_margin,1),
            "source_native_anchor":True,"source_nonwhite_pixels_clear_labels":True}
    if min_hub_gap<18 or min_card_gap<40 or min_canvas_margin<55:
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


def archive_v07():
    folder = OUT / "versoes" / "v07"
    for rel in (
        "cdf-busca-categorias_stories-9x16_v07.mp4",
        "projeto/stories-9x16.tsrct",
        "previews/filmstrip_stories-9x16.png",
        "previews/layout_qa_v07.json",
        "brief.md", "notes.md", "offer.json", "versao.txt",
    ):
        src, dst = OUT / rel, folder / rel
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def build():
    archive_v07()
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
           gradient=grad(0, 0, 1080, 1920, [(0, INK), (.30, DARKRED), (.62, BRAND_RED), (.88, BRAND_ORANGE), (1, BRAND_YELLOW)]))
    b.rect(101, "Browser soft brand haze", 0, 4500, 700, 1180, 520, 720, BRAND_YELLOW, 250, opacity=14)
    b.rect(102, "Browser shadow", 0, 4500, 72, 350, 936, 1060, SLATE, 53)
    b.rect(103, "Browser window", 0, 4500, 75, 338, 930, 1060, WHITE, 50)
    b.rect(104, "Browser toolbar", 0, 4500, 75, 338, 930, 96, PAPER, 49)
    for lid,x,c in ((105,115,RED),(106,143,SLATE),(107,171,SLATE)):
        b.rect(lid,"Browser control",0,4500,x,377,13,13,c,7)
    b.rect(108,"Address field",0,4500,270,361,603,49,WHITE,24)
    b.text(109,"Address",0,4500,300,364,548,40,"Pesquisar", "medium",28,GREY)
    b.rect(110,"Browser brand pill",0,4500,380,484,320,88,RED,44,
           gradient=grad(380,484,700,572,[(0,[.98,.13,.18,1]),(1,[.72,.01,.06,1])]))
    b.text(111,"Browser question",0,4500,130,604,820,156,"Seu próximo treino\ncomeça aqui.","bold",66,BLACK,"center")
    b.rect(112,"Search shadow",0,4500,126,856,828,125,SLATE,59)
    b.rect(113,"Search box",0,4500,130,850,820,125,WHITE,59)
    b.rect(114,"Search icon ring",0,4500,172,892,36,36,RED,18)
    b.rect(168,"Search icon core",0,4500,178,898,24,24,WHITE,12)
    b.shape(169,"Search icon handle",0,4500,
            [(199,922),(205,916),(222,933),(216,939)],
            grad(0,0,1,1,[(0,RED),(1,RED)]),front=True)
    phrase = "equipamentos fitness para casa"
    for i in range(1,len(phrase)+1):
        start = 1050 + int((i-1)*84)
        end = 1050 + i*84 if i<len(phrase) else 4440
        b.text(120+i,f"Typed {i}",start,end-start,245,888,660,54,
               phrase[:i],"medium",37,BLACK)
    b.text(160,"Browser supporting",0,4500,130,1046,820,94,
           "Esteiras, bicicletas, musculação, acessórios...", "medium",34,[.34,.35,.38,1],"center")
    b.rect(161,"Search action",0,4500,369,1220,342,80,RED,39)
    b.text(162,"Search action text",0,4500,370,1236,340,45,"ENCONTRAR", "bold",31,WHITE,"center")
    b.rect(163,"Search focus progress",0,4500,170,966,740,5,RED,3)
    cursor(b,165,166,4500,903,1029)
    b.rect(167,"Search-to-discovery white wash",4300,200,0,0,1080,1920,WHITE)

    # S2: six product cards orbit a fixed, branded hub. Four benefits take turns.
    b.rect(200,"Orbit atmospheric background",4500,9100,0,0,1080,1920,PAPER,
           gradient=grad(0,0,1000,1920,[(0,INK),(.32,DARKRED),(.68,BRAND_RED),(.96,BRAND_ORANGE),(1,BRAND_ORANGE)]))
    b.rect(201,"Orbit top haze",4500,9100,-130,220,540,540,BRAND_RED,270,opacity=45)
    b.rect(202,"Orbit bottom haze",4500,9100,720,1180,550,550,BRAND_YELLOW,275,opacity=9)
    b.text(203,"Orbit title",4500,9100,90,318,900,96,"Do cardio à força.","bold",68,WHITE,"center")
    b.rect(205,"Orbit plate halo",4500,9100,125,545,830,830,WHITE,415,opacity=6)
    b.rect(206,"Orbit plate",4500,9100,140,560,800,800,WHITE,400,opacity=10)
    for lid,opacity in ((216,75),(217,38),(218,16)):
        b.rect(lid,"Orbit scanning light",4500,9100,531,553,18,18,BRAND_YELLOW,9,opacity=opacity)
    b.rect(207,"Hub shadow",4500,9100,358,858,364,222,BLACK,111,opacity=45)
    b.rect(208,"Hub brand capsule",4500,9100,360,850,360,220,INK,110,
           gradient=grad(360,850,720,1070,[(0,[.15,.15,.17,1]),(1,[.02,.02,.03,1])]))
    b.text(209,"Hub category intro",4500,9100,367,984,346,40,
           "TUDO PARA SE MOVER", "semibold",24,WHITE,"center")
    orbit = [
        ("treadmill","ESTEIRAS",-90,(440,441),16.5),
        ("bike","BICICLETAS",-30,(467,433),16.5),
        ("dumbbell","ACESSÓRIOS",30,(500,500),16),
        ("station","MUSCULAÇÃO",90,(388,455),16),
        ("rower","REMO",150,(500,500),19),
        ("elliptical","ELÍPTICOS",210,(405,461),16),
    ]
    validate_orbit_layout(orbit)
    anim=[]
    for i,(asset,label,angle,anchor,scale) in enumerate(orbit):
        rad=math.radians(angle)
        cx=540+375*math.cos(rad)
        cy=960+375*math.sin(rad)
        base=220+i*10
        b.rect(base+4,"Card soft halo",4500,9100,cx-112,cy-117,224,234,BRAND_YELLOW,44,opacity=0)
        b.rect(base,"Orbit card shadow",4500,9100,cx-101,cy-97,202,212,BLACK,37,opacity=38)
        b.rect(base+1,"Orbit card",4500,9100,cx-100,cy-105,200,210,WHITE,36)
        b.rect(base+3,"Card accent",4500,9100,cx-76,cy-83,39,5,RED,3)
        b.text(base+2,f"Orbit {label}",4500,9100,cx-92,cy+65,184,36,label,"bold",24,BLACK,"center")
        # Source-native images: true pixel-centre anchors, no generated substitutes.
        offsets={"treadmill":-22,"bike":-22,"dumbbell":-20,
                 "station":-21,"rower":0,"elliptical":-22}
        y_offset=offsets[asset]
        add_image(doc,asset,500+i,f"Orbit product {label}",4500,9100,cx,cy+y_offset,anchor,scale)
    offers=["ATÉ 18X SEM JUROS","GARANTIA DE 2 ANOS*","5% OFF NO PIX","FRETE GRÁTIS*"]
    for i,offer in enumerate(offers):
        st=7100+i*1120
        b.text(311+i*2,f"Condition {i}",st,1120,367,974,346,48,
               offer,"bold",29,BRAND_YELLOW,"center")
    b.text(330,"Offer note",7100,6400,125,1530,830,48,"*Consulte condições no site.","semibold",28,[1,1,1,.94],"center")

    # S3: preserved clean end-card logic, now within the vertical safe area.
    b.rect(400,"End graphite gradient",13600,3400,0,0,1080,1920,BLACK,
           gradient=grad(0,0,1080,1920,[(0,INK),(.5,[.16,.015,.04,1]),(.76,BRAND_RED),(1,BRAND_ORANGE)]))
    b.rect(401,"End brand halo",13600,3400,900,1130,480,480,BRAND_YELLOW,240,opacity=20)
    b.text(403,"End slogan",13600,3400,95,776,890,174,
           "Sua saúde,\nnosso impulso.","bold",76,WHITE,"center")
    b.text(404,"End categories",13600,3400,96,1010,888,120,
           "Esteiras • Bicicletas • Musculação\nAcessórios e muito mais", "medium",34,[.84,.84,.86,1],"center")
    b.text(405,"End domain",13600,3400,84,1272,912,72,
           "casadofitness.com.br","bold",50,WHITE,"center")
    b.rect(406,"End accent rule",13600,3400,440,970,200,5,BRAND_YELLOW,3)
    b.rect(407,"End domain rule",13600,3400,440,1356,200,5,BRAND_YELLOW,3)

    # Existing story begins after the requested one-second, deliberate click.
    for action in b.front:
        action["activeRange"]["start"] += 1000
    for layer in doc["composition"]["layers"]:
        layer["activeRange"]["start"] += 1000
    b.rect(700,"Click opening backdrop",0,1000,0,0,1080,1920,PAPER,
           gradient=grad(0,0,1080,1920,[(0,INK),(.30,DARKRED),(.62,BRAND_RED),(.88,BRAND_ORANGE),(1,BRAND_YELLOW)]))
    # Anel das seis categorias em volta do cartão: o produto aparece no primeiro segundo e antecipa a órbita.
    ghost_offsets={"treadmill":-22,"bike":-22,"dumbbell":-20,"station":-21,"rower":0,"elliptical":-22}
    GK=0.85
    for i,(asset,label,angle,anchor,scale) in enumerate(orbit):
        gx=540+470*math.cos(math.radians(angle))
        gy=950+590*math.sin(math.radians(angle))
        gb=800+i*10
        b.rect(gb,"Ghost card shadow",0,1000,gx-86,gy-84,172,180,BLACK,32,opacity=38)
        b.rect(gb+1,"Ghost card",0,1000,gx-85,gy-89,170,178,WHITE,30)
        b.rect(gb+3,"Ghost accent",0,1000,gx-65,gy-71,33,4,RED,2)
        b.text(gb+2,f"Ghost {label}",0,1000,gx-78,gy+53,156,34,label,"bold",21,BLACK,"center")
    b.rect(701,"Click opening shadow",0,1000,236,552,608,700,SLATE,44,opacity=50)
    b.rect(702,"Click opening browser",0,1000,240,540,600,700,WHITE,44)
    b.rect(703,"Click opening toolbar",0,1000,240,540,600,72,PAPER,40)
    for lid,x,c in ((704,278,RED),(705,304,SLATE),(706,330,SLATE)):
        b.rect(lid,"Click window dot",0,1000,x,568,14,14,c,7)
    b.rect(707,"Click brand pill",0,1000,300,660,480,130,RED,65,
           gradient=grad(300,660,780,790,[(0,[.98,.13,.18,1]),(1,[.72,.01,.06,1])]))
    b.rect(708,"Click search field",0,1000,290,860,500,96,[.97,.97,.97,1],48)
    b.text(709,"Click search hint",0,1000,330,885,430,48,"Pesquisar equipamentos","medium",30,[.34,.35,.38,1])
    b.rect(710,"Click target",0,1000,430,1040,220,104,RED,52)
    b.text(711,"Click target text",0,1000,431,1066,218,52,"ABRIR","bold",36,WHITE,"center")
    b.rect(712,"Click pulse",640,360,420,1028,240,128,RED,64,opacity=24)
    b.rect(713,"Click pulse inset",640,360,428,1036,224,112,WHITE,56,opacity=95)
    cursor(b,714,715,1000,792,1075)

    actions=WORK/"layers.json"
    actions.write_text(json.dumps([{**a,"insertIndex":0} for a in b.front],ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(actions))
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    actual=json.loads(edit.read_text(encoding="utf-8"))
    actual["composition"]["layers"] = doc["composition"]["layers"] + actual["composition"]["layers"]
    add_image(actual,"logo-white",600,"Orbit CDF logo",5500,9100,540,925,(1200,164),14)
    add_image(actual,"logo-white",601,"End CDF logo",14600,3400,540,620,(1200,164),22)
    add_image(actual,"logo-white",602,"Click CDF logo",0,1000,540,725,(1200,164),15.5)
    add_image(actual,"logo-white",603,"Search CDF logo",1000,4500,540,528,(1200,164),10.5)
    for i,(asset,label,angle,anchor,scale) in enumerate(orbit):
        gx=540+470*math.cos(math.radians(angle))
        gy=950+590*math.sin(math.radians(angle))
        add_image(actual,asset,900+i,f"Ghost product {label}",0,1000,gx,gy+ghost_offsets[asset]*GK,anchor,scale*GK)
    priority_ids={220+i*10+j for i in range(6) for j in (2,3)} | {800+i*10+j for i in range(6) for j in (2,3)} | {602,603,710,711,714,715,165,166,169}
    priority=[v for v in actual["composition"]["layers"] if v["id"] in priority_ids]
    actual["composition"]["layers"] = priority + [v for v in actual["composition"]["layers"] if v["id"] not in priority_ids]
    edit.write_text(json.dumps(actual,ensure_ascii=False),encoding="utf-8")
    run("project","commit","--project",str(PROJECT),"--file",str(edit))
    # Deterministic, continuous motion throughout all three story beats.
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    layer_map={v["id"]:v for v in json.loads(edit.read_text(encoding="utf-8"))["composition"]["layers"]}
    def ease01(v):
        q=max(0.0,min(1.0,v))
        return q*q*(3-2*q)
    for i in range(6):   # anel de categorias da abertura: entra em sequência e some junto com o cartão
        for lid in (800+i*10,801+i*10,802+i*10,803+i*10,900+i):
            x,y=layer_map[lid]["transform"]["position"]
            peak=38 if lid==800+i*10 else 100
            anim += [keys(lid,"positionY",[(0,y+16,LINEAR),(520,y,EASE_OUT),(1000,y-6,LINEAR)]),
                     keys(lid,"opacity",[(0,peak,LINEAR),(780,peak,LINEAR),(1000,0,LINEAR)])]
    for lid in (714,715):   # ponta do cursor termina na borda direita do botão, fora do texto
        anim += [keys(lid,"positionX",[(0,0,LINEAR),(650,-166,LINEAR),(1000,-166,LINEAR)]),
                 keys(lid,"positionY",[(0,0,LINEAR),(650,21,LINEAR),(1000,21,LINEAR)])]
    for lid in (712,713):
        anim.append(keys(lid,"opacity",[(0,0,LINEAR),(80,100,EASE_OUT),(190,50,LINEAR),(360,0,LINEAR)]))
    for lid in (*range(701,712),602):
        x,y=layer_map[lid]["transform"]["position"]
        anim.append(keys(lid,"positionY",[(0,y+12,LINEAR),(640,y,EASE_OUT),(1000,y-8,LINEAR)]))
    for lid in (710,711):
        anim += [keys(lid,"scaleX",[(0,100,LINEAR),(650,100,LINEAR),(730,95,EASE_OUT),(940,100,EASE_OUT)]),
                 keys(lid,"scaleY",[(0,100,LINEAR),(650,100,LINEAR),(730,95,EASE_OUT),(940,100,EASE_OUT)])]
    for lid in (*range(102,115),160,161,162,163,603):
        x,y=layer_map[lid]["transform"]["position"]
        anim.append(keys(lid,"positionY",[(0,y+56,LINEAR),(760,y,EASE_OUT),(4500,y-8,LINEAR)]))
    for lid in (160,161,162):
        anim.append(keys(lid,"opacity",[(0,0,LINEAR),(1700,0,LINEAR),(2450,100,EASE_OUT),(4500,100,LINEAR)]))
    anim.append(keys(163,"scaleX",[(0,0,LINEAR),(950,0,LINEAR),(3700,100,EASE_OUT),(4500,100,LINEAR)]))
    for lid in (168,):
        x,y=layer_map[lid]["transform"]["position"]
        anim.append(keys(lid,"positionY",[(0,y+56,LINEAR),(760,y,EASE_OUT),(4500,y-8,LINEAR)]))
    anim.append(keys(169,"positionY",[(0,56,LINEAR),(760,0,EASE_OUT),(4500,-8,LINEAR)]))
    for lid in (165,166):   # ponta do cursor termina na borda direita de ENCONTRAR, fora do texto
        anim += [keys(lid,"positionX",[(0,0,LINEAR),(3500,0,LINEAR),(4140,-235,EASE_INOUT),(4500,-235,LINEAR)]),
                 keys(lid,"positionY",[(0,0,LINEAR),(3500,0,LINEAR),(4140,233,EASE_INOUT),(4500,233,LINEAR)]),
                 keys(lid,"opacity",[(0,0,LINEAR),(3370,0,LINEAR),(3530,100,EASE_OUT),(4500,100,LINEAR)])]
    for lid in (161,162):
        anim += [keys(lid,"scaleX",[(0,100,LINEAR),(4140,100,LINEAR),(4230,95,EASE_OUT),(4440,100,EASE_OUT)]),
                 keys(lid,"scaleY",[(0,100,LINEAR),(4140,100,LINEAR),(4230,95,EASE_OUT),(4440,100,EASE_OUT)])]
    anim.append(keys(167,"opacity",[(0,0,LINEAR),(130,30,EASE_INOUT),(200,100,EASE_OUT)]))
    for lid in (203,):
        x,y=layer_map[lid]["transform"]["position"]
        anim += [keys(lid,"positionY",[(0,y+48,LINEAR),(560,y,EASE_OUT),(9100,y-5,LINEAR)]),
                 keys(lid,"opacity",[(0,0,LINEAR),(500,100,EASE_OUT),(9100,100,LINEAR)])]
    for lid,delta in ((201,52),(202,-60)):
        x,y=layer_map[lid]["transform"]["position"]
        anim.append(keys(lid,"positionX",[(0,x,LINEAR),(9100,x+delta,LINEAR)]))
    for lid in (205,206):
        anim += [keys(lid,"scaleX",[(0,94,LINEAR),(740,100,EASE_OUT)]),
                 keys(lid,"scaleY",[(0,94,LINEAR),(740,100,EASE_OUT)])]
    for lid,lag in ((216,0),(217,180),(218,360)):
        xp=[];yp=[]
        for t in range(0,9101,180):
            phase=-113+115*ease01(max(0,(t-lag))/9100)
            a=math.radians(phase)
            xp.append((t,540+400*math.cos(a),LINEAR))
            yp.append((t,960+400*math.sin(a),LINEAR))
        anim += [keys(lid,"positionX",xp),keys(lid,"positionY",yp)]
    for i in range(6):
        angle=orbit[i][2]
        cx=540+375*math.cos(math.radians(angle))
        cy=960+375*math.sin(math.radians(angle))
        delay=250+i*170
        highlight=1900+i*940
        for lid in (220+i*10,221+i*10,222+i*10,223+i*10,224+i*10,500+i):
            x,y=layer_map[lid]["transform"]["position"]
            dx,dy=x-cx,y-cy
            xp=[];yp=[]
            for t in range(0,9101,150):
                entry=ease01((t-delay)/600)
                radius=333+42*entry
                turn=ORBIT_DEG*ease01((t-delay-600)/max(1,8500-delay))
                a=math.radians(angle-5*(1-entry)+turn)
                xp.append((t,540+radius*math.cos(a)+dx,LINEAR))
                yp.append((t,960+radius*math.sin(a)+dy,LINEAR))
            anim += [keys(lid,"positionX",xp),keys(lid,"positionY",yp)]
            if lid != 224+i*10:
                anim.append(keys(lid,"opacity",[(0,0,LINEAR),(delay,0,LINEAR),
                                                (delay+500,100,EASE_OUT),(9100,100,LINEAR)]))
        anim.append(keys(224+i*10,"opacity",[(0,0,LINEAR),(highlight-180,0,LINEAR),
                                             (highlight+180,62,EASE_OUT),(highlight+820,0,EASE_OUT),(9100,0,LINEAR)]))
        for lid in (220+i*10,221+i*10,222+i*10,223+i*10,224+i*10):
            anim += [keys(lid,"scaleX",[(0,100,LINEAR),(highlight-120,100,LINEAR),(highlight+320,107,EASE_OUT),
                                        (highlight+900,100,EASE_OUT),(9100,100,LINEAR)]),
                     keys(lid,"scaleY",[(0,100,LINEAR),(highlight-120,100,LINEAR),(highlight+320,107,EASE_OUT),
                                        (highlight+900,100,EASE_OUT),(9100,100,LINEAR)])]
        base_scale=orbit[i][4]
        anim += [keys(500+i,"scaleX",[(0,base_scale,LINEAR),(highlight-120,base_scale,LINEAR),
                                      (highlight+320,base_scale*1.07,EASE_OUT),
                                      (highlight+900,base_scale,EASE_OUT),(9100,base_scale,LINEAR)]),
                 keys(500+i,"scaleY",[(0,base_scale,LINEAR),(highlight-120,base_scale,LINEAR),
                                      (highlight+320,base_scale*1.07,EASE_OUT),
                                      (highlight+900,base_scale,EASE_OUT),(9100,base_scale,LINEAR)])]
    for lid in (207,208,600):
        x,y=layer_map[lid]["transform"]["position"]
        anim += [keys(lid,"positionY",[(0,y+50,LINEAR),(780,y,EASE_OUT),(9100,y-5,LINEAR)]),
                 keys(lid,"opacity",[(0,0,LINEAR),(480,100,EASE_OUT),(9100,100,LINEAR)])]
    anim += [keys(600,"scaleX",[(0,13,LINEAR),(850,14,EASE_OUT),(9100,14.2,LINEAR)]),
             keys(600,"scaleY",[(0,13,LINEAR),(850,14,EASE_OUT),(9100,14.2,LINEAR)])]
    # a tagline do hub cede o lugar à condição de cada vez e volta no fim
    anim.append(keys(209,"opacity",[(0,0,LINEAR),(480,100,EASE_OUT),(2500,100,LINEAR),(2700,0,EASE_OUT),
                                    (7100,0,LINEAR),(7400,100,EASE_OUT),(9100,100,LINEAR)]))
    for i in range(4):
        for lid in (311+i*2,):
            x,y=layer_map[lid]["transform"]["position"]
            anim += [keys(lid,"positionY",[(0,y+18,LINEAR),(220,y,EASE_OUT),(900,y,LINEAR),(1120,y-9,LINEAR)]),
                     keys(lid,"opacity",[(0,0,LINEAR),(180,100,EASE_OUT),(900,100,LINEAR),(1120,0,LINEAR)])]
    anim.append(keys(330,"opacity",[(0,0,LINEAR),(300,100,EASE_OUT),(6400,100,LINEAR)]))
    for lid,delay in ((601,0),(403,430),(406,750),(404,1000),(405,1300),(407,1500)):
        x,y=layer_map[lid]["transform"]["position"]
        position_frames=[(0,y+56,LINEAR)]
        opacity_frames=[(0,0,LINEAR)]
        if delay:
            position_frames.append((delay,y+56,LINEAR))
            opacity_frames.append((delay,0,LINEAR))
        position_frames.extend([(delay+590,y,EASE_OUT),(3400,y-5,LINEAR)])
        opacity_frames.extend([(delay+480,100,EASE_OUT),(3400,100,LINEAR)])
        anim += [keys(lid,"positionY",position_frames),keys(lid,"opacity",opacity_frames)]
    anim += [keys(601,"scaleX",[(0,20,LINEAR),(780,22,EASE_OUT),(3400,22.2,LINEAR)]),
             keys(601,"scaleY",[(0,20,LINEAR),(780,22,EASE_OUT),(3400,22.2,LINEAR)]),
             keys(406,"scaleX",[(0,0,LINEAR),(750,0,LINEAR),(1400,100,EASE_OUT)]),
             keys(407,"scaleX",[(0,0,LINEAR),(1500,0,LINEAR),(2100,100,EASE_OUT)]),
             keys(401,"positionX",[(0,1105,LINEAR),(3400,1140,LINEAR)])]
    animfile=WORK/"animations.json"
    animfile.write_text(json.dumps(anim,ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(animfile))
    stamps=[0,350,680,950,1100,1900,3300,4900,5600,6500,7600,8500,9600,10700,11800,13000,14500,15100,16000,16800,17800]
    run("filmstrip","--project",str(PROJECT),"--timestamps-ms",*map(str,stamps),
        "--tile-width","270","--tile-height","480","--items-per-row","6",
        "--output",str(OUT/"previews"/"filmstrip_stories-9x16_v08.png"))
    for t in (0.35,0.75,1.15,3.2,6.7,8.5,10.4,13.2,17.8):
        run("preview","--project",str(PROJECT),"--time",str(t),
            "--output",str(OUT/"previews"/f"v08_{t:.2f}.png"))


def export():
    silent=WORK/"silent_2160p60.mp4"
    run("export","--project",str(PROJECT),"--output",str(silent),"--fps","60","--resolution","4k")
    score=WORK/"trilha-original-v08.wav"
    sound(duration=DURATION,typing=(2.05,4.65),transitions=(5.5,14.6),output=score)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(score),
                    "-map","0:v:0","-map","1:a:0","-vf","scale=1080:1920:flags=lanczos+accurate_rnd,format=yuv420p",
                    "-c:v","libx264","-preset","medium","-crf","16","-c:a","aac","-b:a","192k",
                    "-ar","48000","-ac","2","-af","loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-t",str(DURATION),"-movflags","+faststart",str(FINAL)],check=True)
    if not FINAL.exists() or FINAL.stat().st_size<100000:
        raise RuntimeError("v08 output missing")
    shutil.copy2(PROJECT,OUT/"projeto"/"stories-9x16.tsrct")
    shutil.copy2(OUT/"previews"/"filmstrip_stories-9x16_v08.png",
                 OUT/"previews"/"filmstrip_stories-9x16.png")
    shutil.copy2(WORK/"layout_qa.json",OUT/"previews"/"layout_qa_v08.json")
    (OUT/"versao.txt").write_text("v08\n",encoding="utf-8")
    print(FINAL)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage",choices=("preview","export"),default="preview")
    args=parser.parse_args()
    build() if args.stage=="preview" else export()
