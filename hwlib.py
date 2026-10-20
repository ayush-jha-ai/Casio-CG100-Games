from casioplot import *
from random import randint

BG=(25,0,45)
OR=(255,130,0)
K=(0,0,0)
WH=(255,255,255)
CC=((255,60,160),(80,220,80),(80,160,255),(255,230,0))
D=200
best=0

def box(x,y,w,h,c):
    for a in range(max(0,x),min(384,x+w)):
        for b in range(max(0,y),min(192,y+h)):
            set_pixel(a,b,c)

def pump(x,y,s):
    box(x,y+2*s,6*s,4*s,OR)
    box(x+2*s,y,2*s,2*s,(0,120,0))
    if s>2:
        box(x+4,y+16,4,4,K)
        box(x+16,y+16,4,4,K)
        box(x+6,y+22,12,3,K)

def hud(s,l,m,lv):
    box(0,0,300,16,BG)
    draw_string(4,1,"Score "+str(s)+"  Best "+str(max(s,best))+"  Lv "+str(lv),OR,"small")
    if m>1:draw_string(250,1,"x"+str(m),(255,255,0),"small")
    box(306,138,78,12,BG)
    for i in range(l):pump(306+i*15,138,2)

def item(e,c):
    x=e[0]
    y=e[1]
    t=e[2]
    if c==0:box(x,y,12,12,BG)
    elif t==0:
        box(x+3,y+3,6,6,c)
        box(x,y+4,3,4,c)
        box(x+9,y+4,3,4,c)
    elif t==1:
        box(x+2,y,8,8,(255,215,0))
        box(x+5,y+8,2,4,WH)
    elif t==2:
        box(x+1,y,10,12,WH)
        box(x+3,y+3,2,3,K)
        box(x+7,y+3,2,3,K)
    elif t==3:
        box(x+4,y+3,4,5,(150,90,200))
        box(x,y+2*(e[3]>0),4,3,(150,90,200))
        box(x+8,y+2*(e[3]<0),4,3,(150,90,200))
    else:
        box(x+1,y+2,4,4,(230,20,40))
        box(x+7,y+2,4,4,(230,20,40))
        box(x+2,y+5,8,4,(230,20,40))
        box(x+4,y+9,4,2,(230,20,40))

def say(t):
    box(40,60,260,24,BG)
    if t:draw_string(170-6*len(t),64,t,(255,255,0))

def key():
    while getkey():pass
    k=0
    while k!=24 and k!=95 and k!=12:k=getkey()
    return k

