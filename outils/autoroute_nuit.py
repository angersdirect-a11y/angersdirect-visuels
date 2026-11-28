import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
"""Illustration originale : autoroute la nuit, chantier balisé (flèches lumineuses orange, cônes), traînées de phares.
Aucun droit tiers. Usage : python3 outils/autoroute_nuit.py sortie.jpg"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 2400, 1600
HOR = int(0.42 * H)
VX = int(0.55 * W)
rng = np.random.default_rng(16)

# ciel nocturne en dégradé
yy = np.linspace(0, 1, H)[:, None]
ciel = np.zeros((H, W, 3), np.float32)
ciel[..., 0] = 8 + 22 * yy
ciel[..., 1] = 14 + 30 * yy
ciel[..., 2] = 34 + 50 * yy
img = Image.fromarray(ciel.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)

# silhouette de haies à l'horizon
pts = [(0, HOR)]
for x in range(0, W + 40, 40):
    pts.append((x, HOR - 20 - int(28 * abs(np.sin(x / 170.0))) - int(rng.integers(0, 14))))
pts.append((W, HOR + 40)); pts.append((0, HOR + 40))
d.polygon(pts, fill=(10, 16, 26))

# bas-côtés et chaussée en perspective
d.polygon([(0, HOR + 20), (W, HOR + 20), (W, H), (0, H)], fill=(14, 20, 30))
d.polygon([(VX - 30, HOR), (VX + 30, HOR), (int(W * 1.25), H), (int(-W * 0.25), H)], fill=(34, 38, 46))


def proj(t, u):
    """t : 0 horizon -> 1 bas de l'image ; u : position latérale (-1 gauche, 1 droite de la chaussée)."""
    y = HOR + t * (H - HOR)
    demi = 30 + t * (W * 0.75 - 30)
    return VX + u * demi, y


# marquages au sol
for k in range(14):
    t0 = (k / 14) ** 2
    t1 = ((k + 0.45) / 14) ** 2
    for u in (-0.33, 0.33):
        a, b = proj(t0, u), proj(t1, u)
        w0, w1 = 1 + 6 * t0, 1 + 6 * t1
        d.polygon([(a[0] - w0, a[1]), (a[0] + w0, a[1]), (b[0] + w1, b[1]), (b[0] - w1, b[1])], fill=(200, 200, 190))

# couche lumineuse (additive, floutée)
lum = Image.new('RGB', (W, H), (0, 0, 0))
dl = ImageDraw.Draw(lum)
# traînées de phares (blanc à gauche, rouge à droite)
for u, col in [(-0.62, (255, 236, 200)), (-0.5, (255, 226, 180)), (0.12, (255, 60, 40)), (0.24, (255, 40, 30))]:
    line = [proj((s / 60) ** 1.6, u) for s in range(61)]
    for i in range(60):
        t = (i / 60) ** 1.6
        dl.line([line[i], line[i + 1]], fill=col, width=int(2 + 16 * t))
# cônes et lampes de chantier orange sur la voie de droite
for k in range(1, 16):
    t = (k / 16) ** 1.7
    x, y = proj(t, 0.5)
    r = 3 + 26 * t
    dl.ellipse([x - r, y - 2.2 * r, x + r, y], fill=(255, 140, 20))
# flèche lumineuse de rabattement
fx, fy = proj(0.42, 0.62)
s = 150
dl.rectangle([fx - s, fy - 2.2 * s, fx + s, fy - 0.4 * s], fill=(40, 30, 10))
for i, (dx, dy) in enumerate([(-0.6, 0), (-0.25, 0), (0.1, 0), (0.45, 0), (0.1, -0.35), (0.1, 0.35), (0.3, -0.18), (0.3, 0.18)]):
    cx, cy = fx + dx * s, fy - 1.3 * s + dy * s
    dl.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 170, 30))

halo = lum.filter(ImageFilter.GaussianBlur(28))
net = lum.filter(ImageFilter.GaussianBlur(3))
a = np.asarray(img, np.float32) + 1.1 * np.asarray(halo, np.float32) + 0.9 * np.asarray(net, np.float32)
# reflets sur la chaussée mouillée
refl = np.asarray(halo.transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(40)), np.float32)
masque = np.zeros((H, 1, 1), np.float32); masque[HOR:] = 0.18
a += refl * masque
# grain léger
a += rng.normal(0, 3, a.shape)
Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(sys.argv[1], quality=92)
__import__('auteur').signer(sys.argv[1])
