"""MODÈLE OFFICIEL « UNE CHOC » (validé par Valentin le 27/11/2026, SCO-Lens) : format "une_choc".
À utiliser comme photo de couverture de l'article en une le jour des matchs importants.
    python3 outils/choc.py outils/exemples/une-choc.json sortie.png
Bleu nuit, halo bleu derrière le club angevin, halo doré derrière l'adversaire, grand éclair blanc entre les logos,
« LE CHOC » en haut, étiquette en dégradé bleu (« AUJOURD'HUI · 17H15 »), rond central en transparence en bas.
Ne rien ajouter (pas de projecteurs, pas d'arcs, pas de VS encadré). Photo de couverture sans légende ni crédit.

Visuel « choc » d'avant-match : logo contre logo, plein cadre sur la photo du stade.

Usage : python3 outils/choc.py fiche.json sortie.png
Fiche : {"format": "post" | "story" | "paysage", "fond": "stade-raymond-kopa.jpg",
         "accroche": "LE CHOC", "competition": "LIGUE 1", "journee": "12e journée",
         "dom": {"nom": "Angers SCO", "logo": "angers-sco"}, "ext": {"nom": "RC Lens", "logo": "rc-lens"},
         "date": "SAMEDI 28 NOVEMBRE", "heure": "17H15", "stade": "Stade Raymond-Kopa"}
Polices : cd outils && npm i --silent (une fois par session).
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
FONTS = ICI / 'node_modules/@fontsource'
TAILLES = {'post': (1080, 1350), 'story': (1080, 1920), 'paysage': (1920, 1080), 'une': (1920, 1080), 'duel': (1920, 1080), 'impact': (1920, 1080), 'duel2': (1920, 1080), 'nuit': (1920, 1080), 'une_choc': (1920, 1080)}


def e(t):
    return html.escape(str(t))


def polices():
    __import__('charte').verifier_polices(FONTS)
    out = ''
    for fam, d, ws in [('Barlow', 'barlow', [500, 600]), ('Barlow Condensed', 'barlow-condensed', [600, 700, 800])]:
        for w in ws:
            out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{FONTS}/{d}/files/{d}-latin-{w}-normal.woff2') format('woff2');}}\n"
    return out


def badge(logo, taille, couleur):
    return (f'<div style="width:{taille}px;height:{taille}px;border-radius:50%;background:#FFFFFF;display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 0 0 10px rgba(255,255,255,0.12),0 0 90px 10px {couleur},0 30px 60px rgba(0,0,0,0.55)">'
            f'<img src="file://{ICI}/logos/{logo}.png" style="width:{int(taille*0.68)}px;height:{int(taille*0.68)}px;object-fit:contain"></div>')


def page(f):
    W, H = TAILLES[f.get('format', 'post')]
    paysage = W > H
    fond = ICI / 'photos' / f.get('fond', 'stade-raymond-kopa.jpg')
    t = min(W, H)
    story = H > 1500
    logo_t = int(t * (0.24 if paysage else 0.36 if story else 0.34))
    vs_t = int(t * (0.13 if paysage else 0.15))
    nom_t = int(t * 0.05)
    # Disposition : logos face à face, VS au centre, infos en bas.
    if paysage:
        haut_logos, bas_infos = int(H * 0.45), 40
    else:
        haut_logos, bas_infos = int(H * (0.47 if story else 0.45)), int(H * (0.11 if story else 0.07))
    col = lambda side: f'''<div style="display:flex;flex-direction:column;align-items:center;gap:{int(t*0.03)}px;width:{int(W*0.36)}px">
        {badge(f[side]['logo'], logo_t, 'rgba(90,182,241,0.55)' if side == 'dom' else 'rgba(255,196,0,0.45)')}
        <div style="font-family:'Barlow Condensed';font-weight:700;font-size:{nom_t}px;letter-spacing:1px;text-transform:uppercase;text-shadow:0 4px 18px rgba(0,0,0,0.8)">{e(f[side]['nom'])}</div></div>'''
    return f'''<html><head><meta charset="utf-8"><style>{polices()}*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body style="width:{W}px;height:{H}px;overflow:hidden;background:#0B1422">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#FFFFFF;font-family:Barlow">
  <img src="file://{fond}" style="position:absolute;top:0;right:0;height:100%;width:{'230%' if paysage else '100%'};object-fit:cover;object-position:{f.get('cadrage','100% 45%')};filter:blur(1.5px) saturate(1.15) contrast(1.1) brightness(0.75)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,15,28,0.92) 0%,rgba(8,15,28,0.35) 32%,rgba(8,15,28,0.30) 55%,rgba(8,15,28,0.95) 100%)"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% {int(haut_logos/H*100)}%,rgba(90,182,241,0.28) 0%,rgba(90,182,241,0) 55%)"></div>
  <div style="position:absolute;left:-10%;top:{haut_logos-int(t*0.02)}px;width:120%;height:{int(t*0.012)}px;background:linear-gradient(90deg,rgba(90,182,241,0),#5AB6F1,rgba(255,255,255,0.9),#F5C400,rgba(245,196,0,0));transform:rotate(-6deg);opacity:0.85"></div>
  <img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:{int(t*0.065)}px;top:{int(t*0.06)}px;width:{int(t*0.19)}px">
  <div style="position:absolute;right:{int(t*0.065)}px;top:{int(t*0.065)}px;padding:6px 26px;background:#FFFFFF;transform:skewX(-12deg)">
    <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:700;font-size:{int(t*0.034)}px;letter-spacing:2px;color:#0F1B2D">AVANT-MATCH</div></div>
  <div style="position:absolute;left:0;right:0;top:{haut_logos-logo_t//2-int(t*(0.17 if paysage else 0.33 if story else 0.26))}px;text-align:center">
    <div style="font-family:'Barlow Condensed';font-weight:800;font-size:{int(t*(0.19 if story else 0.16))}px;line-height:0.9;letter-spacing:4px;text-shadow:0 8px 40px rgba(0,0,0,0.7)">{e(f.get('accroche','LE CHOC'))}</div>
    <div style="margin-top:{int(t*0.015)}px;font-family:Barlow;font-weight:600;font-size:{int(t*0.03)}px;letter-spacing:6px;color:#5AB6F1">{e(f.get('competition','LIGUE 1'))} · {e(f['journee'].upper())}</div>
  </div>
  <div style="position:absolute;left:0;right:0;top:{haut_logos-logo_t//2}px;display:flex;align-items:flex-start;justify-content:center;gap:{int(W*0.02)}px">
    {col('dom')}
    <div style="height:{logo_t}px;display:flex;align-items:center"><div style="background:#FFFFFF;padding:{int(vs_t*0.06)}px {int(vs_t*0.22)}px;transform:skewX(-12deg);box-shadow:0 20px 50px rgba(0,0,0,0.6)">
      <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:{vs_t}px;line-height:1;color:#0F1B2D">VS</div></div></div>
    {col('ext')}
  </div>
  <div style="position:absolute;left:0;right:0;bottom:{bas_infos}px;text-align:center">
    <div style="font-family:'Barlow Condensed';font-weight:700;font-size:{int(t*(0.065 if paysage else 0.075))}px;line-height:1;letter-spacing:2px">{e(f['date'])}</div>
    <div style="display:inline-block;margin-top:{int(t*0.02)}px;padding:4px 38px;background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);transform:skewX(-12deg);box-shadow:0 14px 40px rgba(29,95,208,0.45)">
      <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:{int(t*(0.09 if paysage else 0.11))}px;line-height:1.05;color:#FFFFFF">{e(f['heure'])}</div></div>
    <div style="margin-top:{int(t*0.025)}px;font-family:Barlow;font-weight:500;font-size:{int(t*0.032)}px;letter-spacing:1px;opacity:0.92">{e(f['stade'])} · angersdirect.fr</div>
  </div>
</div></body></html>'''


def page_une(f):
    """Couverture d'article (une du site) : logos et VS dans la zone centrale haute, rien en bas (le titre du site s'y superpose)."""
    W, H = 1920, 1080
    fond = ICI / 'photos' / f.get('fond', 'stade-raymond-kopa.jpg')
    L = 330
    cy = 400
    return f'''<html><head><meta charset="utf-8"><style>{polices()}*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body style="width:{W}px;height:{H}px;overflow:hidden;background:#0B1422">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#FFFFFF;font-family:Barlow">
  <img src="file://{fond}" style="position:absolute;top:0;right:0;height:100%;width:230%;object-fit:cover;object-position:{f.get('cadrage','100% 45%')};filter:blur(1.5px) saturate(1.15) contrast(1.1) brightness(0.8)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,15,28,0.55) 0%,rgba(8,15,28,0.25) 40%,rgba(8,15,28,0.55) 70%,rgba(8,15,28,0.9) 100%)"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 37%,rgba(90,182,241,0.35) 0%,rgba(90,182,241,0) 50%)"></div>
  <div style="position:absolute;left:-10%;top:{cy-6}px;width:120%;height:12px;background:linear-gradient(90deg,rgba(90,182,241,0),#5AB6F1,rgba(255,255,255,0.9),#F5C400,rgba(245,196,0,0));transform:rotate(-5deg);opacity:0.85"></div>
  <div style="position:absolute;left:0;right:0;top:{cy-L//2-120}px;text-align:center;font-family:Barlow;font-weight:600;font-size:40px;letter-spacing:10px;color:#5AB6F1;text-shadow:0 2px 14px rgba(0,0,0,0.8)">{e(f.get('competition','LIGUE 1'))} · {e(f['journee'].upper())}</div>
  <div style="position:absolute;left:0;right:0;top:{cy-L//2}px;display:flex;align-items:center;justify-content:center;gap:60px">
    {badge(f['dom']['logo'], L, 'rgba(90,182,241,0.6)')}
    <div style="background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);padding:6px 34px;transform:skewX(-12deg);box-shadow:0 20px 50px rgba(0,0,0,0.6)">
      <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:150px;line-height:1;color:#FFFFFF">VS</div></div>
    {badge(f['ext']['logo'], L, 'rgba(255,196,0,0.5)')}
  </div>
</div></body></html>'''


def page_duel(f):
    """Couverture « duel » : écran coupé en diagonale aux couleurs des deux clubs, logos sans pastille, VS au centre."""
    W, H = 1920, 1080
    cg, cd = f.get('couleurs_dom', ['#111111', '#2A2A2A']), f.get('couleurs_ext', ['#E2001A', '#FFD600'])
    L = 360; cy = 410
    rayures = 'repeating-linear-gradient(90deg,#0E0E0E 0px,#0E0E0E 60px,#1C1C1C 60px,#1C1C1C 120px)'
    return f'''<html><head><meta charset="utf-8"><style>{polices()}*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body style="width:{W}px;height:{H}px;overflow:hidden">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#FFFFFF;font-family:Barlow;background:#0B1422">
  <div style="position:absolute;inset:0;background:{rayures};clip-path:polygon(0 0,58% 0,42% 100%,0 100%)"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 28% 38%,rgba(255,255,255,0.18) 0%,rgba(255,255,255,0) 45%);clip-path:polygon(0 0,58% 0,42% 100%,0 100%)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(135deg,{cd[0]} 0%,#B00014 45%,#7A000E 100%);clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 72% 38%,rgba(255,214,0,0.45) 0%,rgba(255,214,0,0) 45%);clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)"></div>
  <div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:linear-gradient(90deg,transparent calc(50% - 18px),#FFFFFF calc(50% - 18px),#FFFFFF calc(50% + 18px),transparent calc(50% + 18px));transform:skewX(-8.4deg);opacity:0.95;filter:drop-shadow(0 0 30px rgba(90,182,241,0.9))"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(5,10,20,0.85) 100%)"></div>
  <img src="file://{ICI}/logos/{f['dom']['logo']}.png" style="position:absolute;left:{W//2-260-L}px;top:{cy-L//2}px;width:{L}px;height:{L}px;object-fit:contain;filter:drop-shadow(0 0 2px #FFF) drop-shadow(0 0 2px #FFF) drop-shadow(0 20px 40px rgba(0,0,0,0.6))">
  <img src="file://{ICI}/logos/{f['ext']['logo']}.png" style="position:absolute;left:{W//2+260}px;top:{cy-L//2}px;width:{L}px;height:{L}px;object-fit:contain;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.6))">
  <div style="position:absolute;left:50%;top:{cy}px;transform:translate(-50%,-50%) skewX(-12deg);background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);padding:8px 38px;box-shadow:0 20px 60px rgba(0,0,0,0.6)">
    <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:170px;line-height:1;color:#FFFFFF">VS</div></div>
  <div style="position:absolute;left:0;right:0;top:70px;text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:46px;letter-spacing:12px;text-shadow:0 3px 16px rgba(0,0,0,0.8)">{e(f.get('competition','LIGUE 1'))} · {e(f['journee'].upper())}</div>
</div></body></html>'''


def page_impact(f):
    """Couverture « impact » : les deux logos foncent l'un vers l'autre et se percutent au centre (éclair, rayons, éclats, étincelles)."""
    import random
    random.seed(28)
    W, H = 1920, 1080
    L = 330; cy = 400; cx = W // 2
    rayons = ''.join(f'<div style="position:absolute;left:{cx}px;top:{cy}px;width:{random.randint(700,1300)}px;height:{random.choice([3,4,6,8])}px;transform-origin:0 50%;transform:rotate({a + random.uniform(-4,4):.1f}deg);background:linear-gradient(90deg,rgba(255,255,255,0.95),rgba(255,255,255,0))"></div>' for a in range(0, 360, 9))
    eclats = ''
    for _ in range(26):
        a = random.uniform(0, 6.283); d = random.uniform(120, 430)
        import math
        x = cx + math.cos(a) * d; y = cy + math.sin(a) * d * 0.7; t = random.randint(14, 46)
        col = random.choice(['#FFFFFF', '#5AB6F1', '#FFD600', '#E2001A', '#FFFFFF'])
        eclats += f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{t}px;height:{int(t*0.6)}px;background:{col};clip-path:polygon(0 30%,100% 0,70% 100%);transform:rotate({math.degrees(a):.0f}deg);opacity:{random.uniform(0.6,1):.2f};box-shadow:0 0 12px {col}"></div>'
    for _ in range(60):
        a = random.uniform(0, 6.283); d = random.uniform(60, 620)
        import math
        x = cx + math.cos(a) * d; y = cy + math.sin(a) * d * 0.65; r = random.randint(3, 8)
        eclats += f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{r}px;height:{r}px;border-radius:50%;background:#FFF6C8;box-shadow:0 0 {r*3}px #FFD600"></div>'
    def logo(nom, x, rot, sens):
        trace = ''.join(f'<img src="file://{ICI}/logos/{nom}.png" style="position:absolute;left:{x - sens*i*70}px;top:{cy-L//2}px;width:{L}px;height:{L}px;object-fit:contain;opacity:{0.22 - i*0.05:.2f};filter:blur({i*3}px);transform:rotate({rot}deg)">' for i in (3, 2, 1))
        halo = 'drop-shadow(0 0 2px #FFF) drop-shadow(0 0 2px #FFF) ' if nom == 'angers-sco' else ''
        return trace + f'<img src="file://{ICI}/logos/{nom}.png" style="position:absolute;left:{x}px;top:{cy-L//2}px;width:{L}px;height:{L}px;object-fit:contain;transform:rotate({rot}deg);filter:{halo}drop-shadow(0 25px 40px rgba(0,0,0,0.7))">'
    return f'''<html><head><meta charset="utf-8"><style>{polices()}*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body style="width:{W}px;height:{H}px;overflow:hidden">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#FFFFFF;font-family:Barlow;background:radial-gradient(ellipse at 50% 37%,#1D5FD0 0%,#0F2547 35%,#070D19 75%)">
  <div style="position:absolute;inset:0;background:linear-gradient(100deg,rgba(255,255,255,0.10) 0%,rgba(255,255,255,0) 45%),linear-gradient(280deg,rgba(226,0,26,0.45) 0%,rgba(226,0,26,0) 45%)"></div>
  <div style="position:absolute;inset:0;opacity:0.55">{rayons}</div>
  <div style="position:absolute;left:{cx-560}px;top:{cy-380}px;width:1120px;height:760px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,1) 0%,rgba(255,244,190,0.95) 10%,rgba(255,214,0,0.55) 22%,rgba(90,182,241,0.45) 42%,rgba(90,182,241,0) 70%)"></div>
  <div style="position:absolute;left:{cx-18}px;top:{cy-260}px;width:36px;height:520px;background:#FFFFFF;clip-path:polygon(50% 0,70% 22%,40% 38%,75% 55%,35% 72%,60% 100%,45% 100%,20% 74%,55% 56%,15% 40%,45% 22%);filter:drop-shadow(0 0 18px #FFFFFF) drop-shadow(0 0 30px #5AB6F1)"></div>
  {eclats}
  {logo(f['dom']['logo'], cx - L - 30, -8, 1)}
  {logo(f['ext']['logo'], cx + 30, 8, -1)}
  <div style="position:absolute;left:50%;top:{cy+L//2+20}px;transform:translateX(-50%) rotate(-4deg) skewX(-12deg);background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);padding:4px 40px;box-shadow:0 20px 50px rgba(0,0,0,0.6)">
    <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:96px;line-height:1;letter-spacing:6px;color:#FFFFFF">LE CHOC</div></div>
  <div style="position:absolute;left:0;right:0;top:60px;text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:44px;letter-spacing:12px;text-shadow:0 3px 16px rgba(0,0,0,0.8)">{e(f.get('competition','LIGUE 1'))} · {e(f['journee'].upper())}</div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 62%,rgba(5,10,20,0.85) 100%)"></div>
</div></body></html>'''


def page_duel2(f):
    """Couverture « duel » v2 : écran coupé en diagonale, traînées de vitesse vers le centre, étincelles sur la ligne de choc,
    « LE CHOC » en haut et l'horaire du jour sous les logos. Tout le contenu reste au-dessus de 650 px (le titre du site recouvre le bas)."""
    import random, math
    random.seed(7)
    W, H = 1920, 1080
    L = 310; cy = 395; cx = W // 2
    gauche = 'polygon(0 0,57% 0,43% 100%,0 100%)'
    droite = 'polygon(57% 0,100% 0,100% 100%,43% 100%)'
    def trainees(cote):
        out = ''
        for _ in range(16):
            y = random.randint(140, 760); lg = random.randint(260, 620); ep = random.choice([3, 4, 6, 10])
            if cote == 'g':
                x = random.randint(40, 520); grad = 'linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,0.55))'
            else:
                x = random.randint(1180, 1660) - lg // 3; grad = 'linear-gradient(270deg,rgba(255,214,0,0),rgba(255,214,0,0.6))'
            out += f'<div style="position:absolute;left:{x}px;top:{y}px;width:{lg}px;height:{ep}px;background:{grad};transform:rotate(-8deg);border-radius:4px"></div>'
        return out
    etincelles = ''
    for _ in range(70):
        t = random.uniform(0.02, 0.75); xs = cx + (0.07 - 0.14 * t) * W + random.uniform(-90, 90); ys = t * H + random.uniform(-30, 30)
        r = random.randint(3, 9); col = random.choice(['#FFFFFF', '#FFF2B0', '#5AB6F1', '#FFD600'])
        etincelles += f'<div style="position:absolute;left:{xs:.0f}px;top:{ys:.0f}px;width:{r}px;height:{r}px;border-radius:50%;background:{col};box-shadow:0 0 {r*3}px {col}"></div>'
    for _ in range(18):
        t = random.uniform(0.1, 0.6); xs = cx + (0.07 - 0.14 * t) * W + random.uniform(-160, 160); ys = t * H + random.uniform(-60, 60)
        tl = random.randint(16, 40); col = random.choice(['#FFFFFF', '#5AB6F1', '#FFD600'])
        etincelles += f'<div style="position:absolute;left:{xs:.0f}px;top:{ys:.0f}px;width:{tl}px;height:{int(tl*0.55)}px;background:{col};clip-path:polygon(0 35%,100% 0,65% 100%);transform:rotate({random.randint(0,360)}deg);box-shadow:0 0 10px {col}"></div>'
    def logo(nom, x, rot):
        halo = 'drop-shadow(0 0 2px #FFF) drop-shadow(0 0 2px #FFF) ' if nom == 'angers-sco' else ''
        return f'<img src="file://{ICI}/logos/{nom}.png" style="position:absolute;left:{x}px;top:{cy-L//2}px;width:{L}px;height:{L}px;object-fit:contain;transform:rotate({rot}deg);filter:{halo}drop-shadow(0 0 40px rgba(255,255,255,0.25)) drop-shadow(0 25px 40px rgba(0,0,0,0.7))">'
    return f'''<html><head><meta charset="utf-8"><style>{polices()}*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body style="width:{W}px;height:{H}px;overflow:hidden">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#FFFFFF;font-family:Barlow;background:#0B1422">
  <div style="position:absolute;inset:0;background:repeating-linear-gradient(90deg,#0D0D0D 0px,#0D0D0D 64px,#1E1E1E 64px,#1E1E1E 128px);clip-path:{gauche}"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 30% 37%,rgba(255,255,255,0.22) 0%,rgba(255,255,255,0) 42%);clip-path:{gauche}"></div>
  <div style="position:absolute;inset:0;clip-path:{gauche};overflow:hidden">{trainees('g')}</div>
  <div style="position:absolute;inset:0;background:linear-gradient(135deg,#E2001A 0%,#B00014 50%,#6E000C 100%);clip-path:{droite}"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 37%,rgba(255,214,0,0.55) 0%,rgba(255,214,0,0) 42%);clip-path:{droite}"></div>
  <div style="position:absolute;inset:0;clip-path:{droite};overflow:hidden">{trainees('d')}</div>
  <div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:linear-gradient(90deg,transparent calc(50% - 70px),rgba(90,182,241,0.55) calc(50% - 20px),#FFFFFF calc(50% - 9px),#FFFFFF calc(50% + 9px),rgba(255,214,0,0.55) calc(50% + 20px),transparent calc(50% + 70px));transform:skewX(-7.6deg);filter:blur(1px)"></div>
  <div style="position:absolute;left:{cx-330}px;top:{cy-260}px;width:660px;height:520px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,0.85) 0%,rgba(255,240,180,0.45) 18%,rgba(90,182,241,0) 60%)"></div>
  {etincelles}
  {logo(f['dom']['logo'], cx - L - 210, -6)}
  {logo(f['ext']['logo'], cx + 210, 6)}
  <div style="position:absolute;left:50%;top:{cy}px;transform:translate(-50%,-50%) skewX(-12deg);background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);padding:6px 34px;box-shadow:0 0 0 6px rgba(255,255,255,0.9),0 20px 60px rgba(0,0,0,0.6)">
    <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:150px;line-height:1;color:#FFFFFF">VS</div></div>
  <div style="position:absolute;left:0;right:0;top:46px;text-align:center">
    <div style="font-family:'Barlow Condensed';font-weight:800;font-size:96px;line-height:1;letter-spacing:10px;text-shadow:0 6px 30px rgba(0,0,0,0.8)">LE CHOC</div>
    <div style="margin-top:6px;font-family:'Barlow Condensed';font-weight:700;font-size:36px;letter-spacing:12px;color:#FFFFFF;opacity:0.85;text-shadow:0 3px 16px rgba(0,0,0,0.8)">{e(f.get('competition','LIGUE 1'))} · {e(f['journee'].upper())}</div>
  </div>
  <div style="position:absolute;left:50%;top:{cy+L//2+40}px;transform:translateX(-50%) skewX(-12deg);background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);padding:6px 44px;white-space:nowrap;box-shadow:0 20px 50px rgba(0,0,0,0.6)">
    <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:800;font-size:72px;line-height:1.05;letter-spacing:3px;color:#FFFFFF">{e(f.get('quand','AUJOURD\'HUI · 17H15'))}</div></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 66%,rgba(5,10,20,0.8) 100%)"></div>
</div></body></html>'''


