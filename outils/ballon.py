"""Illustration originale (générée, libre de droits) : ballon de basket sur fond de salle. Usage : python3 outils/ballon.py -> outils/photos/ballon-basket.jpg"""
import numpy as np
from PIL import Image, ImageFilter
W,H=1600,2000
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
# fond : salle sombre avec halo de projecteur
bg=np.zeros((H,W,3),np.float32)
d=np.sqrt(((xx-W*0.5)/W)**2+((yy-H*0.30)/H)**2)
halo=np.clip(1-d*1.6,0,1)**2
bg[...,0]=12+70*halo; bg[...,1]=20+60*halo; bg[...,2]=38+80*halo
# parquet flou en bas
floor=np.clip((yy-H*0.68)/(H*0.32),0,1)
bg[...,0]+=floor*120; bg[...,1]+=floor*70; bg[...,2]+=floor*30
# ombre du ballon
cx,cy,R=W*0.5,H*0.43,560
sh=np.exp(-(((xx-cx)/(R*1.1))**2+((yy-(cy+R*1.02))/(R*0.18))**2)*2.5)
bg*= (1-0.75*sh)[...,None]
img=bg.copy()
nx=(xx-cx)/R; ny=(yy-cy)/R; r2=nx**2+ny**2; m=r2<1
nz=np.sqrt(np.clip(1-r2,0,1))
# rotation du ballon
a,b=0.85,-0.45
X=nx*np.cos(a)+nz*np.sin(a); Z=-nx*np.sin(a)+nz*np.cos(a); Y=ny
Y2=Y*np.cos(b)-Z*np.sin(b); Z2=Y*np.sin(b)+Z*np.cos(b); Y=Y2; Z=Z2
w=0.022
seam=(np.abs(X)<w)|(np.abs(Y)<w)|(np.abs(np.abs(X)-0.70)<w*1.1)
# éclairage
L=np.array([-0.45,-0.55,0.7]); L/=np.linalg.norm(L)
diff=np.clip(nx*L[0]+ny*L[1]+nz*L[2],0,1)
spec=np.clip(nx*L[0]+ny*L[1]+(nz)*L[2],0,1)**40
rng=np.random.default_rng(3); grain=rng.normal(0,1,(H,W)).astype(np.float32)
grain=np.array(Image.fromarray(((grain*20)+128).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),np.float32)/128-1
base=np.stack([232*np.ones_like(nx),105*np.ones_like(nx),38*np.ones_like(nx)],-1)
shade=(0.18+0.95*diff)[...,None]*(1+0.18*grain[...,None])
ball=base*shade+255*0.35*spec[...,None]
ball[seam]=np.array([25,15,10])*(0.4+0.8*diff[seam])[:,None]
rim=np.clip((r2-0.85)/0.15,0,1)[...,None]
ball=ball*(1-0.55*rim)
img[m]=ball[m]
# antialias bord
im=Image.fromarray(img.clip(0,255).astype(np.uint8))
im=im.filter(ImageFilter.GaussianBlur(0.6))
im.save('outils/photos/ballon-basket.jpg',quality=92)
