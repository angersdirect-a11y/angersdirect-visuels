"""Courbe du smic net mensuel (2020-2026), style Angers Direct, 1080x1350. Lancer depuis la racine du dépôt."""
import sys
PAGE = sys.argv[2] if len(sys.argv) > 2 else '2/2'
SORTIE = sys.argv[1] if len(sys.argv) > 1 else '2026-11-09/smic-1502-euros-courbe.png'
sys.path.insert(0, 'outils')
from visuel import polices, ICI, COULEURS, ACCENTS
from playwright.sync_api import sync_playwright

NB = ' '
pts = [("2020-01", 1218.60), ("2021-01", 1230.60), ("2021-10", 1258.22), ("2022-01", 1269.02), ("2022-05", 1302.64),
       ("2022-08", 1329.05), ("2023-01", 1353.07), ("2023-05", 1383.08), ("2024-01", 1398.69), ("2024-11", 1426.30),
       ("2026-01", 1443.11), ("2026-06", 1477.93), ("2026-12", 1501.58)]


def m(s):
    y, mo = map(int, s.split('-'))
    return (y - 2020) * 12 + mo - 1


X0, X1, Y0, Y1 = 170, 990, 1060, 500
t0, t1, v0, v1 = 0, m("2027-01"), 1200, 1520
X = lambda t: X0 + (t - t0) / (t1 - t0) * (X1 - X0)
Y = lambda v: Y0 - (v - v0) / (v1 - v0) * (Y0 - Y1)
path, first = "", True
for s, v in pts:
    x, y = X(m(s)), Y(v)
    path += f"M{x:.1f},{y:.1f}" if first else f"H{x:.1f}V{y:.1f}"
    first = False
path += f"H{X(t1):.1f}"
acc, coul = ACCENTS['ÉCONOMIE'], COULEURS['ÉCONOMIE']
grid = "".join(f'<line x1="{X0}" x2="{X1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="rgba(255,255,255,.12)" stroke-width="2"/>'
               f'<text x="{X0 - 18}" y="{Y(v) + 10:.1f}" text-anchor="end" font-size="28" fill="#9FB0C6">{str(v)[0]}{NB}{str(v)[1:]}{NB}€</text>'
               for v in (1200, 1300, 1400, 1500))
years = "".join(f'<text x="{X((y - 2020) * 12 + 6):.1f}" y="{Y0 + 50}" text-anchor="middle" font-size="28" fill="#9FB0C6">{y}</text>'
                for y in range(2020, 2027))
dots = "".join(f'<circle cx="{X(m(s)):.1f}" cy="{Y(v):.1f}" r="7" fill="{acc}" stroke="#0F1B2D" stroke-width="3"/>' for s, v in pts[:-1])
lab = [("2020-01", 1218.60, "Janv. 2020", f"1{NB}219{NB}€", 0, -30), ("2024-01", 1398.69, "Janv. 2024", f"1{NB}399{NB}€", -130, -30),
       ("2026-06", 1477.93, "Juin 2026", f"1{NB}478{NB}€", -150, 44)]
labels = "".join(f'<text x="{X(m(s)) + dx:.1f}" y="{Y(v) + dy - 34:.1f}" font-size="26" fill="#C9D3E0">{a}</text>'
                 f'<text x="{X(m(s)) + dx:.1f}" y="{Y(v) + dy:.1f}" font-size="34" font-weight="600" fill="#FFFFFF">{b}</text>'
                 for s, v, a, b, dx, dy in lab)
xe, ye = X(m("2026-12")), Y(1501.58)
svg = f'''<svg width="1080" height="1180" style="position:absolute;left:0;top:0" font-family="Barlow">{grid}{years}
<path d="{path}" fill="none" stroke="{acc}" stroke-width="5" stroke-linejoin="round"/>{dots}{labels}
<circle cx="{xe:.1f}" cy="{ye:.1f}" r="12" fill="{acc}" stroke="#0F1B2D" stroke-width="4"/>
<rect x="{xe - 225:.1f}" y="{ye - 150:.1f}" width="245" height="96" rx="10" fill="{acc}"/>
<text x="{xe - 102:.1f}" y="{ye - 115:.1f}" text-anchor="middle" font-size="26" font-weight="600" fill="#0F1B2D">Déc. 2026</text>
<text x="{xe - 102:.1f}" y="{ye - 72:.1f}" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="46" fill="#0F1B2D">≈{NB}1{NB}502{NB}€</text>
<line x1="{xe:.1f}" x2="{xe:.1f}" y1="{ye - 54:.1f}" y2="{ye - 14:.1f}" stroke="{acc}" stroke-width="3"/></svg>'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{polices()}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1350px;position:relative;overflow:hidden;background:#0F1B2D;color:#fff;font-family:Barlow">
<div style="position:absolute;left:72px;top:70px;padding:6px 22px;background:{coul};transform:skewX(-12deg)"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:34px">ÉCONOMIE</div></div>
<div style="position:absolute;left:72px;right:72px;top:150px;font-family:'Barlow Condensed';font-weight:700;font-size:76px;line-height:1.02">Le smic passe la barre<br>des <span style="color:{acc}">1{NB}500{NB}€</span> net</div>
<div style="position:absolute;left:72px;right:72px;top:330px;font-size:30px;line-height:1.35;color:#C9D3E0">Smic mensuel net pour un temps plein (35{NB}heures par semaine), depuis 2020</div>
{svg}
<div style="position:absolute;left:0;right:0;top:1190px;border-top:2px solid rgba(255,255,255,.12)"></div>
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:1236px;width:150px">
<div style="position:absolute;right:72px;top:1262px;font-size:28px;color:#C9D3E0">{PAGE}</div>
</div></body></html>'''
open('/tmp/smic.html', 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    pg.goto('file:///tmp/smic.html')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(400)
    pg.screenshot(path=SORTIE)
    b.close()
print('ok')