def eclair(cx, y0, y1):
    """Grand éclair stylisé (SVG) : forme pleine effilée, cœur blanc, lueur bleue, petites ramifications."""
    h = y1 - y0
    # Forme d'éclair classique, coordonnées relatives (largeur ~0.55 h), pointe en bas.
    rel = [(0.10, 0.00), (0.36, 0.00), (0.16, 0.38), (0.33, 0.38), (-0.12, 1.00), (0.03, 0.52), (-0.15, 0.52), (0.10, 0.00)]
    P = ' '.join(f'{cx + (x - 0.10) * h:.0f},{y0 + y * h:.0f}' for x, y in rel)
    r1 = ' '.join(f'{cx + x * h:.0f},{y0 + y * h:.0f}' for x, y in [(0.18, 0.40), (0.30, 0.47), (0.33, 0.55), (0.42, 0.60)])
    r2 = ' '.join(f'{cx + x * h:.0f},{y0 + y * h:.0f}' for x, y in [(-0.12, 0.53), (-0.22, 0.58), (-0.24, 0.66), (-0.33, 0.70)])
    return (f'<svg width="1920" height="1080" style="position:absolute;left:0;top:0">'
            f'<defs><filter id="g1" x="-80%" y="-50%" width="260%" height="200%"><feGaussianBlur stdDeviation="34"/></filter>'
            f'<filter id="g2" x="-80%" y="-50%" width="260%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>'
            f'<linearGradient id="gc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#CFE9FF"/></linearGradient></defs>'
            f'<polygon points="{P}" fill="#2F8CFF" filter="url(#g1)" opacity="0.95"/>'
            f'<polygon points="{P}" fill="#9FD3FF" filter="url(#g2)"/>'
            f'<polygon points="{P}" fill="#2F8CFF" filter="url(#g1)" opacity="0.9"/>'
            f'<polygon points="{P}" fill="url(#gc)"/></svg>')


