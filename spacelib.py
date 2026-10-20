from casioplot import *
from random import randint

K=(0,0,0)
WH=(255,255,255)
SC=(0,220,255)
RD=(255,40,40)
AC=((80,255,80),(255,80,200),(255,160,0))
D=150
best=0

def box(x,y,w,h,c):
    for a in range(max(0,x),min(384,x+w)):
        for b in range(max(0,y),min(192,y+h)):
            set_pixel(a,b,c)

def ship(x,y,c):
    box(x+7,y,2,4,c)
    box(x+4,y+4,8,6,c)
    box(x,y+8,16,4,c)

def alien(e,c):
    x=e[0]
    y=e[1]
    if c==K:
        box(x,y,14,10,K)
        return
    box(x+2,y,10,6,c)
    box(x,y+4,14,3,c)
    box(x+1,y+7,3,3,c)
    box(x+10,y+7,3,3,c)
    box(x+4,y+2,2,2,K)
    box(x+8,y+2,2,2,K)

def hud(s,l,w):
    box(0,0,384,12,K)
    draw_string(4,1,"Score "+str(s)+"  Best "+str(max(s,best))+"  Wave "+str(w),WH,"small")
    for i in range(l):ship(296+i*17,0,SC)

def say(t,c):
    box(20,80,344,24,K)
    if t:draw_string(192-6*len(t),84,t,c)

def pick():
    while getkey():pass
    k=0
    while k not in (81,82,12):k=getkey()
    return (-1,1,0)[(12,81,82).index(k)]

def key():
    while getkey():pass
    k=0
    while k!=24 and k!=95 and k!=12:k=getkey()
    return k

