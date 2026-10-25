"""Génère une vidéo verticale Angers Direct (MP4 1080x1920, 30 i/s) pour TikTok, Reels et Shorts.

Usage : python3 outils/video.py fiche.json sortie.mp4

Style de la vidéo de présentation Angers Direct : photos plein cadre avec léger zoom,
logo blanc en haut à gauche, étiquette de rubrique en biais puis titre Barlow Condensed
qui monte en fondu, fondus enchaînés entre les scènes. La vidéo se termine TOUJOURS par
la carte de fin : bandes de couleur animées, logo, « Le média d'Angers et de sa région »,
les réseaux pour nous suivre et angersdirect.fr (ajoutée automatiquement).

Les textes restent dans la zone sûre de TikTok (ni le bas ni la marge droite, où
l'application affiche la légende et les boutons).

Fiche :
    {"duree_scene": 3.2,
     "scenes": [
       {"type": "photo", "photo": "chemin.jpg", "cadrage": "60% 50%",
        "rubrique": "CULTURE", "titre": "Que faire à Angers [ce dimanche] ?", "sous_titre": "..."},
       {"type": "photo", "photo": "chemin.jpg", "mode": "haut", ...},   (image peu haute : en haut, fondue dans le bleu nuit)
       {"type": "texte", "rubrique": "CULTURE", "chiffre": "2 expos", "titre": "...", "lignes": ["...", "..."]}
     ]}
    rubrique facultative ; les mots entre crochets s'affichent en bleu.
    Musique : composée automatiquement par musique.py (originale, libre de droits).
    "musique": false pour une piste muette, "graine": 3 pour une autre variante.
"""
import html, json, pathlib, re, subprocess, sys
from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from visuel import polices, COULEURS  # noqa: E402

FPS = 30
FONDU = 0.45
FIN = 4.8
NUIT = '#0F1B2D'
BANDES = ['#E8456B', '#F0A23A', '#F2C94C', '#3DCB6E', '#3A8DF5', '#8B5CF6']

ICONES = {
    'Instagram': '<rect x="3" y="3" width="18" height="18" rx="5.5" fill="none" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.3" fill="#fff"/>',
    'Facebook': '<path fill="#fff" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4V10.5H8v3h2.4V21z"/>',
    'TikTok': '<path fill="#fff" d="M15.6 3c.3 2.3 1.7 3.8 4 4v3c-1.5.1-2.8-.4-4-1.2v6.1c0 3.4-2.6 5.6-5.6 5.6S4.4 18.2 4.4 15.1c0-3.4 2.9-5.7 6.4-5.3v3.1c-1.6-.4-3.3.6-3.3 2.2 0 1.4 1.1 2.4 2.5 2.4 1.5 0 2.5-1 2.5-2.9V3z"/>',
    'YouTube': '<rect x="2" y="5.5" width="20" height="13" rx="4" fill="#fff"/><path d="M10 9v6l5.2-3z" fill="#0F1B2D"/>',
    'LinkedIn': '<rect x="3" y="3" width="18" height="18" rx="3" fill="#fff"/><path fill="#0F1B2D" d="M7 10h2.4v7H7zm1.2-3.6a1.4 1.4 0 1 1 0 2.8 1.4 1.4 0 0 1 0-2.8zM11 10h2.3v1c.4-.7 1.2-1.2 2.4-1.2 2 0 2.7 1.3 2.7 3.3V17H16v-3.5c0-.9-.2-1.7-1.2-1.7s-1.4.8-1.4 1.7V17H11z"/>',
}


def e(t):
    return html.escape(str(t))


def bleu(t):
    return re.sub(r'\[(.+?)\]', r'<span style="color:#4FA8FF">\1</span>', e(t))


def anim(nom, debut, duree, courbe='cubic-bezier(.2,.8,.2,1)'):
    return f'animation:{nom} {duree:.3f}s {courbe} {debut:.3f}s both;'


