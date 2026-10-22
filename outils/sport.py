"""Visuels sport Angers Direct : score final, classement, calendrier, jour de match (story et paysage).

Usage : python3 outils/sport.py fiche.json sortie.png
Polices : cd outils && npm i --silent (une fois par session).
Logos : outils/logos/<slug>.png (PNG transparent). Sans fichier, un badge avec les initiales est affiché.

Fiches (exemples complets dans outils/exemples/) :
  score       : journee, dom{nom,logo}, ext{nom,logo}, score[a,b], buteurs_dom[], buteurs_ext[], stats[{label,dom,ext,vdom,vext}] (facultatif), pied
  classement  : titre, sous_titre, lignes[{rang,nom,logo,diff,j,pts,surligne}], source
  calendrier  : mois ("d'octobre"), matchs[{date,adversaire,logo,domicile(bool),lieu,heure}], pied
  jdm_story / jdm_paysage : journee, dom{nom,logo}, ext{nom,logo}, date, heure, stade, diffusion (facultatif)
Les valeurs non vérifiées ne doivent jamais être inventées : laisser une liste vide plutôt.
"""
import html, json, pathlib, sys
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
FONTS = ICI / 'node_modules/@fontsource'
BLEU = '#5AB6F1'
BC = "font-family:'Barlow Condensed'"


def e(t):
    return html.escape(str(t))


def polices():
    out = ''
    for fam, d, ws in [('Barlow', 'barlow', [400, 500, 600]), ('Barlow Condensed', 'barlow-condensed', [600, 700])]:
        for w in ws:
            out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{FONTS}/{d}/files/{d}-latin-{w}-normal.woff2') format('woff2');}}\n"
    return out


ALIAS = {'angers': 'angers-sco', 'sco': 'angers-sco', 'auxerre': 'aj-auxerre', 'brest': 'stade-brestois',
         'havre': 'le-havre-ac', 'le mans': 'le-mans-fc', 'lens': 'rc-lens', 'lille': 'losc-lille', 'losc': 'losc-lille',
         'lorient': 'fc-lorient', 'lyon': 'olympique-lyonnais', 'lyonnais': 'olympique-lyonnais',
         'marseille': 'olympique-de-marseille', 'monaco': 'as-monaco', 'nice': 'ogc-nice', 'paris fc': 'paris-fc',
         'saint-germain': 'paris-saint-germain', 'psg': 'paris-saint-germain', 'strasbourg': 'rc-strasbourg',
         'toulouse': 'toulouse-fc', 'troyes': 'estac-troyes', 'estac': 'estac-troyes', 'rennes': 'stade-rennais',
         'rennais': 'stade-rennais'}


def trouver_slug(nom):
    n = nom.lower()
    for cle in sorted(ALIAS, key=len, reverse=True):
        if cle in n:
            return ALIAS[cle]
    return ''


def logo(slug, nom, taille):
    slug = slug or trouver_slug(nom)
    f = ICI / 'logos' / f'{slug}.png'
    if slug and f.exists():
        return f'<img src="file://{f}" style="width:{taille}px;height:{taille}px;object-fit:contain">'
    init = ''.join(w[0] for w in nom.replace('-', ' ').split() if w[0].isalpha())[:3].upper()
    return f'<div style="{BC};font-weight:700;font-size:{int(taille*0.42)}px;color:#3B4656">{e(init)}</div>'


def rond(slug, nom, d):
    return (f'<div style="width:{d}px;height:{d}px;border-radius:50%;background:#FFFFFF;display:flex;align-items:center;justify-content:center;box-sizing:border-box;'
            f'border:{max(4, d//40)}px solid #FFFFFF;box-shadow:inset 0 0 0 {max(6, d//30)}px #1F2B3B">{logo(slug, nom, int(d*0.62))}</div>')


def fond(w, h, photo=True):
    p = ICI / 'photos/stade-nuit.jpg'
    img = f'<img src="file://{p}" style="position:absolute;left:-60px;top:-60px;width:{w+120}px;height:{h+120}px;object-fit:cover;filter:blur(26px) grayscale(0.6);opacity:0.45">' if photo else ''
    return (f'<div style="position:absolute;inset:0;background:#0F1B2D"></div>{img}'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,27,45,0.35) 0%,rgba(15,27,45,0.55) 55%,rgba(13,24,41,0.95) 100%)"></div>')


