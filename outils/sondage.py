"""Visuel « sondage » Angers Direct : barres horizontales, même couleur pour tous (neutralité).

Usage : python3 outils/sondage.py fiche.json sortie.png
Fiche : {"format": "post" | "story", "rubrique": "ACTU", "titre": "...", "sous_titre": "...",
         "lignes": [{"nom": "Marine Le Pen", "parti": "RN", "valeur": 31, "affiche": "31 %"}, ...],
         "mentions": "fiche technique obligatoire (loi du 19 juillet 1977)"}
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from visuel import polices, COULEURS, ICI  # noqa

e = html.escape


def corps(f):
    story = f.get('format') == 'story'
    W, H = 1080, (1920 if story else 1350)
    couleur = COULEURS.get(f['rubrique'].upper(), COULEURS['ACTU'])
    lignes = f['lignes']
    vmax = max(l['valeur'] for l in lignes)
    top = 600 if story else 385
    zone = (960 if story else 715)
    pas = zone / len(lignes)
    barre_h = pas * 0.62
    larg_max = 520
    rows = []
    for i, l in enumerate(lignes):
        y = top + i * pas
        w = max(8, larg_max * l['valeur'] / vmax)
        fs_nom = 30 if story else 23
        rows.append(f'''<div style="position:absolute;left:72px;top:{y:.1f}px;width:330px;height:{barre_h:.1f}px;display:flex;flex-direction:column;justify-content:center">
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:{fs_nom + 4}px;line-height:1;color:#FFFFFF;white-space:nowrap">{e(l['nom'])}</div>
<div style="font-size:{fs_nom - 6}px;line-height:1.2;color:#9FB0C6;white-space:nowrap">{e(l.get('parti', ''))}</div></div>
<div style="position:absolute;left:410px;top:{y:.1f}px;width:{w:.1f}px;height:{barre_h:.1f}px;background:linear-gradient(90deg,#4FA8FF 0%,#1D5FD0 100%);border-radius:0 6px 6px 0"></div>
<div style="position:absolute;left:{410 + w + 16:.1f}px;top:{y:.1f}px;height:{barre_h:.1f}px;display:flex;align-items:center;font-family:'Barlow Condensed';font-weight:700;font-size:{fs_nom + 10}px;color:#FFFFFF">{e(l['affiche'])}</div>''')
    titre_top = 170 if story else 70
    logo = f'<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:{H - (150 if story else 92)}px;width:{170 if story else 150}px">'
    mentions_top = top + zone + (30 if story else 14)
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;background:#0F1B2D;font-family:Barlow;color:#FFFFFF">
<div style="position:absolute;left:72px;right:72px;top:{titre_top}px;display:flex;flex-direction:column;align-items:flex-start">
<div style="padding:6px 22px;background:{couleur};transform:skewX(-12deg);margin-bottom:22px"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:{34 if story else 30}px;letter-spacing:1px;color:#FFFFFF">{e(f['rubrique'].upper())}</div></div>
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:{76 if story else 62}px;line-height:1.02">{e(f['titre'])}</div>
<div style="font-weight:500;font-size:{32 if story else 28}px;line-height:1.35;color:#C9D3E0;margin-top:14px">{e(f['sous_titre'])}</div></div>
{''.join(rows)}
<div style="position:absolute;left:72px;right:72px;top:{mentions_top:.0f}px;font-size:{22 if story else 19}px;line-height:1.4;color:#9FB0C6">{e(f['mentions'])}</div>
{logo}
<div style="position:absolute;right:72px;top:{H - (122 if story else 74)}px;font-weight:500;font-size:26px;letter-spacing:1px;color:#C9D3E0">angersdirect.fr</div></div>'''


def main():
    f = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    H = 1920 if f.get('format') == 'story' else 1350
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{corps(f)}</body></html>"
    tmp = sortie.with_suffix('.html'); tmp.write_text(page)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': H})
        pg.goto(f'file://{tmp}'); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
        pg.screenshot(path=str(sortie)); b.close()
    tmp.unlink()
    print('ok', sortie)


if __name__ == '__main__':
    main()
