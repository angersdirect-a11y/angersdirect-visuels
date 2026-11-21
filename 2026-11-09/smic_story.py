"""Story native 1080x1920 du smic à 1 502 € (pleine page, sans bandes floutées). Lancer depuis la racine du dépôt.
Contenu utile entre 250 et 1670 px (zones libres des interfaces Instagram et Facebook)."""
import sys
SORTIE = sys.argv[1] if len(sys.argv) > 1 else '2026-11-09/smic-1502-euros-story.png'
sys.path.insert(0, 'outils')
from visuel import polices, ICI, COULEURS, ACCENTS
from playwright.sync_api import sync_playwright

NB = ' '
pts = [("2020-01", 1218.60), ("2021-01", 1230.60), ("2021-10", 1258.22), ("2022-01", 1269.02), ("2022-05", 1302.64),
       ("2022-08", 1329.05), ("2023-01", 1353.07), ("2023-05", 1383.08), ("2024-01", 1398.69), ("2024-11", 1426.30),
       ("2026-01", 1443.11), ("2026-06", 1477.93), ("2026-12", 1501.58)]


def m(s):
    y, mo = map(int, s.split('-'))
    return (y - 2020) * 12 + mo - 1


# Zone du graphique dans la page
X0, X1, Y0, Y1 = 170, 1000, 1360, 900
t0, t1, v0, v1 = 0, m("2027-01"), 1200, 1520
X = lambda t: X0 + (t - t0) / (t1 - t0) * (X1 - X0)
Y = lambda v: Y0 - (v - v0) / (v1 - v0) * (Y0 - Y1)
path, area, first = "", "", True
for s, v in pts:
    x, y = X(m(s)), Y(v)
    path += f"M{x:.1f},{y:.1f}" if first else f"H{x:.1f}V{y:.1f}"
    first = False
path += f"H{X(t1):.1f}"
area = path + f"V{Y0}H{X0}Z"
acc, coul = ACCENTS['ÉCONOMIE'], COULEURS['ÉCONOMIE']
grid = "".join(f'<line x1="{X0}" x2="{X1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="rgba(255,255,255,.12)" stroke-width="2"/>'
               f'<text x="{X0 - 18}" y="{Y(v) + 10:.1f}" text-anchor="end" font-size="28" fill="#9FB0C6">{str(v)[0]}{NB}{str(v)[1:]}{NB}€</text>'
               for v in (1200, 1300, 1400, 1500))
years = "".join(f'<text x="{X((y - 2020) * 12 + 6):.1f}" y="{Y0 + 48}" text-anchor="middle" font-size="28" fill="#9FB0C6">{y}</text>'
                for y in (2020, 2022, 2024, 2026))
dots = "".join(f'<circle cx="{X(m(s)):.1f}" cy="{Y(v):.1f}" r="7" fill="{acc}" stroke="#0F1B2D" stroke-width="3"/>' for s, v in pts[:-1])
lab = [("2020-01", 1218.60, "Janv. 2020", f"1{NB}219{NB}€", 0, -30), ("2026-06", 1477.93, "Juin 2026", f"1{NB}478{NB}€", -190, 60)]
labels = "".join(f'<text x="{X(m(s)) + dx:.1f}" y="{Y(v) + dy - 34:.1f}" font-size="26" fill="#C9D3E0">{a}</text>'
                 f'<text x="{X(m(s)) + dx:.1f}" y="{Y(v) + dy:.1f}" font-size="34" font-weight="600" fill="#FFFFFF">{b}</text>'
                 for s, v, a, b, dx, dy in lab)
xe, ye = X(m("2026-12")), Y(1501.58)
svg = f'''<svg width="1080" height="1920" style="position:absolute;left:0;top:0" font-family="Barlow">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{acc}" stop-opacity=".28"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></linearGradient></defs>
{grid}{years}<path d="{area}" fill="url(#g)"/>
<path d="{path}" fill="none" stroke="{acc}" stroke-width="6" stroke-linejoin="round"/>{dots}{labels}
<circle cx="{xe:.1f}" cy="{ye:.1f}" r="14" fill="{acc}" stroke="#0F1B2D" stroke-width="4"/></svg>'''

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{polices()}body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;position:relative;overflow:hidden;background:radial-gradient(circle at 85% 18%,rgba(245,184,65,.30) 0%,rgba(245,184,65,0) 45%),linear-gradient(180deg,#14233A 0%,#0F1B2D 55%,#0B1422 100%);color:#fff;font-family:Barlow">
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:250px;width:190px">
<div style="position:absolute;left:72px;top:380px;padding:6px 22px;background:{coul};transform:skewX(-12deg)"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:600;font-size:34px;letter-spacing:1px">ÉCONOMIE</div></div>
<div style="position:absolute;left:72px;right:72px;top:450px;font-family:'Barlow Condensed';font-weight:700;font-size:58px;line-height:1.05;color:#C9D3E0">Le smic net au 1er{NB}décembre</div>
<div style="position:absolute;left:66px;top:505px;font-family:'Barlow Condensed';font-weight:700;font-size:230px;line-height:1;color:{acc}">1{NB}502{NB}€</div>
<div style="position:absolute;left:72px;right:72px;top:760px;font-size:36px;line-height:1.35;color:#FFFFFF">Le smic passe la barre des 1{NB}500{NB}€ net par mois pour un temps plein.</div>
{svg}
<div style="position:absolute;left:72px;right:72px;top:1460px;display:flex;gap:24px">
<div style="flex:1;padding:24px 28px;border:2px solid rgba(255,255,255,.14);border-radius:8px"><div style="font-family:'Barlow Condensed';font-weight:700;font-size:72px;line-height:1;color:{acc}">+1,6{NB}%</div><div style="font-size:30px;margin-top:8px;color:#C9D3E0">de hausse</div></div>
<div style="flex:1;padding:24px 28px;border:2px solid rgba(255,255,255,.14);border-radius:8px"><div style="font-family:'Barlow Condensed';font-weight:700;font-size:72px;line-height:1;color:{acc}">+24{NB}€</div><div style="font-size:30px;margin-top:8px;color:#C9D3E0">net par mois</div></div>
</div>
<div style="position:absolute;right:72px;top:1760px;font-weight:500;font-size:28px;letter-spacing:1px;color:#C9D3E0">angersdirect.fr</div>
</div></body></html>'''
open('/tmp/smic_story.html', 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file:///tmp/smic_story.html')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(400)
    pg.screenshot(path=SORTIE)
    b.close()
print('ok')