def scene_photo(s, t0, d):
    couleur = COULEURS.get(s.get('rubrique', 'ACTU').upper(), COULEURS['ACTU'])
    photo = pathlib.Path(s['photo']).resolve()
    if s.get('mode') == 'haut':
        img = (f'<img src="file://{photo}" style="position:absolute;left:0;top:0;width:1080px;'
               f'transform-origin:50% 0;{anim("zoom", t0, d + FONDU, "linear")}'
               '-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent 100%)">')
    else:
        img = (f'<img src="file://{photo}" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;'
               f'object-position:{s.get("cadrage", "50% 50%")};{anim("zoom", t0, d + FONDU, "linear")}">')
    tag = ''
    if s.get('rubrique'):
        tag = (f'<div style="align-self:flex-start;padding:6px 22px;background:{couleur};transform:skewX(-12deg);margin-bottom:28px;{anim("tag", t0 + .15, .5)}">'
               f'<div style="transform:skewX(12deg);font-family:\'Barlow Condensed\';font-weight:600;font-size:38px;letter-spacing:1px">{e(s["rubrique"].upper())}</div></div>')
    sous = (f'<div style="font-weight:500;font-size:44px;line-height:1.3;color:#E3E8EF;margin-top:24px;{anim("monte", t0 + .55, .6)}">{e(s["sous_titre"])}</div>'
            if s.get('sous_titre') else '')
    return f'''<div class="scene" style="background:{NUIT};{anim("entree", t0, FONDU, "linear")}">
{img}
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,22,38,.5) 0%,rgba(13,22,38,0) 14%,rgba(13,22,38,0) 40%,rgba(15,27,45,.85) 62%,{NUIT} 82%)"></div>
<div style="position:absolute;left:72px;right:150px;top:1130px;display:flex;flex-direction:column">
{tag}<div style="font-family:'Barlow Condensed';font-weight:700;font-size:104px;line-height:1.02;{anim("monte", t0 + .3, .6)}">{bleu(s["titre"])}</div>{sous}</div></div>'''


def scene_texte(s, t0, d):
    couleur = COULEURS.get(s.get('rubrique', 'CULTURE').upper(), COULEURS['CULTURE'])
    lignes = ''.join(f'<div style="font-weight:500;font-size:44px;line-height:1.3;color:#E3E8EF;margin-top:26px;{anim("monte", t0 + .7 + .25 * i, .6)}">{e(l)}</div>'
                     for i, l in enumerate(s.get('lignes', [])))
    return f'''<div class="scene" style="background:{NUIT};{anim("entree", t0, FONDU, "linear")}">
<div style="position:absolute;left:0;top:300px;height:420px;width:1080px;background:{couleur};{anim("balaye", t0 + .1, .7)}"></div>
<div style="position:absolute;left:72px;top:400px;font-family:'Barlow Condensed';font-weight:700;font-size:200px;line-height:1;{anim("monte", t0 + .35, .6)}">{e(s["chiffre"])}</div>
<div style="position:absolute;left:72px;right:150px;top:820px">
<div style="font-family:'Barlow Condensed';font-weight:700;font-size:104px;line-height:1.02;{anim("monte", t0 + .5, .6)}">{bleu(s["titre"])}</div>{lignes}</div></div>'''


def carte_fin(t0):
    bandes = ''.join(f'<div style="height:16px;width:{420 - 52 * i}px;margin-top:{0 if i == 0 else 10}px;background:{c};transform:skewX(-30deg);transform-origin:0 50%;{anim("bande", t0 + .1 + .08 * i, .55)}"></div>'
                     for i, c in enumerate(BANDES))
    icones = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;width:150px;{anim("pop", t0 + 1.5 + .12 * i, .45, "cubic-bezier(.3,1.6,.5,1)")}">'
                     f'<div style="width:112px;height:112px;border-radius:30px;background:rgba(255,255,255,.1);border:2px solid {BANDES[i % 6]};display:flex;align-items:center;justify-content:center">'
                     f'<svg width="62" height="62" viewBox="0 0 24 24">{svg}</svg></div>'
                     f'<div style="font-size:26px;font-weight:500;color:#C9D3E0;margin-top:14px">{nom}</div></div>'
                     for i, (nom, svg) in enumerate(ICONES.items()))
    return f'''<div class="scene" style="background:linear-gradient(180deg,#0D1626 0%,#152A48 100%);{anim("entree", t0, FONDU, "linear")}">
<div style="position:absolute;left:90px;top:300px">{bandes}</div>
<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:90px;top:520px;width:520px;{anim("monte", t0 + .5, .6)}">
<div style="position:absolute;left:90px;right:120px;top:740px;font-family:'Barlow Condensed';font-weight:600;font-size:64px;line-height:1.1;{anim("monte", t0 + .8, .6)}">Le média d'Angers et de sa région</div>
<div style="position:absolute;left:90px;top:900px;padding:8px 26px;background:{COULEURS['ACTU']};transform:skewX(-12deg);{anim("tag", t0 + 1.1, .5)}"><div style="transform:skewX(12deg);font-family:'Barlow Condensed';font-weight:700;font-size:46px;letter-spacing:1px">SUIVEZ-NOUS</div></div>
<div style="position:absolute;left:60px;right:60px;top:1040px;display:flex;justify-content:space-between">{icones}</div>
<div style="position:absolute;left:90px;top:1290px;font-weight:600;font-size:48px;{anim("monte", t0 + 2.3, .6)}">@angersdirect</div>
<div style="position:absolute;left:90px;top:1370px;font-family:'Barlow Condensed';font-weight:700;font-size:92px;color:#4FA8FF;{anim("monte", t0 + 2.55, .6)}">angersdirect.fr</div>
</div>'''


