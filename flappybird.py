from casioplot import *
from random import randint

W=384
H=192
G=55

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            if a>=0 and a<W and b>=0 and b<H:
                set_pixel(a,b,c)

def hit(x,y,p):
    for q in p:
        if q[0]<x+8 and q[0]+18>x:
            if y<q[1] or y+8>q[1]+G:
                return True
    return False

def main():
    y=90
    v=0
    t=0
    score=0
    pipes=[[250,randint(45,110)],[380,randint(45,110)]]

    while True:
        k=getkey()

        if k==12:return

        if k==24 or k==95:
            v=-6

        if k==36:
            draw_string(165,85,"PAUSED",(0,0,0))
            show_screen()
            while True:
                k=getkey()
                if k==24 or k==95:break
                if k==12:return

        v+=1
        y+=v

        for p in pipes:
            p[0]-=3

        if pipes[0][0]<-20:
            pipes.pop(0)
            pipes.append([380,randint(45,110)])
            score+=1

        if y<0 or y>H-8 or hit(70,y,pipes):
            break

        clear_screen()

        box(70,y,8,8,(255,150,0))

        for p in pipes:
            box(p[0],0,18,p[1],(0,180,0))
            box(p[0],p[1]+G,18,H-p[1]-G,(0,180,0))

        draw_string(5,5,"Score:"+str(score),(0,0,0))
        show_screen()

        for i in range(1200):
            pass

    clear_screen()
    draw_string(145,70,"GAME OVER",(255,0,0))
    draw_string(150,90,"Score: "+str(score),(0,0,0))
    draw_string(120,115,"24/95 = Again",(0,0,0))
    show_screen()

    while True:
        k=getkey()
        if k==24 or k==95:
            main()
            return
        if k==12:return

main()
