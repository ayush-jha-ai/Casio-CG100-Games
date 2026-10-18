from casioplot import *
from random import randint

W=384
H=192
BH=24
G=8

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            if a>=0 and a<W and b>=0 and b<H:
                set_pixel(a,b,c)

def num(x,y,w,h,v):
    s=str(v)
    if len(s)<4:draw_string(x+(w-12*len(s))//2,y+(h-17)//2,s,(0,0,0))
    else:draw_string(x+(w-8*len(s))//2,y+(h-10)//2,s,(0,0,0),"small")

def wall(v):
    a=[2,4,8,16,32,64,128,256]
    r=randint(1,6)
    a[r]=v
    return [380,a]

def drawbird(y,v):
    box(60,y,36,18,(255,180,0))
    num(60,y,36,18,v)

def drawwall(x,a):
    for i in range(8):
        y=i*BH
        box(x,y,38,BH-2,(180,180,180))
        num(x,y,38,BH-2,a[i])

def main():
    while True:
        y=85
        vel=0
        value=2
        x,a=wall(value)
        passed=False

        while True:
            k=getkey()

            if k==12:return
            if k==24 or k==95:vel=-6

            vel+=1
            y+=vel
            x-=3

            if y<0 or y>H-18:
                break

            if x<96 and x+38>60 and not passed:
                n=(y+9)//BH

                if n<0 or n>7 or a[n]!=value:
                    break

                value*=2
                passed=True

                if value>=2048:
                    clear_screen()
                    draw_string(145,75,"YOU WIN!",(0,0,0))
                    draw_string(140,100,"2048!",(0,0,0))
                    show_screen()
                    while getkey():pass
                    while getkey()==0:pass
                    return

            if x<-40:
                x,a=wall(value)
                passed=False

            clear_screen()
            draw_string(5,5,"Value:"+str(value),(0,0,0))
            drawbird(y,value)
            drawwall(x,a)
            show_screen()

            for i in range(1200):
                pass

        clear_screen()
        draw_string(145,70,"GAME OVER",(255,0,0))
        draw_string(140,95,"Value: "+str(value),(0,0,0))
        draw_string(139,120,"OK = Again",(0,0,0))
        show_screen()

        while getkey():pass
        while True:
            k=getkey()
            if k==24 or k==95:break
            if k==12:return

main()