def page_nuit(f):
    """Couverture bleu nuit : projecteurs, terrain en perspective, halos derrière les logos, grand éclair (option « eclair »)
    avec arcs électriques vers les deux logos. Contenu utile au-dessus de 650 px (le titre du site recouvre le bas)."""
    import random
    random.seed(11)
    W, H = 1920, 1080
    L = 340; cy = 395; cx = W // 2; dx = 420
    def halo(x, c):
        return (f'<div style="position:absolute;left:{x-420}px;top:{cy-420}px;width:840px;height:840px;border-radius:50%;'
                f'background:radial-gradient(circle,rgba({c},0.75) 0%,rgba({c},0.38) 22%,rgba({c},0.12) 45%,rgba({c},0) 68%)"></div>'
                f'<div style="position:absolute;left:{x-205}px;top:{cy-205}px;width:410px;height:410px;border-radius:50%;border:2px solid rgba({c},0.35);box-shadow:0 0 40px rgba({c},0.35),inset 0 0 40px rgba({c},0.25)"></div>')
    def logo(nom, x):
        net = 'drop-shadow(0 0 1.5px #FFF) drop-shadow(0 0 1.5px #FFF) ' if nom == 'angers-sco' else ''
        return f'<img src="file://{ICI}/logos/{nom}.png" style="position:absolute;left:{x-L//2}px;top:{cy-L//2}px;width:{L}px;height:{L}px;object-fit:contain;filter:{net}drop-shadow(0 30px 50px rgba(0,0,0,0.65))">'
    def arc(x0, x1, y):
        pts = [(x0, y)]; n = 6
        for i in range(1, n):
            pts.append((x0 + (x1 - x0) * i / n, y + random.uniform(-22, 22)))
        pts.append((x1, y + random.uniform(-10, 10)))
        q = ' '.join(f'{a:.0f},{b:.0f}' for a, b in pts)
        return (f'<polyline points="{q}" fill="none" stroke="#7CC4FF" stroke-width="10" opacity="0.5" filter="url(#ga)"/>'
                f'<polyline points="{q}" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.9"/>')
    arcs = ''
    if f.get('arcs'):
        arcs = ('<svg width="1920" height="1080" style="position:absolute;left:0;top:0"><defs><filter id="ga"><feGaussianBlur stdDeviation="6"/></filter></defs>'
                + arc(cx - 70, cx - dx + 175, cy - 20) + arc(cx - 60, cx - dx + 170, cy + 55)
                + arc(cx + 70, cx + dx - 160, cy - 40) + arc(cx + 55, cx + dx - 165, cy + 40) + '</svg>')
    poussiere = ''.join(f'<div style="position:absolute;left:{random.randint(120,1800)}px;top:{random.randint(80,700)}px;width:{r}px;height:{r}px;border-radius:50%;background:#FFFFFF;opacity:{random.uniform(0.15,0.6):.2f};box-shadow:0 0 {r*4}px #9FD3FF"></div>' for r in [random.choice([2, 2, 3, 4]) for _ in range(45)])
    faisceau = lambda x, rot: (f'<div style="position:absolute;left:{x}px;top:-120px;width:520px;height:1300px;transform-origin:50% 0;transform:rotate({rot}deg);'
                               f'background:linear-gradient(180deg,rgba(200,230,255,0.22) 0%,rgba(200,230,255,0.06) 45%,rgba(200,230,255,0) 75%);clip-path:polygon(45% 0,55% 0,100% 100%,0 100%);filter:blur(6px)"></div>')
    terrain = ('<svg width="1920" height="1080" style="position:absolute;left:0;top:0;opacity:0.22">'
               '<ellipse cx="960" cy="905" rx="420" ry="95" fill="none" stroke="#9FD3FF" stroke-width="4"/>'
               '<line x1="0" y1="905" x2="1920" y2="905" stroke="#9FD3FF" stroke-width="4"/>'
               '<circle cx="960" cy="905" r="9" fill="#9FD3FF"/></svg>')
    return f'''<html><head><meta charset="utf-8"><style>{polices()}*{{margin:0;padding:0;box-sizing:border-box}}</style></head>
<body style="width:{W}px;height:{H}px;overflow:hidden">
<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#FFFFFF;font-family:Barlow;background:linear-gradient(180deg,#0C1A34 0%,#0A1528 50%,#071022 72%,#0A1E2E 100%)">
  {faisceau(-120, -28) + faisceau(1520, 28) if f.get('projecteurs') else ''}
  <div style="position:absolute;left:0;right:0;top:700px;height:380px;background:linear-gradient(180deg,rgba(10,40,50,0) 0%,rgba(14,60,64,0.55) 100%)"></div>
  {terrain}
  {halo(cx-dx, '110,190,255')}
  {halo(cx+dx, '255,196,60')}
  {poussiere}
  {arcs}
  {eclair(cx, 245, 800) if f.get('eclair') else ''}
  {logo(f['dom']['logo'], cx-dx)}
  {logo(f['ext']['logo'], cx+dx)}
  <div style="display:{'none' if f.get('eclair') else 'block'};position:absolute;left:0;right:0;top:{cy-80}px;text-align:center;font-family:'Barlow Condensed';font-weight:800;font-style:italic;font-size:150px;line-height:1;background:linear-gradient(180deg,#FFFFFF 0%,#9FD3FF 100%);-webkit-background-clip:text;color:transparent">VS</div>
  <div style="position:absolute;left:0;right:0;top:44px;text-align:center">
    <div style="font-family:'Barlow Condensed';font-weight:700;font-size:34px;letter-spacing:14px;color:#5AB6F1">{e(f.get('competition','LIGUE 1'))} · {e(f['journee'].upper())}</div>
    <div style="margin-top:2px;font-family:'Barlow Condensed';font-weight:800;font-size:112px;line-height:1;letter-spacing:14px;text-shadow:0 0 40px rgba(90,182,241,0.55),0 6px 24px rgba(0,0,0,0.6)">LE CHOC</div>
  </div>
  <div style="position:absolute;left:50%;top:{cy+L//2+52}px;transform:translateX(-50%) skewX(-12deg);background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);padding:6px 42px;white-space:nowrap;box-shadow:0 0 40px rgba(79,168,255,0.45),0 18px 44px rgba(0,0,0,0.5)">
    <div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:700;font-size:62px;line-height:1.05;letter-spacing:4px;color:#FFFFFF">{e(f.get('quand','AUJOURD\'HUI · 17H15'))}</div></div>
</div></body></html>'''


def main():
    f = json.loads(pathlib.Path(sys.argv[1]).read_text())
    W, H = TAILLES[f.get('format', 'post')]
    out = pathlib.Path(sys.argv[2]).resolve()
    tmp = out.with_suffix('.html')
    tmp.write_text(page_nuit({**f, 'eclair': True}) if f.get('format') == 'une_choc' else page_nuit(f) if f.get('format') == 'nuit' else page_duel2(f) if f.get('format') == 'duel2' else page_impact(f) if f.get('format') == 'impact' else page_duel(f) if f.get('format') == 'duel' else page_une(f) if f.get('format') == 'une' else page(f))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto(f'file://{tmp}')
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(out))
        b.close()
    tmp.unlink()


if __name__ == '__main__':
    main()