def page(fiche):
    d = fiche.get('duree_scene', 3.2)
    t, blocs = 0.0, []
    for s in fiche['scenes']:
        blocs.append((scene_texte if s['type'] == 'texte' else scene_photo)(s, t, d))
        t += d
    blocs.append(carte_fin(t))
    total = t + FIN
    css = polices() + f'''
body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{NUIT}}}
.scene{{position:absolute;inset:0;overflow:hidden;font-family:Barlow;color:#fff}}
@keyframes entree{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes zoom{{from{{transform:scale(1.0)}}to{{transform:scale(1.09)}}}}
@keyframes monte{{from{{opacity:0;transform:translateY(60px)}}to{{opacity:1;transform:none}}}}
@keyframes tag{{from{{opacity:0;transform:skewX(-12deg) translateX(-140px)}}to{{opacity:1;transform:skewX(-12deg)}}}}
@keyframes balaye{{from{{transform:scaleX(0);transform-origin:0 50%}}to{{transform:scaleX(1);transform-origin:0 50%}}}}
@keyframes bande{{from{{opacity:0;transform:skewX(-30deg) translateX(-480px)}}to{{opacity:1;transform:skewX(-30deg)}}}}
@keyframes pop{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:scale(1)}}}}
'''
    logo = f'<img src="file://{ICI}/assets/logo_blanc.png" style="position:absolute;left:72px;top:110px;width:230px;z-index:9">'
    corps = '\n'.join(blocs)
    return f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{corps}{logo}<div id="fin" style="display:none" data-t="{t}"></div></body></html>', total, t


def main():
    fiche = json.load(open(sys.argv[1]))
    sortie = pathlib.Path(sys.argv[2]).resolve()
    contenu, total, debut_fin = page(fiche)
    tmp = sortie.with_suffix('.html')
    tmp.write_text(contenu)
    n = int(round(total * FPS))
    wav = sortie.with_suffix('.wav')
    if fiche.get('musique', True):
        subprocess.run([sys.executable, str(ICI / 'musique.py'), f'{total:.3f}', str(wav), str(fiche.get('graine', 7))], check=True)
        audio = ['-i', str(wav)]
    else:
        audio = ['-f', 'lavfi', '-t', f'{total:.3f}', '-i', 'anullsrc=r=44100:cl=stereo']
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                           *audio,
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(sortie)], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(f'file://{tmp}')
        pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready')
        pg.evaluate('document.getAnimations().forEach(a => a.pause())')
        for i in range(n):
            ms = i * 1000 / FPS
            pg.evaluate(f'''(() => {{
                const t = {ms};
                document.getAnimations().forEach(a => a.currentTime = t);
                const fin = {debut_fin * 1000};
                document.querySelectorAll('body > img').forEach(l => l.style.opacity = Math.min(1, Math.max(0, 1 - (t - fin) / {FONDU * 1000})));
            }})()''')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
        b.close()
    ff.stdin.close()
    ff.wait()
    tmp.unlink()
    wav.unlink(missing_ok=True)
    print('ok', sortie, f'{total:.1f} s', n, 'images')


if __name__ == '__main__':
    main()
