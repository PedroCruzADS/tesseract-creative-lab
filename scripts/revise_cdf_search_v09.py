"""Vertical CDF search film v09: abertura sem anel e com cartão maior, título novo, hub folgado, categorias em fade sequencial, domínio digitado."""
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

WORK = OUT / ".tesseract-work" / "v09"
PROJECT = WORK / "stories-9x16-v09.tsrct"
FINAL = OUT / "cdf-busca-categorias_stories-9x16_v09.mp4"
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
    hub=(350,840,730,1080)
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
            # o hub é uma cápsula (raio 120): distância do card ao eixo da cápsula menos o raio
            def rect_dist(px,py):
                return math.hypot(max(box[0]-px,px-box[2],0),max(box[1]-py,py-box[3],0))
            cap_gap=min(rect_dist(470+140*k/14,960) for k in range(15))-120
            min_hub_gap=min(min_hub_gap,cap_gap)
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


def archive_v08():
    folder = OUT / "versoes" / "v08"
    for rel in (
        "cdf-busca-categorias_stories-9x16_v08.mp4",
        "projeto/stories-9x16.tsrct",
        "previews/filmstrip_stories-9x16.png",
        "previews/layout_qa_v08.json",
        "brief.md", "notes.md", "offer.json", "versao.txt",
    ):
        src, dst = OUT / rel, folder / rel
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def build():
    archive_v08()
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
    b.rect(102, "Browser shadow", 0, 4500, 72, 312, 936, 1140, SLATE, 53)
    b.rect(103, "Browser window", 0, 4500, 75, 300, 930, 1140, WHITE, 50)
    b.rect(104, "Browser toolbar", 0, 4500, 75, 300, 930, 100, PAPER, 49)
    for lid,x,c in ((105,115,RED),(106,143,SLATE),(107,171,SLATE)):
        b.rect(lid,"Browser control",0,4500,x,342,14,14,c,7)
    b.rect(108,"Address field",0,4500,270,324,603,52,WHITE,26)
    b.text(109,"Address",0,4500,300,327,548,44,"Pesquisar", "medium",30,GREY)
    b.rect(110,"Browser brand pill",0,4500,360,464,360,104,RED,52,
           gradient=grad(360,464,720,568,[(0,[.98,.13,.18,1]),(1,[.72,.01,.06,1])]))
    b.text(111,"Browser question",0,4500,110,608,860,180,"Seu próximo treino\ncomeça aqui.","bold",74,BLACK,"center")
    b.rect(112,"Search shadow",0,4500,126,868,828,142,SLATE,71)
    b.rect(113,"Search box",0,4500,130,862,820,142,WHITE,71)
    b.rect(114,"Search icon ring",0,4500,176,914,40,40,RED,20)
    b.rect(168,"Search icon core",0,4500,183,921,26,26,WHITE,13)
    b.shape(169,"Search icon handle",0,4500,
            [(206,952),(212,946),(231,965),(225,971)],
            grad(0,0,1,1,[(0,RED),(1,RED)]),front=True)
    phrase = "equipamentos fitness para casa"
    for i in range(1,len(phrase)+1):
        start = 1050 + int((i-1)*84)
        end = 1050 + i*84 if i<len(phrase) else 4440
        b.text(120+i,f"Typed {i}",start,end-start,262,908,660,64,
               phrase[:i],"medium",42,BLACK)
    b.text(160,"Browser supporting",0,4500,100,1076,880,100,
           "Esteiras, bicicletas, musculação, acessórios...", "medium",37,[.34,.35,.38,1],"center")
    b.rect(161,"Search action",0,4500,340,1256,400,104,RED,52)
    b.text(162,"Search action text",0,4500,341,1276,398,58,"ENCONTRAR", "bold",37,WHITE,"center")
    b.rect(163,"Search focus progress",0,4500,170,1000,740,5,RED,3)
    cursor(b,165,166,4500,903,1120)
    b.rect(167,"Search-to-discovery white wash",4300,200,0,0,1080,1920,WHITE)

    # S2: six product cards orbit a fixed, branded hub. Four benefits take turns.
    b.rect(200,"Orbit atmospheric background",4500,9100,0,0,1080,1920,PAPER,
           gradient=grad(0,0,1000,1920,[(0,INK),(.32,DARKRED),(.68,BRAND_RED),(.96,BRAND_ORANGE),(1,BRAND_ORANGE)]))
    b.rect(201,"Orbit top haze",4500,9100,-130,220,540,540,BRAND_RED,270,opacity=45)
    b.rect(202,"Orbit bottom haze",4500,9100,720,1180,550,550,BRAND_YELLOW,275,opacity=9)
    b.text(203,"Orbit title",4500,9100,90,262,900,190,"Monte a academia\nda sua casa.","bold",66,WHITE,"center")
    b.rect(205,"Orbit plate halo",4500,9100,125,545,830,830,WHITE,415,opacity=6)
    b.rect(206,"Orbit plate",4500,9100,140,560,800,800,WHITE,400,opacity=10)
    for lid,opacity in ((216,75),(217,38),(218,16)):
        b.rect(lid,"Orbit scanning light",4500,9100,531,553,18,18,BRAND_YELLOW,9,opacity=opacity)
    b.rect(207,"Hub shadow",4500,9100,348,848,384,242,BLACK,121,opacity=45)
    b.rect(208,"Hub brand capsule",4500,9100,350,840,380,240,INK,120,
           gradient=grad(350,840,730,1080,[(0,[.15,.15,.17,1]),(1,[.02,.02,.03,1])]))
    b.text(209,"Hub category intro",4500,9100,380,972,320,40,
           "TUDO PARA SE MOVER", "semibold",22,WHITE,"center")
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
        b.text(311+i*2,f"Condition {i}",st,1120,380,966,320,50,
               offer,"bold",26,BRAND_YELLOW,"center")
    b.text(330,"Offer note",7100,6400,125,1530,830,48,"*Consulte condições no site.","semibold",28,[1,1,1,.94],"center")

    # S3: preserved clean end-card logic, now within the vertical safe area.
    b.rect(400,"End graphite gradient",13600,3400,0,0,1080,1920,BLACK,
           gradient=grad(0,0,1080,1920,[(0,INK),(.5,[.16,.015,.04,1]),(.76,BRAND_RED),(1,BRAND_ORANGE)]))
    b.rect(401,"End brand halo",13600,3400,900,1130,480,480,BRAND_YELLOW,240,opacity=20)
    b.text(403,"End slogan",13600,3400,95,776,890,174,
           "Sua saúde,\nnosso impulso.","bold",76,WHITE,"center")
    b.text(404,"End categories",13600,3400,96,1010,888,120,
           "Esteiras • Bicicletas • Musculação\nAcessórios e muito mais", "medium",34,[.84,.84,.86,1],"center")
    from PIL import ImageFont
    domain="www.casadofitness.com.br"
    domain_font=ImageFont.truetype(str(BRAND/"fonts"/"BaiJamjuree-Bold.ttf"),50)
    domain_x=round(540-domain_font.getlength(domain)/2)
    for i in range(1,len(domain)+1):   # digitação caractere a caractere, alinhada à esquerda na largura final
        d_start=13600+1100+int((i-1)*55)
        b.text(1000+i,f"Domain typed {i}",d_start,13600+3400-d_start,domain_x,1272,1000,72,
               domain[:i],"bold",50,WHITE)
    b.rect(406,"End accent rule",13600,3400,440,970,200,5,BRAND_YELLOW,3)
    b.rect(407,"End domain rule",13600,3400,440,1356,200,5,BRAND_YELLOW,3)

    # Existing story begins after the requested one-second, deliberate click.
    for action in b.front:
        action["activeRange"]["start"] += 1000
    for layer in doc["composition"]["layers"]:
        layer["activeRange"]["start"] += 1000
    b.rect(700,"Click opening backdrop",0,1000,0,0,1080,1920,PAPER,
           gradient=grad(0,0,1080,1920,[(0,INK),(.30,DARKRED),(.62,BRAND_RED),(.88,BRAND_ORANGE),(1,BRAND_YELLOW)]))
    b.rect(701,"Click opening shadow",0,1000,176,562,728,820,SLATE,52,opacity=50)
    b.rect(702,"Click opening browser",0,1000,180,550,720,820,WHITE,52)
    b.rect(703,"Click opening toolbar",0,1000,180,550,720,84,PAPER,46)
    for lid,x,c in ((704,226,RED),(705,256,SLATE),(706,286,SLATE)):
        b.rect(lid,"Click window dot",0,1000,x,584,16,16,c,8)
    b.rect(707,"Click brand pill",0,1000,270,676,540,150,RED,75,
           gradient=grad(270,676,810,826,[(0,[.98,.13,.18,1]),(1,[.72,.01,.06,1])]))
    b.rect(708,"Click search field",0,1000,240,898,600,112,[.97,.97,.97,1],56)
    b.text(709,"Click search hint",0,1000,290,926,520,56,"Pesquisar equipamentos","medium",34,[.34,.35,.38,1])
    b.rect(710,"Click target",0,1000,390,1120,300,120,RED,60)
    b.text(711,"Click target text",0,1000,391,1150,298,60,"ABRIR","bold",42,WHITE,"center")
    b.rect(712,"Click pulse",640,360,376,1106,328,148,RED,74,opacity=24)
    b.rect(713,"Click pulse inset",640,360,385,1115,310,130,WHITE,65,opacity=95)
    cursor(b,714,715,1000,846,1130)

    actions=WORK/"layers.json"
    actions.write_text(json.dumps([{**a,"insertIndex":0} for a in b.front],ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(actions))
    run("project","checkout","--project",str(PROJECT),"--output",str(edit))
    actual=json.loads(edit.read_text(encoding="utf-8"))
    actual["composition"]["layers"] = doc["composition"]["layers"] + actual["composition"]["layers"]
    add_image(actual,"logo-white",600,"Orbit CDF logo",5500,9100,540,906,(1200,164),11.3)
    add_image(actual,"logo-white",601,"End CDF logo",14600,3400,540,620,(1200,164),22)
    add_image(actual,"logo-white",602,"Click CDF logo",0,1000,540,751,(1200,164),17.5)
    add_image(actual,"logo-white",603,"Search CDF logo",1000,4500,540,516,(1200,164),12)

    priority_ids={220+i*10+j for i in range(6) for j in (2,3)} | {602,603,710,711,714,715,165,166,169}
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
    for lid in (714,715):   # ponta do cursor termina na borda direita do botão, fora do texto
        anim += [keys(lid,"positionX",[(0,0,LINEAR),(650,-172,LINEAR),(1000,-172,LINEAR)]),
                 keys(lid,"positionY",[(0,0,LINEAR),(650,46,LINEAR),(1000,46,LINEAR)])]
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
        anim.append(keys(lid,"opacity",[(0,0,LINEAR),(450,0,LINEAR),(1050,100,EASE_OUT),(4500,100,LINEAR)]))
    anim.append(keys(163,"scaleX",[(0,0,LINEAR),(950,0,LINEAR),(3700,100,EASE_OUT),(4500,100,LINEAR)]))
    for lid in (168,):
        x,y=layer_map[lid]["transform"]["position"]
        anim.append(keys(lid,"positionY",[(0,y+56,LINEAR),(760,y,EASE_OUT),(4500,y-8,LINEAR)]))
    anim.append(keys(169,"positionY",[(0,56,LINEAR),(760,0,EASE_OUT),(4500,-8,LINEAR)]))
    for lid in (165,166):   # ponta do cursor termina na borda direita de ENCONTRAR, fora do texto
        anim += [keys(lid,"positionX",[(0,0,LINEAR),(3500,0,LINEAR),(4140,-208,EASE_INOUT),(4500,-208,LINEAR)]),
                 keys(lid,"positionY",[(0,0,LINEAR),(3500,0,LINEAR),(4140,208,EASE_INOUT),(4500,208,LINEAR)]),
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
        delay=300+i*620          # uma categoria por vez, com fade leve
        highlight=4300+i*700     # destaque só depois de todas presentes
        for lid in (220+i*10,221+i*10,222+i*10,223+i*10,224+i*10,500+i):
            x,y=layer_map[lid]["transform"]["position"]
            dx,dy=x-cx,y-cy
            xp=[];yp=[]
            for t in range(0,9101,150):
                entry=ease01((t-delay)/700)
                radius=362+13*entry
                turn=ORBIT_DEG*ease01(t/8500)   # giro único do anel: as categorias nunca se aproximam
                a=math.radians(angle+turn)
                xp.append((t,540+radius*math.cos(a)+dx,LINEAR))
                yp.append((t,960+radius*math.sin(a)+dy,LINEAR))
            anim += [keys(lid,"positionX",xp),keys(lid,"positionY",yp)]
            if lid != 224+i*10:
                anim.append(keys(lid,"opacity",[(0,0,LINEAR),(delay,0,LINEAR),
                                                (delay+700,100,EASE_OUT),(9100,100,LINEAR)]))
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
    anim += [keys(600,"scaleX",[(0,10.4,LINEAR),(850,11.3,EASE_OUT),(9100,11.5,LINEAR)]),
             keys(600,"scaleY",[(0,10.4,LINEAR),(850,11.3,EASE_OUT),(9100,11.5,LINEAR)])]
    # a tagline do hub cede o lugar à condição de cada vez e volta no fim
    anim.append(keys(209,"opacity",[(0,0,LINEAR),(480,100,EASE_OUT),(2500,100,LINEAR),(2700,0,EASE_OUT),
                                    (7100,0,LINEAR),(7400,100,EASE_OUT),(9100,100,LINEAR)]))
    for i in range(4):
        for lid in (311+i*2,):
            x,y=layer_map[lid]["transform"]["position"]
            anim += [keys(lid,"positionY",[(0,y+18,LINEAR),(220,y,EASE_OUT),(900,y,LINEAR),(1120,y-9,LINEAR)]),
                     keys(lid,"opacity",[(0,0,LINEAR),(180,100,EASE_OUT),(900,100,LINEAR),(1120,0,LINEAR)])]
    anim.append(keys(330,"opacity",[(0,0,LINEAR),(300,100,EASE_OUT),(6400,100,LINEAR)]))
    for lid,delay in ((601,0),(403,300),(406,550),(404,800),(407,2600)):
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
             keys(406,"scaleX",[(0,0,LINEAR),(550,0,LINEAR),(1200,100,EASE_OUT)]),
             keys(407,"scaleX",[(0,0,LINEAR),(2600,0,LINEAR),(3200,100,EASE_OUT)]),
             keys(401,"positionX",[(0,1105,LINEAR),(3400,1140,LINEAR)])]
    animfile=WORK/"animations.json"
    animfile.write_text(json.dumps(anim,ensure_ascii=False),encoding="utf-8")
    run("project","apply","--project",str(PROJECT),"--actions",str(animfile))
    stamps=[0,350,680,950,1100,1900,3300,4900,5600,6500,7600,8500,9600,10700,11800,13000,14500,15100,16000,16800,17800]
    run("filmstrip","--project",str(PROJECT),"--timestamps-ms",*map(str,stamps),
        "--tile-width","270","--tile-height","480","--items-per-row","6",
        "--output",str(OUT/"previews"/"filmstrip_stories-9x16_v09.png"))
    for t in (0.35,0.75,1.15,3.2,6.7,8.5,10.4,13.2,17.8):
        run("preview","--project",str(PROJECT),"--time",str(t),
            "--output",str(OUT/"previews"/f"v09_{t:.2f}.png"))


def export():
    silent=WORK/"silent_2160p60.mp4"
    run("export","--project",str(PROJECT),"--output",str(silent),"--fps","60","--resolution","4k")
    score=WORK/"trilha-original-v09.wav"
    sound(duration=DURATION,typing=(2.05,4.65),transitions=(5.5,14.6),output=score)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(silent),"-i",str(score),
                    "-map","0:v:0","-map","1:a:0","-vf","scale=1080:1920:flags=lanczos+accurate_rnd,format=yuv420p",
                    "-c:v","libx264","-preset","medium","-crf","16","-c:a","aac","-b:a","192k",
                    "-ar","48000","-ac","2","-af","loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-t",str(DURATION),"-movflags","+faststart",str(FINAL)],check=True)
    if not FINAL.exists() or FINAL.stat().st_size<100000:
        raise RuntimeError("v09 output missing")
    shutil.copy2(PROJECT,OUT/"projeto"/"stories-9x16.tsrct")
    shutil.copy2(OUT/"previews"/"filmstrip_stories-9x16_v09.png",
                 OUT/"previews"/"filmstrip_stories-9x16.png")
    shutil.copy2(WORK/"layout_qa.json",OUT/"previews"/"layout_qa_v09.json")
    (OUT/"versao.txt").write_text("v09\n",encoding="utf-8")
    print(FINAL)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage",choices=("preview","export"),default="preview")
    args=parser.parse_args()
    build() if args.stage=="preview" else export()
