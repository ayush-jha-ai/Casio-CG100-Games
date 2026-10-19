from casioplot import *
from random import randint

BG=(25,0,45)
OR=(255,130,0)
K=(0,0,0)
WH=(255,255,255)
CC=((255,60,160),(80,220,80),(80,160,255),(255,230,0))
D=200

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def hud(s,l):
    box(0,0,300,16,BG)
    draw_string(4,1,"Candy "+str(s)+"   Lives "+str(l),OR,"small")

def bucket(x,c):
    if c:
        box(x,160,24,16,OR)
        box(x+8,156,8,4,(0,120,0))
        box(x+4,164,4,4,K)
        box(x+16,164,4,4,K)
        box(x+6,170,12,3,K)
    else:box(x,156,24,20,BG)

def item(t,x,y,c):
    if c==0:box(x,y,12,12,BG)
    elif t:
        box(x+1,y,10,12,WH)
        box(x+3,y+3,2,3,K)
        box(x+7,y+3,2,3,K)
    else:
        box(x+3,y+3,6,6,c)
        box(x,y+4,3,4,c)
        box(x+9,y+4,3,4,c)

def main():
    while True:
        clear_screen()
        box(0,0,384,192,BG)
        for d in range(-16,17):
            w=int((289-d*d)**0.5)
            box(340-w,40+d,2*w,1,(250,240,200))
        box(0,176,384,16,(20,60,20))
        draw_string(306,80,"TRICK",OR)
        draw_string(306,100,"OR",OR)
        draw_string(306,120,"TREAT",OR)
        s=0
        l=3
        x=138
        it=[]
        f=0
        hud(s,l)
        bucket(x,1)
        while l:
            k=getkey()
            if k==12:return
            if k==23 and x>0 or k==25 and x<276:
                bucket(x,0)
                x+=(k-24)*6
                bucket(x,1)
            sp=2+s//150
            if len(it)<3+s//200 and randint(0,20)==0:
                t=randint(0,5)==0
                it.append([randint(0,30)*9,18,t,CC[randint(0,3)]])
            for e in it[:]:
                item(e[2],e[0],e[1],0)
                e[1]+=sp
                if e[1]>146 and e[1]<170 and x-10<e[0]<x+22:
                    it.remove(e)
                    if e[2]:l-=1
                    else:s+=10
                    hud(s,l)
                    bucket(x,1)
                elif e[1]>162:it.remove(e)
                else:item(e[2],e[0],e[1],e[3])
            show_screen()
            for i in range(D):pass
            f+=1
        draw_string(110,80,"GAME OVER",OR,"large")
        draw_string(130,120,"OK: again",WH)
        show_screen()
        while getkey():pass
        k=0
        while k!=24 and k!=95 and k!=12:k=getkey()
        if k==12:return

main()
