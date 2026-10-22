"""Génère un visuel Angers Direct (PNG 1080x1350) à partir d'une fiche JSON.

Usage : python3 outils/visuel.py fiche.json sortie.png

Installation préalable (une fois par session) :
    cd outils && npm i --silent @fontsource/barlow@5 @fontsource/barlow-condensed@5

Fiche « meteo » :
    {"type": "meteo", "jour": "Vendredi 23 octobre",
     "creneaux": [{"label": "Matin", "icone": "nuage", "temp": 11}, ...3 créneaux],
     "bas": "Min. 10° · Max. 15° · Vent 20 km/h · Pluie 60 %"}
    icônes : soleil, eclaircies, nuage, pluie_faible, pluie, orage

Fiche « article » (photo en haut, style Angers Direct) :
    {"type": "article", "photo": "chemin/photo.jpg", "credit": "",
     (crédit vide pour les photos d'illustration ; à remplir seulement si la licence l'impose, ex. Wikimedia CC BY-SA)
     "bloc": "SCORE FINAL", "rubrique": "SPORT", "titre": "...", "texte": "..."}
    rubriques : ACTU, SPORT, CULTURE, SOCIÉTÉ, ÉCONOMIE, ENVIRONNEMENT, MÉTÉO
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
FONTS = ICI / 'node_modules/@fontsource'
COULEURS = {'ACTU': 'linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%)',
            'SPORT': 'linear-gradient(90deg,#3DCB6E 0%,#16834A 100%)',
            'CULTURE': 'linear-gradient(90deg,#F0587F 0%,#B01E4C 100%)',
            'SOCIÉTÉ': 'linear-gradient(90deg,#9B6BFF 0%,#5B28CC 100%)',
            'ÉCONOMIE': 'linear-gradient(90deg,#F5B841 0%,#C2701A 100%)',
            'ENVIRONNEMENT': 'linear-gradient(90deg,#2FD3AB 0%,#0F8069 100%)',
            'MÉTÉO': 'linear-gradient(90deg,#3AA3F5 0%,#1665D8 100%)'}
BLOC = 'linear-gradient(90deg,#3AA3F5 0%,#1665D8 100%)'

NUAGE = '<g fill="#FFFFFF"><circle cx="66" cy="{y1}" r="28"/><circle cx="102" cy="{y2}" r="36"/><circle cx="134" cy="{y3}" r="22"/><rect x="38" y="{y4}" width="118" height="26" rx="13"/></g>'


def nuage(dy=0):
    return NUAGE.format(y1=76 + dy, y2=64 + dy, y3=86 + dy, y4=82 + dy)


SOLEIL = ('<g stroke="#FFC21A" stroke-width="9" stroke-linecap="round">'
          + ''.join(f'<line x1="{90 + 52 * c:.0f}" y1="{90 + 52 * s:.0f}" x2="{90 + 74 * c:.0f}" y2="{90 + 74 * s:.0f}"/>'
                    for c, s in [(1, 0), (.707, .707), (0, 1), (-.707, .707), (-1, 0), (-.707, -.707), (0, -1), (.707, -.707)])
          + '</g><circle cx="90" cy="90" r="38" fill="#FFC21A"/>')
ICONES = {
    'soleil': SOLEIL,
    'eclaircies': '<g transform="translate(-22,-26) scale(0.8)">' + SOLEIL + '</g>' + nuage(30),
    'nuage': '<g fill="#FFFFFF" opacity="0.6"><circle cx="50" cy="62" r="20"/><circle cx="76" cy="52" r="26"/><rect x="30" y="60" width="84" height="24" rx="12"/></g>' + nuage(24),
    'pluie_faible': nuage(0) + '<g stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"><line x1="78" y1="128" x2="70" y2="148"/><line x1="114" y1="128" x2="106" y2="148"/></g>',
    'pluie': nuage(-10) + '<g stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"><line x1="62" y1="116" x2="54" y2="136"/><line x1="96" y1="116" x2="88" y2="136"/><line x1="130" y1="116" x2="122" y2="136"/><line x1="79" y1="148" x2="71" y2="168"/><line x1="113" y1="148" x2="105" y2="168"/></g>',
    'orage': nuage(-10) + '<path d="M98 112 L80 146 H98 L88 174 L120 134 H102 L114 112 Z" fill="#FFC21A"/>',
}


def polices():
    out = ''
    for fam, d, ws in [('Barlow', 'barlow', [300, 400, 500, 600]), ('Barlow Condensed', 'barlow-condensed', [600, 700, 800])]:
        for w in ws:
            out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{FONTS}/{d}/files/{d}-latin-{w}-normal.woff2') format('woff2');}}\n"
    return out


def e(t):
    return html.escape(str(t))


def meteo(f):
    cartes = ''
    for c in f['creneaux']:
        cartes += f'''<div style="border-radius:24px;background:rgba(255,255,255,0.15);display:flex;flex-direction:column;align-items:center;padding-top:40px;box-sizing:border-box">
<div style="font-weight:500;font-size:34px">{e(c['label'])}</div>
<svg width="190" height="190" viewBox="0 0 180 180" style="margin-top:30px">{ICONES[c['icone']]}</svg>
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:116px;line-height:1;margin-top:34px">{e(c['temp'])}°</div></div>'''
    return f'''<div style="width:1080px;height:1350px;position:relative;overflow:hidden;background:linear-gradient(135deg,#5AB6F1 0%,#3B9DE6 45%,#1E8DE3 100%);font-family:Barlow;color:#FFFFFF">
<div style="position:absolute;left:72px;top:70px;width:133px;height:50px;background:#FFFFFF;transform:skewX(-12deg);display:flex;align-items:center;justify-content:center"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:700;font-size:32px;letter-spacing:2px;color:#1C8FE3">MÉTÉO</div></div>
<div style="position:absolute;left:70px;top:196px;font-family:'Barlow Condensed';font-weight:700;font-size:112px;line-height:1">Angers</div>
<div style="position:absolute;left:72px;top:336px;font-weight:500;font-size:36px">{e(f['jour'])}</div>
<div style="position:absolute;left:70px;top:470px;width:940px;height:520px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:20px">{cartes}</div>
<div style="position:absolute;left:72px;right:72px;top:1056px;font-weight:500;font-size:34px">{e(f['bas'])}</div>
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:1205px;width:215px">
<div style="position:absolute;right:70px;top:1228px;font-weight:500;font-size:30px;letter-spacing:2px">angersdirect.fr</div></div>'''


def article(f):
    couleur = COULEURS.get(f['rubrique'].upper(), COULEURS['ACTU'])
    photo = pathlib.Path(f['photo']).resolve()
    credit = ''
    if f.get('credit'):
        credit = f'<div style="position:absolute;right:16px;top:16px;padding:4px 10px;background:rgba(15,27,45,0.55);font-size:18px;color:#FFFFFF">{e(f["credit"])}</div>'
    return f'''<div style="width:1080px;height:1350px;position:relative;overflow:hidden;background:#FFFFFF;font-family:Barlow;color:#0F1B2D">
<img src="file://{photo}" style="position:absolute;left:0;top:0;width:1080px;height:640px;object-fit:cover">
{credit}
<div style="position:absolute;left:0;top:570px;height:140px;box-sizing:border-box;padding:0 70px 0 72px;background:{BLOC};clip-path:polygon(0 0,100% 0,calc(100% - 30px) 100%,0 100%);display:flex;align-items:center;font-family:'Barlow Condensed';font-weight:700;font-size:84px;line-height:1;color:#FFFFFF">{e(f['bloc'])}</div>
<div style="position:absolute;left:72px;right:72px;top:755px;display:flex;flex-direction:column;align-items:flex-start;gap:26px">
<div style="padding:6px 22px;background:{couleur};transform:skewX(-12deg)"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:34px;letter-spacing:1px;color:#FFFFFF">{e(f['rubrique'].upper())}</div></div>
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:66px;line-height:1.08">{e(f['titre'])}</div>
<div style="font-size:32px;line-height:1.55;color:#3B4656">{e(f['texte'])}</div></div>
<img src="file://{ICI}/assets/logo_bleu.png" style="position:absolute;left:72px;top:1222px;width:146px">
<div style="position:absolute;right:70px;top:1240px;font-size:26px;letter-spacing:1px;color:#3B4656">angersdirect.fr</div></div>'''


def main():
    fiche = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    corps = {'meteo': meteo, 'article': article}[fiche['type']](fiche)
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{corps}</body></html>"
    tmp = sortie.with_suffix('.html')
    tmp.write_text(page)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        pg.goto('file://' + str(tmp))
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(sortie), clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
        b.close()
    tmp.unlink()
    print('ok', sortie)


if __name__ == '__main__':
    main()
