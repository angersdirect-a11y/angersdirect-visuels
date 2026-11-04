"""Illustration originale : route de campagne la nuit, gyrophares bleus flous et reflets sur l'asphalte mouillé.
Aucun droit tiers. Usage : python3 outils/gyrophares.py sortie.jpg"""
import sys, math
import numpy as np
from PIL import Image, ImageFilter

W, H = 2400, 1600
rng = np.random.default_rng(30)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
hor = 0.52 * H

# ciel nocturne
t = np.clip(yy / hor, 0, 1)[..., None]
img = (1 - t) * np.array([6, 10, 24]) + t * np.array([20, 30, 58])

# route en perspective
vx = W * 0.5
road_half = (yy - hor) / (H - hor) * W * 0.62
road = (yy > hor) & (np.abs(xx - vx) < road_half)
ground = yy > hor
img[ground] = [10, 13, 20]
g = np.clip((yy - hor) / (H - hor), 0, 1)
asph = np.stack([16 + 10 * g, 20 + 12 * g, 30 + 16 * g], -1)
img[road] = asph[road]
# ligne médiane pointillée
dash = road & (np.abs(xx - vx) < 4 + 22 * g) & (np.sin(1 / np.maximum(g, 0.02) * 9) > 0.2)
img[dash] = [150, 150, 140]

# silhouettes d'arbres de chaque côté (haies du bocage)
rows = []
for side in (-1, 1):
    for i in range(70):
        x = vx + side * (W * 0.06 + rng.random() * W * 0.5)
        r = 40 + rng.random() * 130
        cy = hor - r * (0.3 + rng.random() * 0.6)
        mask = (xx - x) ** 2 + ((yy - cy) * 1.2) ** 2 < r ** 2
        img[mask & ~road] = [4, 6, 12]
img = np.clip(img, 0, 255)

# lumières : gyrophares bleus, un rouge, feux orange lointains
glow = np.zeros_like(img)


def lumiere(x, y, r, col, k):
    d2 = (xx - x) ** 2 + (yy - y) ** 2
    glow[...] += k * np.exp(-d2 / (2 * r * r))[..., None] * np.array(col) / 255
    # reflet vertical étiré sur l'asphalte mouillé
    if y < H:
        dy = yy - y
        ref = np.exp(-((xx - x) ** 2) / (2 * (r * 0.7) ** 2)) * np.exp(-np.maximum(dy, 0) / (H * 0.35)) * (dy > r * 0.6)
        glow[...] += 0.35 * k * ref[..., None] * np.array(col) / 255 * (road[..., None] * 1.0 + 0.2)


for x, y, r, col, k in [
    (vx - 160, hor + 40, 90, (40, 110, 255), 1.8),
    (vx + 120, hor + 30, 80, (60, 140, 255), 1.6),
    (vx - 40, hor + 10, 55, (30, 90, 255), 1.3),
    (vx + 420, hor + 70, 120, (40, 120, 255), 1.1),
    (vx - 520, hor + 90, 140, (50, 110, 240), 0.9),
    (vx + 260, hor + 45, 60, (255, 50, 60), 0.9),
    (vx - 300, hor + 20, 40, (255, 170, 70), 0.6),
    (vx + 600, hor - 10, 35, (255, 180, 90), 0.5),
]:
    lumiere(x, y, r, col, k)

# petits points de bokeh
for _ in range(35):
    x = vx + rng.normal(0, 380); y = hor + rng.normal(30, 60); r = 6 + rng.random() * 22
    col = (60, 130, 255) if rng.random() < 0.8 else (255, 80, 80)
    lumiere(x, y, r, col, 0.15 + rng.random() * 0.25)

out = np.clip(img + 255 * (1 - np.exp(-glow * 1.1)), 0, 255).astype(np.uint8)
im = Image.fromarray(out).filter(ImageFilter.GaussianBlur(3))
# grain léger
n = rng.normal(0, 4, (H, W, 1))
im = Image.fromarray(np.clip(np.asarray(im, np.float32) + n, 0, 255).astype(np.uint8))
im.save(sys.argv[1], quality=92)
