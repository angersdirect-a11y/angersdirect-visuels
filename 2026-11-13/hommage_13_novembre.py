"""Visuel hommage 13-Novembre (post 1080x1350 et story 1080x1920), fond bleu nuit uni, sobre, sans photo.
Usage (depuis la racine du dépôt) : python3 2026-11-13/hommage_13_novembre.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'outils'))
from visuel import polices, ICI
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).resolve().parent
LIEUX = ['Stade de France', 'Le Carillon', 'Le Petit Cambodge', 'La Bonne Bière', 'Le Comptoir Voltaire',
         'La Belle Équipe', 'Le Bataclan']


def page(H):
    st = H == 1920
    top = 250 if st else 90
    sep = '<span style="color:#5E6B85;margin-left:16px">·</span>'
    lieux = ' '.join(f'<span style="white-space:nowrap;margin:0 8px">{l}{sep if i < len(LIEUX) - 1 else ""}</span>' for i, l in enumerate(LIEUX))
    return f'''<div style="width:1080px;height:{H}px;position:relative;overflow:hidden;font-family:Barlow;color:#FFFFFF;
background:radial-gradient(ellipse 900px 600px at 50% {top + 380}px,rgba(120,150,210,.22) 0%,rgba(10,20,40,0) 70%),#0B1628">
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:{top}px;width:150px;opacity:.9">
<div style="position:absolute;right:72px;top:{top + 18}px;font-family:'Barlow Condensed';font-weight:600;font-size:30px;letter-spacing:4px;color:#AEB9CF">HOMMAGE</div>
<div style="position:absolute;left:72px;right:72px;top:{top + 200 + (60 if st else 0)}px;text-align:center">
 <div style="font-family:'Barlow Condensed';font-weight:600;font-size:46px;letter-spacing:10px;color:#AEB9CF">13 NOVEMBRE 2015</div>
 <div style="display:flex;justify-content:center;gap:0;margin:34px auto 0;width:240px;height:6px">
  <div style="flex:1;background:#2A5BD7"></div><div style="flex:1;background:#FFFFFF"></div><div style="flex:1;background:#E0313B"></div></div>
 <div style="font-family:'Barlow Condensed';font-weight:800;font-size:{300 if st else 260}px;line-height:1;margin-top:{50 if st else 30}px">132</div>
 <div style="font-family:'Barlow Condensed';font-weight:600;font-size:44px;letter-spacing:3px;color:#DDE3EE;margin-top:6px">VICTIMES À PARIS ET À SAINT-DENIS</div>
 <div style="font-family:'Barlow Condensed';font-weight:700;font-size:{88 if st else 80}px;line-height:1.05;margin-top:{90 if st else 60}px">Onze ans après,<br>nous n'oublions pas.</div>
 <div style="font-weight:400;font-size:30px;line-height:1.6;color:#AEB9CF;margin:{80 if st else 54}px auto 0;max-width:900px">{lieux}</div>
</div>
<div style="position:absolute;left:72px;top:{1620 if st else 1250}px;font-weight:500;font-size:28px;letter-spacing:1px;color:#7F8BA3">angersdirect.fr</div>
</div>'''


def paysage():
    return f'''<div style="width:1200px;height:675px;position:relative;overflow:hidden;font-family:Barlow;color:#FFFFFF;
background:radial-gradient(ellipse 700px 400px at 50% 300px,rgba(120,150,210,.22) 0%,rgba(10,20,40,0) 70%),#0B1628;text-align:center">
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:56px;top:48px;width:120px;opacity:.9">
<div style="position:absolute;right:56px;top:60px;font-family:'Barlow Condensed';font-weight:600;font-size:24px;letter-spacing:4px;color:#AEB9CF">HOMMAGE</div>
<div style="position:absolute;left:0;right:0;top:150px">
 <div style="font-family:'Barlow Condensed';font-weight:600;font-size:34px;letter-spacing:8px;color:#AEB9CF">13 NOVEMBRE 2015</div>
 <div style="display:flex;margin:22px auto 0;width:180px;height:5px"><div style="flex:1;background:#2A5BD7"></div><div style="flex:1;background:#FFFFFF"></div><div style="flex:1;background:#E0313B"></div></div>
 <div style="font-family:'Barlow Condensed';font-weight:800;font-size:170px;line-height:1;margin-top:18px">132</div>
 <div style="font-family:'Barlow Condensed';font-weight:600;font-size:32px;letter-spacing:3px;color:#DDE3EE">VICTIMES À PARIS ET À SAINT-DENIS</div>
 <div style="font-family:'Barlow Condensed';font-weight:700;font-size:54px;margin-top:30px">Onze ans après, nous n'oublions pas.</div>
</div></div>'''


with sync_playwright() as p:
    b = p.chromium.launch()
    for nom, H in [('hommage-13-novembre-post', 1350), ('hommage-13-novembre-story', 1920)]:
        tmp = D / f'{nom}.html'
        tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{page(H)}</body></html>")
        pg = b.new_page(viewport={'width': 1080, 'height': H})
        pg.goto(f'file://{tmp}'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(D / f'{nom}.png')); tmp.unlink(); print('ok', nom)
    tmp = D / 'hommage-13-novembre-x.html'
    tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{paysage()}</body></html>")
    pg = b.new_page(viewport={'width': 1200, 'height': 675})
    pg.goto(f'file://{tmp}'); pg.wait_for_timeout(300)
    pg.screenshot(path=str(D / 'hommage-13-novembre-x.png')); tmp.unlink(); print('ok x')
    b.close()
    from PIL import Image
    Image.open(D / 'hommage-13-novembre-story.png').convert('RGB').save(D / 'hommage-13-novembre-story.jpg', quality=92)
