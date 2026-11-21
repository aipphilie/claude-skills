# Концепт пряника: генерирует SVG вариантов и рендерит PNG через Playwright
import sys

BROWN="#B8692E"; DARK="#7A3F17"; GLAZE="#FFF6E8"; ICING="#FFFFFF"; Y="#FFD60A"

def limbs(cx,cy,r,color,arm="shock"):
    # руки и ноги как у человечка: палочки с полукруглыми концами
    w=r*0.26
    if arm=="shock":   # руки к щекам/вверх
        arms=f'<path d="M{cx-r*0.9},{cy} Q{cx-r*1.35},{cy-r*0.4} {cx-r*1.15},{cy-r*0.95}" />'\
             f'<path d="M{cx+r*0.9},{cy} Q{cx+r*1.35},{cy-r*0.4} {cx+r*1.15},{cy-r*0.95}" />'
    elif arm=="type":
        arms=f'<path d="M{cx-r*0.85},{cy+r*0.2} Q{cx-r*1.0},{cy+r*0.7} {cx-r*0.5},{cy+r*0.85}" />'\
             f'<path d="M{cx+r*0.85},{cy+r*0.2} Q{cx+r*1.0},{cy+r*0.7} {cx+r*0.5},{cy+r*0.85}" />'
    else:
        arms=f'<path d="M{cx-r*0.95},{cy+r*0.1} L{cx-r*1.35},{cy+r*0.55}" /><path d="M{cx+r*0.95},{cy+r*0.1} L{cx+r*1.35},{cy+r*0.55}" />'
    legs=f'<path d="M{cx-r*0.35},{cy+r*0.9} L{cx-r*0.4},{cy+r*1.45}" /><path d="M{cx+r*0.35},{cy+r*0.9} L{cx+r*0.4},{cy+r*1.45}" />'
    return f'<g stroke="{color}" stroke-width="{w}" stroke-linecap="round" fill="none">{arms}{legs}</g>'

def shadow(cx,cy,r):
    return f'<ellipse cx="{cx}" cy="{cy+r*1.55}" rx="{r*0.85}" ry="{r*0.12}" fill="#000" opacity="0.12"/>'

def mouth_shock(cx,cy,r):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.16}" ry="{r*0.22}" fill="#2A1206"/>'\
           f'<ellipse cx="{cx}" cy="{cy+r*0.1}" rx="{r*0.09}" ry="{r*0.07}" fill="#E0505A"/>'

def var_a(cx,cy,r,arm="shock"):
    # «Классика»: круглый глазированный пряник, только рот (как у человечка)
    drips=""
    import math
    pts=[]
    for i in range(13):
        a=math.pi*(1.08+0.84*i/12)
        x=cx+r*0.97*math.cos(a); yb=cy+r*0.97*math.sin(a)
        d=r*(0.10 if i%2 else 0.22)
        pts.append((x,yb,d))
    path=f'M{cx-r*0.97},{cy-r*0.2} '
    path+=f'A{r*0.97},{r*0.97} 0 0 1 {cx+r*0.97},{cy-r*0.2} '
    for x,yb,d in reversed(pts):
        path+=f'L{x},{yb+d} '
    path+='Z'
    glaze=f'<clipPath id="cl{int(cx)}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><path clip-path="url(#cl{int(cx)})" d="{path}" fill="{GLAZE}" opacity="0.92"/>'
    return shadow(cx,cy,r)+limbs(cx,cy,r,DARK,arm)+\
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BROWN}"/>'+glaze+\
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{DARK}" stroke-width="{r*0.04}"/>'+\
        mouth_shock(cx,cy+r*0.42,r)

def var_b(cx,cy,r,arm="shock"):
    # «Глазурь-лицо»: имбирный круг, белая глазурь — глаза-точки, рот, обводка-волна
    import math
    wave=""
    n=28
    d="M"
    for i in range(n+1):
        a=2*math.pi*i/n
        rr=r*0.84+(r*0.035 if i%2 else -r*0.035)
        d+=f'{cx+rr*math.cos(a)},{cy+rr*math.sin(a)} '
    return shadow(cx,cy,r)+limbs(cx,cy,r,DARK,arm)+\
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BROWN}"/>'+\
        f'<polyline points="{d[1:]}" fill="none" stroke="{ICING}" stroke-width="{r*0.06}" stroke-linejoin="round"/>'+\
        f'<circle cx="{cx-r*0.3}" cy="{cy-r*0.15}" r="{r*0.13}" fill="{ICING}"/><circle cx="{cx+r*0.3}" cy="{cy-r*0.15}" r="{r*0.13}" fill="{ICING}"/>'+\
        f'<circle cx="{cx-r*0.3}" cy="{cy-r*0.13}" r="{r*0.05}" fill="#2A1206"/><circle cx="{cx+r*0.3}" cy="{cy-r*0.13}" r="{r*0.05}" fill="#2A1206"/>'+\
        f'<ellipse cx="{cx}" cy="{cy+r*0.33}" rx="{r*0.17}" ry="{r*0.21}" fill="none" stroke="{ICING}" stroke-width="{r*0.06}"/>'

