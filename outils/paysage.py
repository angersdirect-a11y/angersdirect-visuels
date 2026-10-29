"""Visuel paysage Angers Direct 1200x675 (16:9) pour X, à partir d'une fiche JSON.

Usage : python3 outils/paysage.py fiche.json sortie.png
Fiche : {"photo": "outils/sel/x.jpg", "rubrique": "ÉCONOMIE", "titre": "...", "date": "...",
         "cadrage": "50% 50%"}   (date et cadrage facultatifs ; les mots entre crochets s'affichent dans la teinte de la rubrique)
Photo à gauche, panneau bleu nuit à droite. Jamais de source ni de crédit sur la photo.
"""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright
from visuel import ACCENTS, COULEURS, polices, e, ICI


def corps(f):
    rub = f['rubrique'].upper()
    couleur = COULEURS.get(rub, COULEURS['ACTU'])
    accent = ACCENTS.get(rub, ACCENTS['ACTU'])
    photo = pathlib.Path(f['photo']).resolve()
    titre = re.sub(r'\[(.+?)\]', rf'<span style="color:{accent}">\1</span>', e(f['titre']))
    date = f'<div style="font-weight:500;font-size:26px;color:#C9D2DE;margin-top:22px">{e(f["date"])}</div>' if f.get('date') else ''
    return f'''<div style="width:1200px;height:675px;position:relative;overflow:hidden;background:#0F1B2D;font-family:Barlow;color:#FFFFFF">
<img src="file://{photo}" style="position:absolute;left:0;top:0;width:600px;height:675px;object-fit:cover;object-position:{f.get('cadrage', '50% 50%')}">
<div style="position:absolute;left:520px;top:0;width:80px;height:675px;background:linear-gradient(90deg,rgba(15,27,45,0) 0%,#0F1B2D 100%)"></div>
<div style="position:absolute;left:640px;right:56px;top:0;bottom:110px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
<div style="padding:5px 18px;background:{couleur};transform:skewX(-12deg);margin-bottom:24px"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:28px;letter-spacing:1px">{e(rub)}</div></div>
<div id="titre" style="font-family:'Barlow Condensed';font-weight:700;font-size:56px;line-height:1.06">{titre}</div>
{date}</div>
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:640px;top:575px;width:130px">
<div style="position:absolute;right:56px;top:598px;font-size:22px;letter-spacing:1px;color:#C9D2DE">angersdirect.fr</div></div>'''


def main():
    f = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    tmp = sortie.with_suffix('.html')
    tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{corps(f)}</body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 675})
        pg.goto('file://' + str(tmp))
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(sortie), clip={'x': 0, 'y': 0, 'width': 1200, 'height': 675})
        b.close()
    tmp.unlink()
    print('ok', sortie)


if __name__ == '__main__':
    main()
