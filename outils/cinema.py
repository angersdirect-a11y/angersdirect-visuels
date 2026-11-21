"""Illustration originale : salle de projection au cinéma fantastique (écran avec lune, forêt et château), faisceau du projecteur, spectateurs en silhouette."""
import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter
W,H=2400,1350
random.seed(7); rng=np.random.default_rng(7)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
img=np.zeros((H,W,3),np.float32)
img[...]=[10,14,30]
# écran
sx0,sy0,sx1,sy1=560,140,1840,820
scr=np.zeros((H,W),bool); scr[sy0:sy1,sx0:sx1]=True
# ciel de l'écran : dégradé nuit violet -> bleu
t=np.clip((yy-sy0)/(sy1-sy0),0,1)
sky=np.stack([40+60*t,30+40*t,90+50*t],-1)
img[scr]=sky[scr]
# lune
mx,my,mr=1450,330,95
d=np.sqrt((xx-mx)**2+(yy-my)**2)
glow=np.exp(-((d/mr-1).clip(0))*2.2)*scr
img+= (glow[...,None]*np.array([90,80,60]))
moon=(d<mr)&scr
img[moon]=[245,235,200]
# étoiles
for _ in range(160):
    x=random.randint(sx0,sx1-1); y=random.randint(sy0,sy0+380)
    if math.hypot(x-mx,y-my)<mr+20: continue
    r=random.choice([1,1,2,2,3]); b=random.randint(160,255)
    img[max(y-r,0):y+r,max(x-r,0):x+r]=[b,b,b*0.9]
im=Image.fromarray(img.clip(0,255).astype(np.uint8))
dr=ImageDraw.Draw(im)
# collines et forêt en silhouette sur l'écran
def colline(base,amp,col,seed):
    r=random.Random(seed); pts=[(sx0,sy1)]
    for x in range(sx0,sx1+1,20):
        y=base-amp*math.sin((x-sx0)/170+seed)-r.uniform(0,18); pts.append((x,y))
    pts.append((sx1,sy1)); dr.polygon(pts,fill=col)
colline(650,40,(36,30,70),1)
# château de conte
cx=1050; base=600
dr.rectangle([cx-90,base-120,cx+90,sy1],fill=(22,18,46))
for tx,h in [(cx-110,200),(cx+110,200),(cx,260)]:
    dr.rectangle([tx-28,base-h,tx+28,sy1],fill=(22,18,46))
    dr.polygon([(tx-38,base-h),(tx+38,base-h),(tx,base-h-80)],fill=(22,18,46))
for wx,wy in [(cx-110,base-140),(cx+110,base-140),(cx,base-200),(cx-30,base-40),(cx+30,base-40)]:
    dr.rectangle([wx-7,wy-12,wx+7,wy+10],fill=(255,205,110))
colline(720,30,(18,16,36),3)
# sapins
for x in range(sx0,sx1,46):
    h=random.randint(70,150); b=sy1-random.randint(0,30)
    dr.polygon([(x,b),(x+23,b-h),(x+46,b)],fill=(12,12,26))
# cadre écran
dr.rectangle([sx0-8,sy0-8,sx1+8,sy1+8],outline=(70,70,90),width=8)
# rideaux rouges
for side in (0,1):
    for i in range(10):
        x0=(0 if side==0 else W-420)+i*42
        c=110+ (30 if i%2 else 0)
        dr.rectangle([x0,0,x0+42,H],fill=(c,16,28))
arr=np.array(im).astype(np.float32)
# faisceau projecteur depuis le haut-fond vers l'écran
px,py=1200,1350
beam=np.zeros((H,W),np.float32)
ang=np.arctan2(yy-py,xx-px); dist=np.sqrt((xx-px)**2+(yy-py)**2)
a0=math.atan2(sy0-py,sx0-px); a1=math.atan2(sy0-py,sx1-px)
inside=(ang>a0)&(ang<a1)&(yy>sy1-40)
beam[inside]=0.12*np.exp(-dist[inside]/1400)
dust=rng.random((H,W))>0.9985
beam+=dust*inside*0.5
arr+=beam[...,None]*np.array([255,240,200])
# spectateurs en silhouette
im=Image.fromarray(arr.clip(0,255).astype(np.uint8)); dr=ImageDraw.Draw(im)
for row,(yb,s) in enumerate([(1180,1.0),(1290,1.25)]):
    x=180+row*60
    while x<W-150:
        r=int(random.randint(42,55)*s)
        dr.ellipse([x-r,yb-2.6*r,x+r,yb-0.6*r],fill=(6,6,14))
        dr.rounded_rectangle([x-int(1.9*r),yb-0.9*r,x+int(1.9*r),H],radius=40,fill=(6,6,14))
        x+=int(random.randint(150,200)*s)
im=im.filter(ImageFilter.GaussianBlur(0.8))
im.save('outils/photos/cinema-fantastique.jpg',quality=92)
print('ok')
