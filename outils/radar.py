"""Illustration originale : radar tourelle au bord d'une route de campagne, au crépuscule.
Dessin vectoriel (SVG) rendu en JPG, aucun droit tiers.
Usage : python3 outils/radar.py sortie.jpg"""
import sys, random
from playwright.sync_api import sync_playwright

W, H = 2400, 1600
random.seed(49)

# haies et arbres au loin
arbres = ''
for i in range(70):
    x = random.uniform(-50, W + 50)
    r = random.uniform(30, 75)
    y = 905 - random.uniform(0, 25)
    arbres += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.3:.0f}" ry="{r:.0f}" fill="#1d2a2a"/>'
for i in range(8):
    x = random.choice([random.uniform(80, 700), random.uniform(1650, 2300)])
    s = random.uniform(0.8, 1.3)
    arbres += (f'<rect x="{x - 8 * s:.0f}" y="{900 - 120 * s:.0f}" width="{16 * s:.0f}" height="{120 * s:.0f}" fill="#141d1d"/>'
               f'<ellipse cx="{x:.0f}" cy="{900 - 150 * s:.0f}" rx="{80 * s:.0f}" ry="{95 * s:.0f}" fill="#172322"/>')

# pointillés de la ligne médiane en perspective
tirets = ''
y = 925
while y < H:
    p = (y - 900) / (H - 900)
    h = 10 + 140 * p
    w = 3 + 22 * p
    tirets += f'<polygon points="{1180 - w / 2:.1f},{y:.0f} {1180 + w / 2:.1f},{y:.0f} {1180 + w * 0.6:.1f},{y + h:.0f} {1180 - w * 0.6:.1f},{y + h:.0f}" fill="#e9e4d4" opacity="0.9"/>'
    y += h * 2.1

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#16244a"/><stop offset="0.45" stop-color="#3f4f86"/>
    <stop offset="0.75" stop-color="#c9788a"/><stop offset="1" stop-color="#f3b27a"/>
  </linearGradient>
  <linearGradient id="champ" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2d3b2c"/><stop offset="1" stop-color="#1a2419"/>
  </linearGradient>
  <linearGradient id="route" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4a4b55"/><stop offset="1" stop-color="#25262d"/>
  </linearGradient>
  <linearGradient id="mat" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#6c727c"/><stop offset="0.45" stop-color="#c7ccd3"/><stop offset="1" stop-color="#5a6069"/>
  </linearGradient>
  <linearGradient id="cabF" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8d939c"/><stop offset="0.6" stop-color="#d3d7dd"/><stop offset="1" stop-color="#b9bec6"/>
  </linearGradient>
  <linearGradient id="cabC" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#5f656e"/><stop offset="1" stop-color="#7b818a"/>
  </linearGradient>
  <linearGradient id="vitre" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2a3448"/><stop offset="1" stop-color="#0b0f18"/>
  </linearGradient>
  <radialGradient id="soleil" cx="0.3" cy="0.56" r="0.35">
    <stop offset="0" stop-color="#ffd9a0" stop-opacity="0.75"/><stop offset="1" stop-color="#ffd9a0" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#ciel)"/>
<rect width="{W}" height="{H}" fill="url(#soleil)"/>
{arbres}
<rect y="900" width="{W}" height="{H - 900}" fill="url(#champ)"/>
<polygon points="1150,900 1210,900 2350,{H} 10,{H}" fill="url(#route)"/>
<polygon points="1150,900 1157,900 120,{H} 60,{H}" fill="#d9d4c4" opacity="0.7"/>
<polygon points="1203,900 1210,900 2300,{H} 2240,{H}" fill="#d9d4c4" opacity="0.7"/>
{tirets}
<!-- accotement et socle -->
<ellipse cx="1820" cy="1210" rx="120" ry="22" fill="#11160f" opacity="0.7"/>
<rect x="1760" y="1170" width="120" height="40" rx="4" fill="#8b8e92"/>
<rect x="1760" y="1170" width="120" height="10" fill="#a9acb0"/>
<!-- mât -->
<rect x="1797" y="470" width="46" height="705" fill="url(#mat)"/>
<!-- cabine -->
<polygon points="1700,220 1940,220 1940,520 1700,520" fill="url(#cabF)"/>
<polygon points="1940,220 1990,250 1990,540 1940,520" fill="url(#cabC)"/>
<polygon points="1700,220 1940,220 1990,250 1750,250" fill="#e2e5ea"/>
<rect x="1700" y="512" width="240" height="14" fill="#6f747c"/>
<!-- vitres des capteurs -->
<rect x="1730" y="268" width="180" height="96" rx="10" fill="url(#vitre)"/>
<rect x="1742" y="280" width="64" height="20" rx="6" fill="#ffffff" opacity="0.15"/>
<rect x="1730" y="384" width="82" height="82" rx="10" fill="url(#vitre)"/>
<rect x="1828" y="384" width="82" height="82" rx="10" fill="url(#vitre)"/>
<circle cx="1771" cy="425" r="20" fill="#05070c"/><circle cx="1765" cy="419" r="6" fill="#9fb4d8" opacity="0.6"/>
<circle cx="1869" cy="425" r="20" fill="#05070c"/><circle cx="1863" cy="419" r="6" fill="#9fb4d8" opacity="0.6"/>
<!-- bandes réfléchissantes -->
<rect x="1700" y="486" width="240" height="12" fill="#f2f2f2"/>
<rect x="1940" y="503" width="50" height="12" fill="#cfd2d6" transform="skewY(22) translate(0,-784)"/>
</svg>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
    pg.screenshot(path=sys.argv[1], type='jpeg', quality=92)
    b.close()
print('ok', sys.argv[1])