def var_c(cx,cy,r,arm="shock"):
    # «Тульский-силуэт»: плоский тёмный пряник в стиле канала, белая обводка-стикер, только рот, надкус
    return shadow(cx,cy,r)+limbs(cx,cy,r,"#5B2C0E",arm)+\
        f'<mask id="bite{int(cx)}"><rect x="0" y="0" width="4000" height="4000" fill="#fff"/>'\
        f'<circle cx="{cx+r*0.82}" cy="{cy-r*0.72}" r="{r*0.28}" fill="#000"/><circle cx="{cx+r*1.02}" cy="{cy-r*0.42}" r="{r*0.22}" fill="#000"/></mask>'+\
        f'<g mask="url(#bite{int(cx)})"><circle cx="{cx}" cy="{cy}" r="{r+r*0.06}" fill="#fff"/>'\
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#8A4A1E"/>'\
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.8}" fill="none" stroke="#6E3812" stroke-width="{r*0.03}" stroke-dasharray="{r*0.06} {r*0.1}"/></g>'+\
        mouth_shock(cx,cy+r*0.3,r)

def label(x,y,t,sub):
    w=len(t)*25+50
    return f'<rect x="{x-w/2}" y="{y-48}" width="{w}" height="64" rx="6" fill="{Y}"/>'\
           f'<text x="{x}" y="{y}" font-family="Oswald, Inter" font-weight="800" font-size="36" text-anchor="middle">{t}</text>'\
           f'<text x="{x}" y="{y+60}" font-family="Inter" font-size="26" fill="#555" text-anchor="middle">{sub}</text>'

def sheet():
    W,H=1620,900
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="#fff"/>'
    s+=f'<text x="{W/2}" y="90" font-family="Inter" font-weight="800" font-size="54" text-anchor="middle">ПРЯНИК — 3 варианта</text>'
    for i,(fn,t,sub) in enumerate([(var_a,"A · ГЛАЗУРЬ","только рот, как у человечка"),(var_b,"B · ЛИЦО ИЗ ГЛАЗУРИ","глаза-точки, больше эмоций"),(var_c,"C · ТЁМНЫЙ ТУЛЬСКИЙ","стикер-обводка, надкус")]):
        cx=270+i*540
        s+=fn(cx,390,150)
        s+=label(cx,730,t,sub)
    return s+'</svg>'

def scene(fn):
    W,H=1080,1920
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="#fff"/>'
    s+=f'<rect x="150" y="290" width="780" height="100" rx="8" fill="{Y}"/><text x="540" y="362" font-family="Inter" font-weight="900" font-size="60" text-anchor="middle">ПЕРВЫЙ РАЗ В CLAUDE</text>'
    s+='<g transform="translate(540,0) scale(0.72) translate(-540,51)">'
    s+='<rect x="190" y="560" width="700" height="440" rx="22" fill="#1E1E1E"/><rect x="215" y="585" width="650" height="390" rx="8" fill="#0F0F0F"/>'
    s+='<text x="245" y="650" font-family="monospace" font-size="34" fill="#D97757">✻ Claude Code</text>'
    s+='<text x="245" y="720" font-family="monospace" font-size="32" fill="#ddd">&gt; сделай мне сайт</text>'
    s+='<text x="245" y="780" font-family="monospace" font-size="32" fill="#ddd">  а ты кто? 🙂</text>'
    s+='<rect x="245" y="815" width="18" height="34" fill="#ddd"/>'
    s+='<path d="M130,1000 L950,1000 L1000,1045 L80,1045 Z" fill="#2B2B2B"/></g>'
    s+=fn(540,1060,140,"shock")
    s+='<rect x="650" y="880" width="260" height="84" rx="42" fill="#fff" stroke="#111" stroke-width="5"/><text x="780" y="937" font-family="Inter" font-weight="800" font-size="40" text-anchor="middle">ЧЁ?!</text>'
    s+='<text x="540" y="1360" font-family="Inter" font-weight="800" font-size="50" text-anchor="middle">Пряник впервые открыл</text>'
    s+=f'<text x="540" y="1425" font-family="Inter" font-weight="800" font-size="50" text-anchor="middle">Claude Code и <tspan style="paint-order:stroke" stroke="{Y}" stroke-width="22" stroke-linejoin="round">в ах*е</tspan></text>'
    return s+'</svg>'

def render(svg,out,w,h):
    open(out.replace('.png','.svg'),'w').write(svg)
    import subprocess; subprocess.run(['node','shot.js',out.replace('.png','.svg'),out,str(w),str(h)],check=True)

if __name__=="__main__":
    render(sheet(),"varianty.png",1620,900)
    render(scene(var_a),"kadr-A.png",1080,1920)
    render(scene(var_b),"kadr-B.png",1080,1920)
    render(scene(var_c),"kadr-C.png",1080,1920)