def entete(w, tag, rouge=False, top=70):
    bg = '#E53935' if rouge else '#FFFFFF'
    col = '#FFFFFF' if rouge else '#0F1B2D'
    return (f'<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:{top}px;width:196px">'
            f'<div style="position:absolute;right:72px;top:{top+8}px;padding:6px 26px;background:{bg};transform:skewX(-12deg)">'
            f'<div style="transform:skewX(12deg);{BC};font-weight:600;font-size:38px;letter-spacing:2px;color:{col}">{e(tag)}</div></div>')


def score(f):
    a, b = f['score']
    def buts(l, align):
        return ''.join(f'<div style="text-align:{align}">{e(x)}</div>' for x in l)
    stats = ''
    y = 940
    for s in f.get('stats', []):
        tot = (s['vdom'] + s['vext']) or 1
        wl, wr = int(460 * s['vdom'] / tot), int(460 * s['vext'] / tot)
        stats += f'''<div style="position:absolute;left:70px;right:70px;top:{y}px;display:flex;justify-content:space-between;align-items:center">
<div style="{BC};font-weight:600;font-size:42px">{e(s['dom'])}</div><div style="font-size:28px;letter-spacing:3px;color:{BLEU}">{e(s['label'])}</div><div style="{BC};font-weight:600;font-size:42px">{e(s['ext'])}</div></div>
<div style="position:absolute;left:70px;top:{y+56}px;width:460px;height:9px;background:#2A3646"></div><div style="position:absolute;left:{530-wl}px;top:{y+56}px;width:{wl}px;height:9px;background:#FFFFFF"></div>
<div style="position:absolute;left:550px;top:{y+56}px;width:460px;height:9px;background:#2A3646"></div><div style="position:absolute;left:550px;top:{y+56}px;width:{wr}px;height:9px;background:#D3D5D9"></div>'''
        y += 92
    return f'''<div style="width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Barlow;color:#FFFFFF">{fond(1080,1350)}{entete(1080,'SCORE FINAL',True)}
<div style="position:absolute;left:0;right:0;top:272px;text-align:center;font-size:34px;letter-spacing:4px;color:{BLEU}">LIGUE 1 · {e(f['journee']).upper()}</div>
<div style="position:absolute;left:0;right:0;top:346px;height:282px;background:rgba(255,255,255,0.10);border-top:2px solid rgba(255,255,255,0.4);border-bottom:2px solid rgba(255,255,255,0.4)"></div>
<div style="position:absolute;left:44px;top:369px">{rond(f['dom'].get('logo'),f['dom']['nom'],236)}</div>
<div style="position:absolute;right:44px;top:369px">{rond(f['ext'].get('logo'),f['ext']['nom'],236)}</div>
<div style="position:absolute;left:330px;top:366px;width:420px;height:240px;background:#111C2C;transform:skewX(-8deg);display:flex;align-items:center;justify-content:center"><div style="transform:skewX(8deg);{BC};font-weight:700;font-size:200px;line-height:1">{a} - {b}</div></div>
<div style="position:absolute;left:56px;top:652px;{BC};font-weight:600;font-size:46px">{e(f['dom']['nom'])}</div>
<div style="position:absolute;right:75px;top:652px;{BC};font-weight:600;font-size:46px">{e(f['ext']['nom'])}</div>
<div style="position:absolute;left:70px;right:70px;top:746px;height:2px;background:rgba(255,255,255,0.25)"></div>
<div style="position:absolute;left:90px;top:782px;font-size:32px;line-height:1.6">{buts(f.get('buteurs_dom',[]),'left')}</div>
<div style="position:absolute;right:90px;top:782px;font-size:32px;line-height:1.6">{buts(f.get('buteurs_ext',[]),'right')}</div>
{stats}
<div style="position:absolute;left:0;right:0;top:1240px;text-align:center;font-size:32px;color:{BLEU}">{e(f.get('pied','Le résumé et les réactions sur angersdirect.fr'))}</div></div>'''


