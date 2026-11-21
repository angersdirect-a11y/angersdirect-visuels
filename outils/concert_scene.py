"""Illustration originale (aucun droit tiers) : scène de concert vide, projecteurs colorés, micro sur pied.
Usage : python3 outils/concert_scene.py sortie.jpg"""
import sys, random
from playwright.sync_api import sync_playwright
random.seed(7)
W, H = 1600, 1100
beams = ''
for x, col, ang in [(250, '#ff3fa4', 18), (560, '#ffb13b', 6), (1040, '#38c6ff', -6), (1350, '#b06bff', -18), (800, '#ffffff', 0)]:
    beams += f'<polygon points="{x-18},0 {x+18},0 {x+260+ang*10},{H-260} {x-260+ang*10},{H-260}" fill="url(#b{col[1:]})" opacity=".55"/>'
grads = ''.join(f'<linearGradient id="b{c[1:]}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".95"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>' for c in ['#ff3fa4','#ffb13b','#38c6ff','#b06bff','#ffffff'])
dust = ''.join(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,H-300)}" r="{random.uniform(1,3):.1f}" fill="#fff" opacity="{random.uniform(.1,.5):.2f}"/>' for _ in range(160))
lamps = ''.join(f'<rect x="{x-30}" y="8" width="60" height="34" rx="6" fill="#1b1b24"/><circle cx="{x}" cy="40" r="16" fill="{c}"/>' for x, c in [(250,'#ff7cc2'),(560,'#ffd08a'),(800,'#ffffff'),(1040,'#8fdcff'),(1350,'#d1a8ff')])
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs>{grads}
<radialGradient id="sol" cx=".5" cy=".2" r=".7"><stop offset="0" stop-color="#3a2a55"/><stop offset="1" stop-color="#0b0b14"/></radialGradient>
<linearGradient id="fond" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120c22"/><stop offset="1" stop-color="#1e1433"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#fond)"/>
<rect y="{H-300}" width="{W}" height="300" fill="url(#sol)"/>
<rect x="0" y="0" width="{W}" height="56" fill="#0d0d14"/>{lamps}
{beams}{dust}
<g fill="#07070c">
<rect x="160" y="{H-520}" width="230" height="260" rx="10"/><rect x="1210" y="{H-520}" width="230" height="260" rx="10"/>
<rect x="420" y="{H-420}" width="170" height="160" rx="8"/>
<rect x="1040" y="{H-430}" width="150" height="170" rx="8"/>
<rect x="796" y="{H-690}" width="8" height="430"/><rect x="740" y="{H-265}" width="120" height="10" rx="5"/>
<rect x="790" y="{H-720}" width="20" height="52" rx="10"/>
<ellipse cx="1110" cy="{H-470}" rx="70" ry="22"/><rect x="1106" y="{H-470}" width="8" height="40"/>
</g>
<g fill="#26203a"><circle cx="275" cy="{H-410}" r="62"/><circle cx="1325" cy="{H-410}" r="62"/></g>
<g fill="#07070c"><circle cx="275" cy="{H-410}" r="34"/><circle cx="1325" cy="{H-410}" r="34"/></g>
</svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f'<body style="margin:0">{svg}</body>'); pg.screenshot(path=sys.argv[1], type='jpeg', quality=92); b.close()
