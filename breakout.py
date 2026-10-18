from casioplot import *
from random import randint

PY=180
PW=40
BY=24
D=300
K=(0,0,0)
WH=(255,255,255)
RC=((220,40,40),(240,130,0),(220,190,0),(40,170,40),(0,160,200),(60,80,220))

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def hud(s,l,v):
    box(0,0,384,13,WH)
    draw_string(4,1,"Score "+str(s),K,"small")
    draw_string(160,1,"Level "+str(v),K,"small")
    draw_string(310,1,"Lives "+str(l),K,"small")

def hit(k,x,y):
    if y<BY or y>=BY+60 or (y-BY)%10>7:return -1
    if x%32==0 or x%32==31:return -1
    i=(y-BY)//10*12+x//32
    if k[i]:return i
    return -1

def wait():
    while getkey():pass
    k=0
    while k!=24 and k!=95 and k!=12:k=getkey()
    return k

def main():
    while True:
        s=0
        l=3
        v=1
        sp=3
        n=0
        px=172
        go=False
        bx=by=vx=vy=0
        clear_screen()
        box(0,13,384,1,K)
        hud(s,l,v)
        while True:
            if n==0:
                k=[1]*72
                n=72
                go=False
                bx=px+PW//2-2
                by=PY-4
                for i in range(72):
                    box(i%12*32+1,BY+i//12*10,30,8,RC[i//12])
            g=getkey()
            if g==12:return
            ox=px
            if g==23:px=max(0,px-6)
            if g==25:px=min(384-PW,px+6)
            ax=bx
            ay=by
            if not go:
                bx=px+PW//2-2
                by=PY-4
                if g==24 or g==95 or g==14:
                    go=True
                    vy=-sp
                    vx=2
                    if randint(0,1):vx=-2
            else:
                bx+=vx
                by+=vy
                if bx<0:
                    bx=0
                    vx=-vx
                if bx>380:
                    bx=380
                    vx=-vx
                if by<14:
                    by=14
                    vy=-vy
                h=0
                for x,y in ((bx,by),(bx+3,by),(bx,by+3),(bx+3,by+3)):
                    i=hit(k,x,y)
                    if i>=0:
                        k[i]=0
                        n-=1
                        h=1
                        s+=6-i//12
                        box(i%12*32+1,BY+i//12*10,30,8,WH)
                if h:
                    vy=-vy
                    hud(s,l,v)
                if vy>0 and by+3>=PY and by+3-vy<PY and bx+3>=px and bx<px+PW:
                    by=PY-4
                    vy=-vy
                    vx=(bx+2-px-PW//2)//4
                    if vx==0:vx=1-2*randint(0,1)
                    vx=max(-4,min(4,vx))
                if by>186:
                    box(ax,ay,4,4,WH)
                    l-=1
                    go=False
                    hud(s,l,v)
                    if l==0:break
                    bx=px+PW//2-2
                    by=PY-4
                    ax=bx
                    ay=by
                if n==0:
                    v+=1
                    sp=min(5,sp+1)
                    hud(s,l,v)
            box(ax,ay,4,4,WH)
            if px!=ox:box(ox,PY,PW,4,WH)
            box(px,PY,PW,4,K)
            if n:box(bx,by,4,4,(200,0,0))
            show_screen()
            for i in range(D):pass
        box(112,70,160,60,WH)
        draw_string(138,75,"GAME OVER",(255,0,0))
        draw_string(140,100,"OK: again",K)
        show_screen()
        if wait()==12:return

main()