def classement(f):
    rows = ''
    y = 370
    for i, l in enumerate(f['lignes']):
        hi = l.get('surligne')
        bg = '#E6E9EE' if hi else ('rgba(255,255,255,0.07)' if i % 2 == 0 else 'rgba(255,255,255,0.03)')
        col = '#0F1B2D' if hi else '#FFFFFF'
        rows += f'''<div style="position:absolute;left:56px;right:56px;top:{y}px;height:46px;background:{bg};border-radius:{10 if hi else 0}px;color:{col};{BC};font-weight:600;font-size:28px">
<div style="position:absolute;left:24px;width:40px;top:6px;text-align:center">{l['rang']}</div>
<div style="position:absolute;left:86px;top:5px;width:36px;height:36px;border-radius:50%;background:#FFFFFF;display:flex;align-items:center;justify-content:center">{logo(l.get('logo'),l['nom'],28)}</div>
<div style="position:absolute;left:149px;top:6px">{e(l['nom'])}</div>
<div style="position:absolute;right:264px;top:6px">{e(l['diff'])}</div>
<div style="position:absolute;right:150px;width:60px;top:6px;text-align:center">{l['j']}</div>
<div style="position:absolute;right:30px;width:60px;top:6px;text-align:center">{l['pts']}</div></div>'''
        y += 49.5
    return f'''<div style="width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Barlow;color:#FFFFFF">
<div style="position:absolute;inset:0;background:#0F1B2D"></div><div style="position:absolute;inset:0;background:rgba(255,255,255,0.05);clip-path:polygon(100% 260px,100% 100%,850px 100%)"></div>
{entete(1080,'CLASSEMENT')}
<div style="position:absolute;left:70px;top:196px;{BC};font-weight:700;font-size:96px;line-height:1">{e(f.get('titre','Ligue 1'))}</div>
<div style="position:absolute;left:72px;top:292px;font-size:32px;color:{BLEU}">{e(f['sous_titre'])}</div>
<div style="position:absolute;right:320px;top:336px;font-size:22px;letter-spacing:2px;color:{BLEU}">DIFF.</div>
<div style="position:absolute;right:206px;width:60px;top:336px;text-align:center;font-size:22px;color:{BLEU}">J</div>
<div style="position:absolute;right:86px;width:60px;top:336px;text-align:center;font-size:22px;letter-spacing:2px;color:{BLEU}">PTS</div>
{rows}
<div style="position:absolute;right:70px;top:1290px;font-size:22px;color:#A7B0BD">{e(f.get('source','Source : ligue officielle · angersdirect.fr'))}</div></div>'''


def calendrier(f):
    rows = ''
    y = 440
    for m in f['matchs'][:5]:
        pre = 'vs' if m['domicile'] else 'à'
        sous = ('Domicile · ' if m['domicile'] else 'Extérieur · ') + m['lieu']
        rows += f'''<div style="position:absolute;left:70px;right:70px;top:{y}px;height:140px;border-radius:16px;background:rgba(255,255,255,0.07)">
<div style="position:absolute;left:30px;top:30px;width:160px;height:80px;background:#FFFFFF;transform:skewX(-12deg);display:flex;align-items:center;justify-content:center"><div style="transform:skewX(12deg);{BC};font-weight:600;font-size:34px;color:#0F1B2D">{e(m['date'])}</div></div>
<div style="position:absolute;left:208px;top:28px">{rond(m.get('logo'),m['adversaire'],84)}</div>
<div style="position:absolute;left:312px;top:26px;{BC};font-weight:600;font-size:42px">{pre} {e(m['adversaire'])}</div>
<div style="position:absolute;left:313px;top:82px;font-size:26px;color:#A7B0BD">{e(sous)}</div>
<div style="position:absolute;right:30px;top:44px;{BC};font-weight:600;font-size:46px;color:{BLEU}">{e(m['heure'])}</div></div>'''
        y += 158
    return f'''<div style="width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Barlow;color:#FFFFFF">{fond(1080,1350)}{entete(1080,'CALENDRIER')}
<div style="position:absolute;left:70px;top:206px;{BC};font-weight:700;font-size:96px;line-height:1.02">Les matchs<br><span style="color:{BLEU}">{e(f['mois'])}</span></div>
{rows}
<div style="position:absolute;left:0;right:0;top:1276px;text-align:center;font-size:26px;color:#A7B0BD">{e(f.get('pied','Horaires sous réserve · angersdirect.fr'))}</div></div>'''


