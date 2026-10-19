from casioplot import *
from random import randint

WH=(255,255,255)
K=(0,0,0)
BL=(30,80,255)
RD=(230,30,30)
LN=((190,14,2,178),(0,58,40,2),(0,132,40,2),(38,58,2,76),(344,58,40,2),(344,132,40,2),(344,58,2,76),(188,94,6,4),(0,74,3,44),(381,74,3,44))
D=100

def pc(a,b):
    for x,y,w,h in LN:
        if x<=a<x+w and y<=b<y+h:return WH
    return ((40,150,40),(60,170,60))[a//32%2]

def bg(x,y,w,h):
    for a in range(max(0,x),min(384,x+w)):
        for b in range(max(14,y),min(192,y+h)):
            set_pixel(a,b,pc(a,b))

def box(x,y,w,h,c):
    for a in range(max(0,x),min(384,x+w)):
        for b in range(max(0,y),min(192,y+h)):
            set_pixel(a,b,c)

def man(p,c):
    box(p[0]-3,p[1]-6,7,8,c)
    box(p[0]-2,p[1]-9,5,3,(240,190,150))
    box(p[0]-3,p[1]+2,2,3,K)
    box(p[0]+2,p[1]+2,2,3,K)

def hud(a,b,m):
    box(0,0,384,14,(20,20,20))
    draw_string(110,1,"YOU "+str(a)+" - "+str(b)+" CPU   "+str(m)+"'",WH,"small")

def kick(ball,gk):
    ball[0]+=ball[2]
    ball[1]+=ball[3]
    ball[2]-=ball[2]//24
    ball[3]-=ball[3]//24
    bx=ball[0]//16
    by=ball[1]//16
    if by<16 or by>188:ball[3]=-ball[3]
    if (bx<4 or bx>378) and not 76<by<116:ball[2]=-ball[2]
    for g in gk:
        if abs(g[0]-bx)<6 and abs(g[1]-by)<8:
            ball[2]=-ball[2]
            ball[0]+=ball[2]
    if bx<1:return 2
    if bx>381:return 1
    return 0
