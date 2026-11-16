"""Illustration originale (aucun droit tiers) : vieux ordinateurs portables, écran, téléphones et câbles posés sur une table, sous une lumière chaude.
Sortie : photos/numerique-recup-illustration.jpg (1600x2000). Pour les sujets collecte, recyclage, réemploi du matériel numérique."""
import pathlib
from playwright.sync_api import sync_playwright
ICI = pathlib.Path(__file__).resolve().parent


def tel(x, y, r, ecran='#1b2a3c'):
    return f'''<g transform="translate({x} {y}) rotate({r})"><rect x="-70" y="-140" width="140" height="280" rx="22" fill="#2a2f38"/>
<rect x="-60" y="-122" width="120" height="236" rx="10" fill="{ecran}"/><rect x="-60" y="-122" width="120" height="70" rx="10" fill="#ffffff" opacity=".06"/>
<circle cx="0" cy="128" r="6" fill="#4a505b"/></g>'''


SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2000" viewBox="0 0 1600 2000">
<defs>
<radialGradient id="lum" cx="50%" cy="30%" r="75%"><stop offset="0" stop-color="#4d6a78"/><stop offset=".5" stop-color="#22323f"/><stop offset="1" stop-color="#0f1822"/></radialGradient>
<linearGradient id="table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4a31"/><stop offset="1" stop-color="#2a1b10"/></linearGradient>
<linearGradient id="alu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c9ced6"/><stop offset=".5" stop-color="#9aa1ab"/><stop offset="1" stop-color="#6c727c"/></linearGradient>
<linearGradient id="noir" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3c424c"/><stop offset="1" stop-color="#1c2027"/></linearGradient>
<linearGradient id="ecran" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2d6f8f"/><stop offset=".6" stop-color="#173a52"/><stop offset="1" stop-color="#0d2233"/></linearGradient>
<linearGradient id="verte" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2fd3ab"/><stop offset="1" stop-color="#0f8069"/></linearGradient>
<filter id="flou"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="1600" height="2000" fill="url(#lum)"/>
<rect y="1300" width="1600" height="700" fill="url(#table)"/>
<g stroke="#000" stroke-opacity=".12" stroke-width="4"><line x1="0" y1="1480" x2="1600" y2="1440"/><line x1="0" y1="1700" x2="1600" y2="1660"/></g>
<ellipse cx="800" cy="1340" rx="720" ry="80" fill="#000" opacity=".45" filter="url(#flou)"/>
<!-- vieil écran au fond -->
<rect x="860" y="430" width="560" height="400" rx="18" fill="url(#noir)"/><rect x="890" y="458" width="500" height="340" rx="6" fill="url(#ecran)"/>
<polygon points="1100,830 1180,830 1210,1000 1070,1000" fill="#2a2f38"/><rect x="1000" y="1000" width="280" height="34" rx="10" fill="#2a2f38"/>
<!-- tour d'ordinateur -->
<rect x="170" y="560" width="300" height="760" rx="16" fill="url(#noir)"/><rect x="200" y="600" width="240" height="60" rx="6" fill="#4a505b"/>
<rect x="200" y="690" width="240" height="22" rx="4" fill="#4a505b"/><circle cx="320" cy="800" r="26" fill="#4a505b"/><circle cx="320" cy="800" r="10" fill="#2fd3ab"/>
<g stroke="#2a2f38" stroke-width="6">{''.join(f'<line x1="210" y1="{y}" x2="430" y2="{y}"/>' for y in range(900, 1260, 34))}</g>
<!-- pile de portables -->
<rect x="420" y="1180" width="760" height="46" rx="12" fill="url(#noir)"/>
<rect x="450" y="1120" width="720" height="46" rx="12" fill="url(#alu)"/>
<rect x="480" y="1062" width="660" height="44" rx="12" fill="#5b616b"/>
<!-- portable ouvert sur la pile -->
<polygon points="560,1062 1060,1062 1110,1040 510,1040" fill="#aab0b9"/>
<polygon points="540,640 1080,640 1060,1040 560,1040" fill="url(#alu)"/>
<polygon points="566,668 1052,668 1036,1012 582,1012" fill="url(#ecran)"/>
<polygon points="566,668 1052,668 1040,760 574,820" fill="#ffffff" opacity=".07"/>
<!-- câbles -->
<path d="M300 1320 C380 1460 560 1420 640 1520 C720 1620 940 1560 1010 1660" stroke="#1c2027" stroke-width="16" fill="none" stroke-linecap="round"/>
<path d="M1260 1330 C1200 1450 1340 1520 1250 1620 C1180 1700 1060 1720 980 1780" stroke="#e9ecef" stroke-width="12" fill="none" stroke-linecap="round"/>
<rect x="990" y="1640" width="60" height="40" rx="6" fill="#1c2027" transform="rotate(20 1020 1660)"/>
<!-- téléphones et batterie au premier plan -->
{tel(420, 1640, -18)}{tel(640, 1700, 12, '#173a52')}{tel(1330, 1600, 24)}
<g transform="translate(860 1560) rotate(-8)"><rect x="-110" y="-60" width="220" height="120" rx="16" fill="#2a2f38"/><rect x="-90" y="-30" width="120" height="60" rx="6" fill="url(#verte)"/>
<rect x="110" y="-20" width="16" height="40" rx="4" fill="#2a2f38"/></g>
<!-- flèches de réemploi discrètes sur l'écran du fond -->
<g transform="translate(1140 628)" fill="none" stroke="#6fe3c6" stroke-width="14" stroke-linecap="round" opacity=".85">
<path d="M-70 30 A80 80 0 0 1 40 -66"/><path d="M78 10 A80 80 0 0 1 -30 76"/></g>
<g fill="#6fe3c6" opacity=".85"><polygon points="1186,548 1196,586 1162,578"/><polygon points="1094,708 1084,670 1118,678"/></g>
</svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1600, 'height': 2000})
    pg.set_content(f'<html><body style="margin:0">{SVG}</body></html>')
    pg.screenshot(path=str(ICI / 'photos/numerique-recup-illustration.jpg'), type='jpeg', quality=90)
    b.close()
print('ok')
