"""Transforme un visuel 1080x1350 (ou autre) en story 1080x1920 sans rien couper.

Usage : python3 outils/story.py visuel.png story.png

Le visuel est posé en entier au centre ; au-dessus et en dessous, le même visuel flouté et assombri
remplit le format 9:16. Instagram et Facebook recadrent toute story qui n'est pas en 1080x1920 :
toute story doit donc passer par ce script (sauf les modèles déjà en 1080x1920 : jdm_story, heure d'hiver story).
"""
import sys
from PIL import Image, ImageFilter, ImageEnhance

W, H = 1080, 1920
src = Image.open(sys.argv[1]).convert('RGB')
if src.size == (W, H):
    src.save(sys.argv[2]); print('ok (déjà 1080x1920)', sys.argv[2]); sys.exit()
r = max(W / src.width, H / src.height)
fond = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
fond = fond.crop(((fond.width - W) // 2, (fond.height - H) // 2, (fond.width - W) // 2 + W, (fond.height - H) // 2 + H))
fond = ImageEnhance.Brightness(fond.filter(ImageFilter.GaussianBlur(40))).enhance(0.55)
k = min(W / src.width, H / src.height)
img = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
fond.paste(img, ((W - img.width) // 2, (H - img.height) // 2))
fond.save(sys.argv[2], optimize=True); print('ok', sys.argv[2])
