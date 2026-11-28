import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
"""Illustration originale (aucun droit tiers) : trois verres de dégustation (rouge, rosé, blanc) sur une table,
grappe de raisin et feuilles de vigne, lumières chaudes floues en fond. Pour les salons et foires aux vins.
Usage : python3 outils/vin_degustation.py sortie.jpg"""
import random, sys
from playwright.sync_api import sync_playwright

W, H = 2400, 1600
random.seed(11)

bokeh = ''.join(
    f'<circle cx="{random.randint(0, W)}" cy="{random.randint(0, 900)}" r="{random.randint(30, 110)}" '
    f'fill="{random.choice(["#F5B95A", "#E88A3C", "#FFD98A", "#C9643A"])}" opacity="{random.uniform(0.10, 0.35):.2f}"/>'
    for _ in range(46))


def verre(cx, base_y, vin, niveau, echelle=1.0):
    s = echelle
    h_coupe, l_coupe, h_pied = 430 * s, 300 * s, 330 * s
    top = base_y - h_pied - h_coupe
    x0, x1 = cx - l_coupe / 2, cx + l_coupe / 2
    coupe = (f'M{x0},{top} C{x0-20*s},{top+h_coupe*0.55} {cx-l_coupe*0.42},{top+h_coupe} {cx},{top+h_coupe} '
             f'C{cx+l_coupe*0.42},{top+h_coupe} {x1+20*s},{top+h_coupe*0.55} {x1},{top} Z')
    ny = top + h_coupe * (1 - niveau)
    clip = f'clip{int(cx)}'
    return f'''
<clipPath id="{clip}"><path d="{coupe}"/></clipPath>
<ellipse cx="{cx}" cy="{base_y+6*s}" rx="{170*s}" ry="{26*s}" fill="#000" opacity="0.35"/>
<rect x="{x0-40*s}" y="{ny}" width="{l_coupe+80*s}" height="{h_coupe}" fill="url(#{vin})" clip-path="url(#{clip})"/>
<ellipse cx="{cx}" cy="{ny}" rx="{l_coupe*0.47*(0.75+0.25*niveau)}" ry="{16*s}" fill="#fff" opacity="0.18" clip-path="url(#{clip})"/>
<path d="{coupe}" fill="#ffffff" fill-opacity="0.06" stroke="#F4EBDD" stroke-opacity="0.75" stroke-width="{5*s}"/>
<path d="M{x0+28*s},{top+40*s} C{x0+10*s},{top+h_coupe*0.5} {cx-l_coupe*0.3},{top+h_coupe*0.88} {cx-l_coupe*0.12},{top+h_coupe*0.95}"
      fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="{10*s}" stroke-linecap="round"/>
<rect x="{cx-7*s}" y="{top+h_coupe-4*s}" width="{14*s}" height="{h_pied}" rx="{6*s}" fill="#F4EBDD" opacity="0.8"/>
<ellipse cx="{cx}" cy="{base_y}" rx="{150*s}" ry="{22*s}" fill="#F4EBDD" opacity="0.75"/>
<ellipse cx="{cx}" cy="{base_y-4*s}" rx="{120*s}" ry="{12*s}" fill="#fff" opacity="0.35"/>'''


def grappe(cx, cy):
    out = ''
    rangs = [(0, 7), (1, 6), (2, 6), (3, 5), (4, 4), (5, 3), (6, 2), (7, 1)]
    for r, n in rangs:
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * 62 + random.uniform(-6, 6)
            y = cy + r * 52 + random.uniform(-5, 5)
            out += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="36" fill="url(#raisin)"/>'
                    f'<circle cx="{x-11:.0f}" cy="{y-13:.0f}" r="9" fill="#fff" opacity="0.35"/>')
    return out


def feuille(cx, cy, rot, sc):
    return (f'<g transform="translate({cx},{cy}) rotate({rot}) scale({sc})">'
            '<path d="M0,0 C-60,-40 -150,-30 -170,-110 C-120,-100 -110,-150 -90,-200 C-60,-160 -40,-190 0,-260 '
            'C40,-190 60,-160 90,-200 C110,-150 120,-100 170,-110 C150,-30 60,-40 0,0 Z" fill="url(#feuille)"/>'
            '<path d="M0,0 L0,-230 M0,-80 L-120,-120 M0,-80 L120,-120 M0,-150 L-70,-185 M0,-150 L70,-185" '
            'stroke="#2E4A1E" stroke-width="6" fill="none" opacity="0.55"/></g>')


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <radialGradient id="fond" cx="50%" cy="35%" r="80%"><stop offset="0" stop-color="#5A2E25"/><stop offset="0.55" stop-color="#2A1514"/><stop offset="1" stop-color="#120A0B"/></radialGradient>
 <linearGradient id="table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6B4126"/><stop offset="1" stop-color="#2E1A10"/></linearGradient>
 <linearGradient id="rouge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9E1B32"/><stop offset="1" stop-color="#4A0A18"/></linearGradient>
 <linearGradient id="rose" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7A08C"/><stop offset="1" stop-color="#D9605A"/></linearGradient>
 <linearGradient id="blanc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6E7A1"/><stop offset="1" stop-color="#D8B54C"/></linearGradient>
 <radialGradient id="raisin" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#8E5BB5"/><stop offset="1" stop-color="#3A1650"/></radialGradient>
 <linearGradient id="feuille" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7DAA3E"/><stop offset="1" stop-color="#3F6B22"/></linearGradient>
 <filter id="flou"><feGaussianBlur stdDeviation="38"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#fond)"/>
<g filter="url(#flou)">{bokeh}</g>
<rect x="0" y="1180" width="{W}" height="{H-1180}" fill="url(#table)"/>
<rect x="0" y="1180" width="{W}" height="8" fill="#A06A3E" opacity="0.6"/>
{feuille(1880, 1185, -28, 1.25)}{feuille(2090, 1200, 18, 1.0)}
{grappe(1980, 870)}
<path d="M1980,870 C1975,820 2000,790 2030,770" stroke="#4E3420" stroke-width="16" fill="none" stroke-linecap="round"/>
{verre(640, 1235, "rouge", 0.42, 1.08)}
{verre(1080, 1215, "rose", 0.38, 0.98)}
{verre(1480, 1225, "blanc", 0.40, 1.02)}
</svg>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': W, 'height': H})
    pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
    pg.screenshot(path=sys.argv[1], type='jpeg', quality=90)
    __import__('auteur').signer(sys.argv[1])
    b.close()
print('ok', sys.argv[1])