def jdm(f, paysage):
    if paysage:
        W, H, d, cy = 1920, 1080, 380, 297
        lx, rx = 233, 1307
    else:
        W, H, d, cy = 1080, 1920, 354, 590
        lx, rx = 93, 633
    top = 70 if paysage else 230
    band_h = d + 20
    vs_w, vs_h = (180, 172) if paysage else (150, 160)
    infos = (f'''<div style="position:absolute;left:0;right:0;top:826px;text-align:center;{BC};font-weight:700;font-size:72px">{e(f['date'])} · {e(f['heure'])}</div>
<div style="position:absolute;left:0;right:0;top:914px;text-align:center;font-size:32px;color:#D3D5D9">{e(f['stade'])} · Live sur angersdirect.fr</div>''' if paysage else
             f'''<div style="position:absolute;left:0;right:0;top:1238px;text-align:center;{BC};font-weight:700;font-size:72px">{e(f['date'])}</div>
<div style="position:absolute;left:0;right:0;top:1326px;text-align:center;{BC};font-weight:700;font-size:116px;line-height:1">{e(f['heure'])}</div>
<div style="position:absolute;left:0;right:0;top:1468px;text-align:center;font-size:34px">{e(f['stade'])}</div>
<div style="position:absolute;left:0;right:0;top:1520px;text-align:center;font-size:28px;color:#D3D5D9">{e((('Diffusion : ' + f['diffusion'] + ' · ') if f.get('diffusion') else '') + 'Live texte sur angersdirect.fr')}</div>''')
    ny = cy + band_h + 22
    return f'''<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;font-family:Barlow;color:#FFFFFF">{fond(W,H)}{entete(W,'JOUR DE MATCH',False,top)}
<div style="position:absolute;left:0;right:0;top:{cy-80}px;text-align:center;font-size:34px;letter-spacing:4px;color:{BLEU}">LIGUE 1 · {e(f['journee']).upper()}</div>
<div style="position:absolute;left:0;right:0;top:{cy-8}px;height:{band_h}px;background:rgba(255,255,255,0.10);border-top:2px solid rgba(255,255,255,0.4);border-bottom:2px solid rgba(255,255,255,0.4)"></div>
<div style="position:absolute;left:{lx}px;top:{cy}px">{rond(f['dom'].get('logo'),f['dom']['nom'],d)}</div>
<div style="position:absolute;left:{rx}px;top:{cy}px">{rond(f['ext'].get('logo'),f['ext']['nom'],d)}</div>
<div style="position:absolute;left:{W//2 - vs_w//2}px;top:{cy + d//2 - vs_h//2}px;width:{vs_w}px;height:{vs_h}px;background:#FFFFFF;transform:skewX(-12deg);display:flex;align-items:center;justify-content:center"><div style="transform:skewX(12deg);{BC};font-weight:700;font-size:{int(vs_h*0.72)}px;color:#0F1B2D">VS</div></div>
<div style="position:absolute;left:{lx}px;width:{d}px;top:{ny}px;text-align:center;{BC};font-weight:600;font-size:48px">{e(f['dom']['nom'])}</div>
<div style="position:absolute;left:{rx}px;width:{d}px;top:{ny}px;text-align:center;{BC};font-weight:600;font-size:48px">{e(f['ext']['nom'])}</div>
{infos}</div>'''


TYPES = {'score': (score, 1080, 1350), 'classement': (classement, 1080, 1350), 'calendrier': (calendrier, 1080, 1350),
         'jdm_story': (lambda f: jdm(f, False), 1080, 1920), 'jdm_paysage': (lambda f: jdm(f, True), 1920, 1080)}


def main():
    fiche = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    fn, W, H = TYPES[fiche['type']]
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>{polices()}body{{margin:0}}</style></head><body>{fn(fiche)}</body></html>"
    tmp = sortie.with_suffix('.html')
    tmp.write_text(page)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto('file://' + str(tmp))
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(sortie), clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        b.close()
    tmp.unlink()
    print('ok', sortie)


if __name__ == '__main__':
    main()
