"""Illustration originale (aucun droit tiers) : colis d'aide alimentaire (carton, pain, fruits, lait) sous une lumière chaude.
Sortie : photos/colis-alimentaire-illustration.jpg (1600x2000). Pour les sujets pauvreté, précarité, aide alimentaire."""
import pathlib
from playwright.sync_api import sync_playwright
ICI = pathlib.Path(__file__).resolve().parent
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2000" viewBox="0 0 1600 2000">
<defs>
<radialGradient id="lum" cx="50%" cy="38%" r="70%"><stop offset="0" stop-color="#6a5440"/><stop offset=".5" stop-color="#2c2a33"/><stop offset="1" stop-color="#121722"/></radialGradient>
<linearGradient id="table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3f2a"/><stop offset="1" stop-color="#24180f"/></linearGradient>
<linearGradient id="carton" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b9864f"/><stop offset=".6" stop-color="#c99a62"/><stop offset="1" stop-color="#9c6d3d"/></linearGradient>
<linearGradient id="pain" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e7b46a"/><stop offset="1" stop-color="#a8652a"/></linearGradient>
<radialGradient id="pomme" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#ff7a63"/><stop offset="1" stop-color="#8f1d16"/></radialGradient>
<radialGradient id="orange" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#ffc06a"/><stop offset="1" stop-color="#c2600f"/></radialGradient>
<filter id="flou"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<rect width="1600" height="2000" fill="url(#lum)"/>
<rect y="1380" width="1600" height="620" fill="url(#table)"/>
<ellipse cx="800" cy="1420" rx="640" ry="70" fill="#000" opacity=".45" filter="url(#flou)"/>
<!-- baguettes -->
<g transform="rotate(-14 640 700)"><rect x="560" y="420" width="110" height="720" rx="55" fill="url(#pain)"/>
<g stroke="#8a4f1e" stroke-width="10" stroke-linecap="round" opacity=".7"><line x1="585" y1="520" x2="640" y2="490"/><line x1="585" y1="640" x2="640" y2="610"/><line x1="585" y1="760" x2="640" y2="730"/></g></g>
<g transform="rotate(10 900 700)"><rect x="840" y="470" width="100" height="660" rx="50" fill="url(#pain)"/>
<g stroke="#8a4f1e" stroke-width="10" stroke-linecap="round" opacity=".7"><line x1="862" y1="560" x2="918" y2="532"/><line x1="862" y1="680" x2="918" y2="652"/></g></g>
<!-- brique de lait -->
<g><rect x="1010" y="640" width="190" height="420" fill="#eef1f5"/><polygon points="1010,640 1105,560 1200,640" fill="#d8dde5"/><rect x="1010" y="760" width="190" height="120" fill="#3a7bd5"/></g>
<!-- poireau -->
<g transform="rotate(-30 430 800)"><rect x="400" y="560" width="70" height="520" rx="30" fill="#e8efd8"/><path d="M400 600 C380 450 360 380 330 320 L380 330 C410 420 430 500 440 590Z" fill="#4f8a3a"/><path d="M470 600 C500 460 520 400 560 340 L510 340 C480 430 465 500 450 590Z" fill="#3f7a2e"/></g>
<!-- carton -->
<polygon points="300,900 1300,900 1240,1420 360,1420" fill="url(#carton)"/>
<polygon points="300,900 1300,900 1380,820 230,820" fill="#d9ad74" opacity=".9"/>
<polygon points="300,900 230,820 160,1010 300,960" fill="#a9773f"/>
<polygon points="1300,900 1380,820 1450,1010 1300,960" fill="#a9773f"/>
<path d="M800 1080 C760 1020 680 1040 690 1110 C700 1170 800 1230 800 1230 C800 1230 900 1170 910 1110 C920 1040 840 1020 800 1080Z" fill="#c43b33" opacity=".85"/>
<!-- fruits devant -->
<circle cx="520" cy="1360" r="95" fill="url(#pomme)"/><path d="M520 1268 q10 -40 40 -50" stroke="#4a2c12" stroke-width="10" fill="none"/>
<circle cx="700" cy="1395" r="80" fill="url(#orange)"/>
<circle cx="1080" cy="1370" r="90" fill="url(#pomme)"/><path d="M1080 1282 q8 -36 36 -46" stroke="#4a2c12" stroke-width="10" fill="none"/>
<circle cx="1240" cy="1410" r="70" fill="url(#orange)"/>
</svg>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1600, 'height': 2000})
    pg.set_content(f'<html><body style="margin:0">{SVG}</body></html>')
    pg.screenshot(path=str(ICI / 'photos/colis-alimentaire-illustration.jpg'), type='jpeg', quality=90)
    b.close()
print('ok')
