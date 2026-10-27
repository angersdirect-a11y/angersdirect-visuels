"""Story Angers Direct 1080x1920 « points clés » : photo en haut, titre, liste de chiffres clés, encart final.

Usage : python3 outils/story_points.py fiche.json sortie.png
Fiche : {"photo": "outils/sel/x.jpg", "credit": "", "rubrique": "SOCIÉTÉ", "titre": "...",
         "points": [{"chiffre": "2028", "texte": "..."}, ...3 à 5],
         "encart": {"label": "À SUIVRE", "texte": "..."}}
Contenu utile entre 250 et 1670 px de haut (zones libres des interfaces Instagram et Facebook).
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
from visuel import COULEURS, polices, e, ICI


def corps(f):
    couleur = COULEURS.get(f['rubrique'].upper(), COULEURS['ACTU'])
    photo = pathlib.Path(f['photo']).resolve()
    credit = (f'<div style="position:absolute;right:16px;top:16px;padding:4px 10px;background:rgba(15,27,45,0.55);'
              f'font-size:18px;color:#FFFFFF">{e(f["credit"])}</div>') if f.get('credit') else ''
    points = ''.join(
        f'''<div style="display:flex;align-items:center;gap:34px;padding:18px 0;border-top:2px solid rgba(255,255,255,0.12)">
<div style="flex:0 0 250px;font-family:'Barlow Condensed';font-weight:700;font-size:84px;line-height:1;color:#B497FF">{e(p['chiffre'])}</div>
<div style="font-weight:500;font-size:34px;line-height:1.3;color:#FFFFFF">{e(p['texte'])}</div></div>'''
        for p in f['points'])
    enc = f.get('encart')
    encart = (f'''<div style="margin-top:34px;padding:26px 30px;background:{couleur};border-radius:6px">
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:30px;letter-spacing:2px;color:#FFFFFF;opacity:.9">{e(enc['label'])}</div>
<div style="font-weight:600;font-size:36px;line-height:1.3;color:#FFFFFF;margin-top:6px">{e(enc['texte'])}</div></div>''') if enc else ''
    return f'''<div style="width:1080px;height:1920px;position:relative;overflow:hidden;background:#0F1B2D;font-family:Barlow;color:#FFFFFF">
<img src="file://{photo}" style="position:absolute;left:0;top:0;width:1080px;height:900px;object-fit:cover">
<div style="position:absolute;left:0;top:0;width:1080px;height:900px;background:linear-gradient(180deg,rgba(13,22,38,0.6) 0%,rgba(13,22,38,0) 30%,rgba(13,22,38,0) 55%,#0F1B2D 100%)"></div>
{credit}
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:250px;width:210px;filter:drop-shadow(0 2px 10px rgba(0,0,0,0.6))">
<div style="position:absolute;left:72px;right:72px;top:660px;display:flex;flex-direction:column;align-items:flex-start">
<div style="padding:6px 22px;background:{couleur};transform:skewX(-12deg);margin-bottom:24px"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:34px;letter-spacing:1px">{e(f['rubrique'].upper())}</div></div>
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:84px;line-height:1.02;margin-bottom:30px">{e(f['titre'])}</div>
<div style="width:100%">{points}</div>{encart}</div>
<div style="position:absolute;right:72px;top:1760px;font-weight:500;font-size:28px;letter-spacing:1px;color:#C9D3E0">angersdirect.fr</div></div>'''


def main():
    f = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    tmp = sortie.with_suffix('.html')
    tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{corps(f)}</body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + str(tmp))
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(sortie), clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1920})
        b.close()
    tmp.unlink()
    print('ok', sortie)


if __name__ == '__main__':
    main()
