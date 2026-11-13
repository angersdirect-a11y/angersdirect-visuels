"""Visuel d'alerte Angers Direct, deux modèles (champ « modele » de la fiche) :
- « trafic » (par défaut) : modèle angers-direct-modele-travaux-circulation, bandes jaunes et noires en haut.
  RÉSERVÉ aux problèmes de circulation, accidents de la route, travaux (règle de la rédaction, 13 novembre 2026).
- « info » : alerte info nationale ou internationale (catastrophe, attentat, décès, décision majeure...),
  sans bandes de chantier : en-tête « ALERTE INFO » avec point rouge, étiquette et filets rouges.

Usage : python3 outils/alerte.py fiche.json sortie.png
Fiche : {"modele": "trafic" | "info", "format": "post" (1080x1350) ou "story" (1080x1920), "tag": "TRAVAUX · CIRCULATION",
         "titre": "...", "blocs": [{"label": "OÙ", "texte": "..."}, ...]}
Jamais de bloc « SOURCE » : la rédaction n'affiche aucune source (voir LISEZMOI.md).
Fond bleu nuit, bandes jaunes en haut, étiquette jaune, blocs avec filet jaune, logo et angersdirect.fr en bas.
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
FONTS = ICI / 'node_modules/@fontsource'
JAUNE, NUIT, ROUGE, ROUGE_CLAIR = '#FFC21A', '#0F1B2D', '#E5322D', '#FF8A80'
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
    info = f.get('modele', 'trafic') == 'info'
    accent = ROUGE if info else JAUNE
    label_c = ROUGE_CLAIR if info else JAUNE
    if info:
        haut = f'''<div style="position:absolute;left:72px;top:{190 if story else 70}px;display:flex;align-items:center;gap:18px">
<div style="width:26px;height:26px;border-radius:50%;background:{ROUGE};box-shadow:0 0 0 10px rgba(229,50,45,.25)"></div>
<div style="{BC};font-weight:700;font-size:40px;letter-spacing:6px">ALERTE INFO</div></div>
<div style="position:absolute;left:72px;right:72px;top:{262 if story else 140}px;height:2px;background:rgba(255,255,255,.18)"></div>'''
        tag_fond, tag_txt = ROUGE, '#FFFFFF'
    else:
        haut = ''.join(f'<div style="position:absolute;top:0;left:{x}px;width:64px;height:46px;background:{JAUNE};transform:skewX(-20deg)"></div>'
                       for x in range(10, W + 60, 120))
        tag_fond, tag_txt = JAUNE, NUIT
    blocs = ''.join(f'''<div style="border-left:7px solid {accent};padding:6px 0 6px 30px;margin-bottom:{40 if story else 34}px">
<div style="font-size:{32 if story else 29}px;letter-spacing:3px;color:{label_c};font-weight:500">{e(b['label'])}</div>
<div style="{BC};font-weight:600;font-size:{42 if story else 37}px;line-height:1.18;margin-top:6px">{e(b['texte'])}</div></div>'''
                    for b in f['blocs'])
    top = (340 if info else 300) if story else (210 if info else 150)
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{NUIT};color:#FFFFFF;font-family:Barlow">
{haut}
<div style="position:absolute;left:72px;right:72px;top:{top}px">
<div style="display:inline-block;background:{tag_fond};padding:4px 26px;transform:skewX(-12deg)"><div style="transform:skewX(12deg);{BC};font-weight:600;font-size:36px;letter-spacing:2px;color:{tag_txt}">{e(f['tag'])}</div></div>
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
