from casioplot import *
from random import randint

K=(0,0,0)
WH=(255,255,255)
SC=(0,220,255)
AC=((80,255,80),(255,80,200),(255,160,0))
D=150

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def ship(x,c):
    box(x+7,172,2,4,c)
    box(x+4,176,8,6,c)
    box(x,180,16,4,c)

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

def hud(s,l):
    box(0,0,384,12,K)
    draw_string(4,1,"Score "+str(s),WH,"small")
    draw_string(300,1,"Ships "+str(l),WH,"small")

def main():
    while True:
        clear_screen()
        box(0,0,384,192,K)
        for i in range(50):
            set_pixel(randint(0,383),randint(14,191),(randint(90,255),)*3)
        s=0
        l=3
        x=180
        bu=[]
        al=[]
        lk=0
        f=0
        hud(s,l)
        ship(x,SC)
        while l:
            k=getkey()
            if k==12:return
            if k==23 and x>0 or k==25 and x<362:
                ship(x,K)
                x+=(k-24)*6
                ship(x,SC)
            if (k==24 or k==95 or k==14) and k!=lk and len(bu)<3:bu.append([x+7,166])
            lk=k
            for b in bu[:]:
                box(b[0],b[1],2,5,K)
                b[1]-=6
                if b[1]<14:bu.remove(b)
                else:box(b[0],b[1],2,5,(255,255,0))
            if len(al)<3+s//100 and randint(0,25)==0:
                al.append([randint(0,26)*14,14,randint(-1,1),randint(0,2)])
            for e in al[:]:
                if f%max(1,4-s//150):continue
                alien(e,K)
                e[1]+=2
                e[0]+=e[2]*2
                if e[0]<0 or e[0]>370:e[2]=-e[2]
                e[0]=max(0,min(370,e[0]))
                hit=0
                for b in bu[:]:
                    if e[0]-2<b[0]<e[0]+14 and e[1]<b[1]+5 and b[1]<e[1]+10:
                        box(b[0],b[1],2,5,K)
                        bu.remove(b)
                        hit=1
                if hit:
                    al.remove(e)
                    s+=10
                    hud(s,l)
                elif e[1]>160:
                    al.remove(e)
                    l-=1
                    hud(s,l)
                    ship(x,SC)
                else:alien(e,AC[e[3]])
            show_screen()
            for i in range(D):pass
            f+=1
        draw_string(110,80,"GAME OVER",(255,60,60),"large")
        draw_string(130,120,"OK: again",WH)
        show_screen()
        while getkey():pass
        k=0
        while k!=24 and k!=95 and k!=12:k=getkey()
        if k==12:return

main()
