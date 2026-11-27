"""Visuel « choc » d'avant-match : logo contre logo, plein cadre sur la photo du stade.

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
TAILLES = {'post': (1080, 1350), 'story': (1080, 1920), 'paysage': (1920, 1080)}


def e(t):
    return html.escape(str(t))


def polices():
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


def main():
    f = json.loads(pathlib.Path(sys.argv[1]).read_text())
    W, H = TAILLES[f.get('format', 'post')]
    out = pathlib.Path(sys.argv[2]).resolve()
    tmp = out.with_suffix('.html')
    tmp.write_text(page(f))
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
