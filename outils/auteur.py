"""Signature des fichiers Angers Direct.

Règle de Valentin (28/11/2026) : chaque image ou vidéo créée pour Angers Direct
porte « angersdirect.fr » comme auteur dans ses métadonnées.

- PNG : chunks texte Author, Copyright, Source, Software + EXIF Artist/Copyright
- JPEG / WebP : EXIF Artist, Copyright, Software
- MP4 / MOV : métadonnées artist, author, copyright, comment (ffmpeg, sans réencodage)

Usage en ligne de commande (fichiers ou dossiers) : python3 outils/auteur.py fichier1.png dossier/ ...
"""
import pathlib, shutil, subprocess, sys
from PIL import Image
from PIL.PngImagePlugin import PngInfo

AUTEUR = 'angersdirect.fr'
COPYRIGHT = '© Angers Direct, angersdirect.fr'
IMAGES = {'.png', '.jpg', '.jpeg', '.webp'}
VIDEOS = {'.mp4', '.mov', '.m4v'}


def _exif(im):
    ex = im.getexif()
    ex[0x013B] = AUTEUR        # Artist
    ex[0x8298] = 'Copyright Angers Direct, angersdirect.fr'  # Copyright (EXIF = ASCII)
    ex[0x0131] = AUTEUR        # Software
    return ex


def signer(chemin):
    p = pathlib.Path(chemin)
    ext = p.suffix.lower()
    if ext in IMAGES:
        im = Image.open(p)
        im.load()
        if ext == '.png':
            info = PngInfo()
            for k, v in (('Author', AUTEUR), ('Copyright', COPYRIGHT), ('Source', AUTEUR), ('Software', AUTEUR)):
                info.add_text(k, v)
            im.save(p, pnginfo=info, exif=_exif(im), optimize=True)
        elif ext in ('.jpg', '.jpeg'):
            im.convert('RGB').save(p, quality=95, exif=_exif(im), subsampling=0)
        else:
            im.save(p, quality=95, exif=_exif(im))
    elif ext in VIDEOS:
        tmp = p.with_name(p.stem + '.signe' + p.suffix)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(p), '-map', '0', '-c', 'copy',
                        '-metadata', f'artist={AUTEUR}', '-metadata', f'author={AUTEUR}',
                        '-metadata', f'copyright={COPYRIGHT}', '-metadata', f'comment={AUTEUR}',
                        '-movflags', '+faststart', str(tmp)], check=True)
        shutil.move(tmp, p)
    return p


if __name__ == '__main__':
    for a in sys.argv[1:]:
        a = pathlib.Path(a)
        for f in (sorted(a.rglob('*')) if a.is_dir() else [a]):
            if f.suffix.lower() in IMAGES | VIDEOS:
                signer(f); print('signé', f)
