import casioplot
from random import randint

W=38
H=19
S=10

def box(x,y,c):
    x*=S;y*=S
    for a in range(8):
        for b in range(8):
            casioplot.set_pixel(x+a,y+b,c)

def food(s):
    while True:
        p=(randint(0,W-1),randint(0,H-1))
        if p not in s:return p

def key():
    while casioplot.getkey():pass
    k=None
    while not k:k=casioplot.getkey()
    return k

def menu():
    casioplot.clear_screen()
    casioplot.draw_string(150,30,"SNAKE",(0,160,0),"large")
    casioplot.draw_string(100,80,"1  Easy",(0,0,0))
    casioplot.draw_string(100,105,"2  Hard",(0,0,0))
    casioplot.draw_string(100,145,"Arrows steer, eat the red food",(0,0,0),"small")
    casioplot.show_screen()
    while True:
        k=key()
        if k==81:return 7500
        if k==82:return 2500
        if k==12:return 0

def main():
    while True:
        dl=menu()
        if dl==0:return
        s=[(19,9),(18,9),(17,9)]
        d=(1,0)
        f=food(s)
        score=0

        while True:
            k=casioplot.getkey()

            if k==12:return
            if k==14 and d!=(0,1):d=(0,-1)
            elif k==34 and d!=(0,-1):d=(0,1)
            elif k==23 and d!=(1,0):d=(-1,0)
            elif k==25 and d!=(-1,0):d=(1,0)

            h=(s[0][0]+d[0],s[0][1]+d[1])

            if h[0]<0 or h[0]>=W or h[1]<0 or h[1]>=H or h in s:
                break

            s.insert(0,h)

            if h==f:
                score+=1
                f=food(s)
            else:
                s.pop()

            casioplot.clear_screen()

            box(f[0],f[1],(255,0,0))

            for p in s:
                box(p[0],p[1],(0,255,0))

            casioplot.draw_string(300,2,"Score:"+str(score),(0,0,255))
            casioplot.show_screen()

            for i in range(dl):
                pass

        casioplot.clear_screen()
        casioplot.draw_string(145,75,"GAME OVER",(255,0,0))
        casioplot.draw_string(145,95,"Score: "+str(score),(0,0,0))
        casioplot.draw_string(145,125,"OK: menu",(0,0,0),"small")
        casioplot.show_screen()

        if key()==12:return

main()
