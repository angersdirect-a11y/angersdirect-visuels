"""Story Angers Direct 1080x1920 native, version story de la carte « fiche » (sans photo) : gros chiffre sur bande
de couleur, rubrique, titre et 2 à 4 paragraphes courts avec filet de couleur.

Usage : python3 outils/story_fiche.py fiche.json sortie.png
Fiche : {"rubrique": "ACTU", "chiffre": "17,54 %", "titre": "...",
         "paragraphes": [{"label": "COLLÈGES ET LYCÉES", "texte": "..."}, ...] (label facultatif), "page": "4/7"}
Contenu utile entre 250 et 1670 px de haut (zones libres des interfaces Instagram et Facebook).
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
from visuel import ACCENTS, COULEURS, polices, e, ICI


def corps(f):
    couleur = COULEURS.get(f['rubrique'].upper(), COULEURS['ACTU'])
    paras = ''.join(
        f'''<div style="border-left:8px solid #1D5FD0;padding:4px 0 4px 28px">
{f'<div style="font-family:Barlow Condensed;font-weight:700;font-size:32px;letter-spacing:2px;color:#1D5FD0;margin-bottom:6px">{e(p["label"])}</div>' if p.get('label') else ''}
<div style="font-weight:500;font-size:36px;line-height:1.34;color:#1F2A3A">{e(p['texte'])}</div></div>'''
        for p in f['paragraphes'])
    page = e(f.get('page', 'angersdirect.fr'))
    return f'''<div style="width:1080px;height:1920px;position:relative;overflow:hidden;background:#FFFFFF;font-family:Barlow;color:#0F1B2D">
<div style="position:absolute;left:0;top:0;width:1080px;height:600px;background:{couleur}"></div>
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:250px;width:170px">
<div style="position:absolute;left:72px;right:72px;top:360px;font-family:'Barlow Condensed';font-weight:700;font-size:200px;line-height:1;color:#FFFFFF">{e(f['chiffre'])}</div>
<div style="position:absolute;left:72px;right:72px;top:650px;display:flex;flex-direction:column;align-items:flex-start;gap:26px">
<div style="padding:6px 22px;background:{couleur};transform:skewX(-12deg)"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:34px;letter-spacing:1px;color:#FFFFFF">{e(f['rubrique'].upper())}</div></div>
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:74px;line-height:1.02">{e(f['titre'])}</div>
<div id="paras" style="display:flex;flex-direction:column;gap:28px;margin-top:6px">{paras}</div></div>
<div style="position:absolute;left:72px;top:1620px;font-weight:500;font-size:28px;letter-spacing:1px;color:#3B4656">angersdirect.fr</div>
<div style="position:absolute;right:72px;top:1620px;font-weight:500;font-size:28px;letter-spacing:1px;color:#3B4656">{page}</div></div>'''


def main():
    f = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{corps(f)}</body></html>"
    tmp = sortie.with_suffix('.html')
    tmp.write_text(page)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{tmp}')
        pg.wait_for_timeout(300)
        bas = pg.evaluate("document.getElementById('paras').getBoundingClientRect().bottom")
        pg.screenshot(path=str(sortie))
        b.close()
    tmp.unlink()
    print('ok', sortie, f'bas du texte {bas:.0f} / 1590' + ('  DÉBORDE' if bas > 1590 else ''))


if __name__ == '__main__':
    main()
