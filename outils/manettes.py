import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image, ImageDraw, ImageFilter
import random
W,H=2400,1600; S=1
im=Image.new('RGB',(W,H))
d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=(int(30+40*t),int(18+20*t),int(60+30*t)))
# glow
g=Image.new('L',(W,H),0); gd=ImageDraw.Draw(g); gd.ellipse([500,200,1900,1500],fill=150); g=g.filter(ImageFilter.GaussianBlur(220))
im=Image.composite(Image.new('RGB',(W,H),(230,90,160)),im,g.point(lambda v:v*0.55))
d=ImageDraw.Draw(im)
random.seed(4)
# pixel confetti
for _ in range(140):
    x,y=random.randrange(W),random.randrange(H); s=random.choice([14,20,26])
    c=random.choice([(255,210,60),(80,220,255),(255,90,120),(140,255,140)])
    d.rectangle([x,y,x+s,y+s],fill=c)
def ctrl(cx,cy,sc,ang,body,acc):
    L=Image.new('RGBA',(1400,800),(0,0,0,0)); q=ImageDraw.Draw(L)
    q.rounded_rectangle([60,180,1340,620],radius=200,fill=(0,0,0,90))
    q.rounded_rectangle([40,150,1320,590],radius=200,fill=body)
    q.rounded_rectangle([40,150,1320,330],radius=180,fill=tuple(min(255,c+25) for c in body))
    q.rounded_rectangle([40,250,1320,590],radius=200,fill=body)
    # dpad
    q.rounded_rectangle([210,300,290,520],radius=14,fill=(35,35,45)); q.rounded_rectangle([140,370,360,450],radius=14,fill=(35,35,45))
    # buttons
    for (x,y),c in zip([(1030,330),(1160,420),(900,420),(1030,510)],[acc,(80,200,255),(255,210,60),(120,230,120)]):
        q.ellipse([x-55,y-55,x+55,y+55],fill=(25,25,30)); q.ellipse([x-48,y-52,x+48,y+44],fill=c)
    q.rounded_rectangle([560,420,660,455],radius=16,fill=(50,50,60)); q.rounded_rectangle([700,420,800,455],radius=16,fill=(50,50,60))
    # cable
    q.line([(680,150),(680,60),(640,0)],fill=(30,30,35),width=22)
    L=L.rotate(ang,expand=True,resample=Image.BICUBIC); L=L.resize((int(L.width*sc),int(L.height*sc)),Image.LANCZOS)
    im.paste(L,(cx-L.width//2,cy-L.height//2),L)
ctrl(780,1000,0.85,14,(205,205,215),(230,60,80))
ctrl(1650,700,0.95,-10,(70,70,90),(255,80,120))
im=im.filter(ImageFilter.GaussianBlur(0.6))
im.save('/home/claude/angersdirect-visuels/outils/photos/retrogaming-manettes-illustration.jpg',quality=90)
__import__('auteur').signer('/home/claude/angersdirect-visuels/outils/photos/retrogaming-manettes-illustration.jpg')
im.resize((800,533)).save('/tmp/claude-0/m.jpg')
