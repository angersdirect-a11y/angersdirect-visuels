"""Visuel « travaux · circulation » / info trafic Angers Direct (modèle angers-direct-modele-travaux-circulation).

Usage : python3 outils/alerte.py fiche.json sortie.png
Fiche : {"format": "post" (1080x1350) ou "story" (1080x1920), "tag": "TRAVAUX · CIRCULATION",
         "titre": "...", "blocs": [{"label": "OÙ", "texte": "..."}, ...]}
Jamais de bloc « SOURCE » : la rédaction n'affiche aucune source (voir LISEZMOI.md).
Fond bleu nuit, bandes jaunes en haut, étiquette jaune, blocs avec filet jaune, logo et angersdirect.fr en bas.
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
FONTS = ICI / 'node_modules/@fontsource'
JAUNE, NUIT = '#FFC21A', '#0F1B2D'
BC = "font-family:'Barlow Condensed'"


def e(t):
    return html.escape(str(t))


def polices():
    out = ''
    for fam, d, ws in [('Barlow', 'barlow', [400, 500, 600]), ('Barlow Condensed', 'barlow-condensed', [600, 700])]:
        for w in ws:
            out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{FONTS}/{d}/files/{d}-latin-{w}-normal.woff2') format('woff2');}}\n"
    return out


def page(f, W, H):
    story = H > 1500
    bandes = ''.join(f'<div style="position:absolute;top:0;left:{x}px;width:64px;height:46px;background:{JAUNE};transform:skewX(-20deg)"></div>'
                     for x in range(10, W + 60, 120))
    blocs = ''.join(f'''<div style="border-left:7px solid {JAUNE};padding:6px 0 6px 30px;margin-bottom:{40 if story else 34}px">
<div style="font-size:{32 if story else 29}px;letter-spacing:3px;color:{JAUNE};font-weight:500">{e(b['label'])}</div>
<div style="{BC};font-weight:600;font-size:{42 if story else 37}px;line-height:1.18;margin-top:6px">{e(b['texte'])}</div></div>'''
                    for b in f['blocs'])
    top = 300 if story else 150
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{NUIT};color:#FFFFFF;font-family:Barlow">
{bandes}
<div style="position:absolute;left:72px;right:72px;top:{top}px">
<div style="display:inline-block;background:{JAUNE};padding:4px 26px;transform:skewX(-12deg)"><div style="transform:skewX(12deg);{BC};font-weight:600;font-size:36px;letter-spacing:2px;color:{NUIT}">{e(f['tag'])}</div></div>
<div style="{BC};font-weight:700;font-size:{88 if story else 80}px;line-height:1.08;margin:{70 if story else 56}px 0 {64 if story else 50}px">{e(f['titre'])}</div>
{blocs}</div>
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;bottom:{220 if story else 72}px;width:216px">
<div style="position:absolute;right:72px;bottom:{246 if story else 92}px;font-size:28px;letter-spacing:2px;color:#D3D5D9">angersdirect.fr</div></div>'''


def main():
    f = json.load(open(sys.argv[1]))
    W, H = (1080, 1920) if f.get('format') == 'story' else (1080, 1350)
    sortie = pathlib.Path(sys.argv[2]).resolve()
    tmp = sortie.with_suffix('.html')
    tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{page(f, W, H)}</body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto('file://' + str(tmp))
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(500)
        # garde-fou : le contenu ne doit pas déborder du cadre
        bas = pg.evaluate("Math.max(...[...document.querySelectorAll('body *')].map(n => n.getBoundingClientRect().bottom))")
        pg.screenshot(path=str(sortie), clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        b.close()
    tmp.unlink()
    print('ok', sortie, 'bas du contenu', int(bas), '/', H)


if __name__ == '__main__':
    main()
