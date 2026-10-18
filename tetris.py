from casioplot import *
from random import randint

BX=147
BY=6
D=200
K=(0,0,0)
WH=(255,255,255)
CL=((0,190,220),(230,200,0),(160,40,200),(40,180,40),(220,40,40),(40,70,220),(240,140,0))
P=((4,((0,1),(1,1),(2,1),(3,1))),(2,((0,0),(1,0),(0,1),(1,1))),
(3,((1,0),(0,1),(1,1),(2,1))),(3,((1,0),(2,0),(0,1),(1,1))),
(3,((0,0),(1,0),(1,1),(2,1))),(3,((0,0),(0,1),(1,1),(2,1))),
(3,((2,0),(0,1),(1,1),(2,1))))

def cells(p,r):
    n,c=P[p]
    for i in range(r):c=[(n-1-b,a) for a,b in c]
    return c

g=bytearray(200)

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def cell(x,y,c):
    box(BX+x*9,BY+y*9,8,8,c)

def fits(p,r,x,y):
    for a,b in cells(p,r):
        a+=x
        b+=y
        if a<0 or a>9 or b>19:return False
        if b>=0 and g[b*10+a]:return False
    return True

def piece(p,r,x,y,c):
    for a,b in cells(p,r):
        if y+b>=0:cell(x+a,y+b,c)

def stat(y,v):
    box(8,y,130,17,WH)
    draw_string(8,y,str(v),K)

def nextp(p):
    box(260,36,36,36,WH)
    for a,b in cells(p,0):box(260+a*9,36+b*9,8,8,CL[p])

def board():
    for i in range(200):
        c=WH
        if g[i]:c=CL[g[i]-1]
        cell(i%10,i//10,c)

def main():
    while True:
        for i in range(200):g[i]=0
        clear_screen()
        box(BX-2,BY,94,182,K)
        box(BX,BY,90,180,WH)
        draw_string(8,6,"TETRIS",(160,40,200),"large")
        for i in range(2):draw_string(8,46+44*i,("Score","Lines")[i],K,"small")
        s=0
        ln=0
        stat(58,0)
        stat(102,0)
        p=randint(0,6)
        nx=randint(0,6)
        nextp(nx)
        r=0
        x=3
        y=0
        t=0
        l=0
        piece(p,r,x,y,CL[p])
        while True:
            k=getkey()
            if k==12:return
            o=(r,x,y)
            dn=False
            if (k==23 or k==25) and k!=l and fits(p,r,x+k-24,y):x+=k-24
            if k==14 and l!=14:
                q=(r+1)%4
                for d in (0,-1,1):
                    if fits(p,q,x+d,y):
                        r=q
                        x+=d
                        break
            if (k==24 or k==95) and k!=l:
                while fits(p,r,x,y+1):y+=1
                dn=True
            t+=1
            if k==34 or t>=max(2,20-ln//5):
                t=0
                if fits(p,r,x,y+1):y+=1
                else:dn=True
            if o!=(r,x,y):
                piece(p,o[0],o[1],o[2],WH)
                piece(p,r,x,y,CL[p])
            if dn and not fits(p,r,x,y+1):
                for a,b in cells(p,r):
                    if y+b>=0:g[(y+b)*10+x+a]=p+1
                f=[i for i in range(20) if all(g[i*10:i*10+10])]
                if f:
                    for i in f:
                        for j in range(i*10+9,9,-1):g[j]=g[j-10]
                        for j in range(10):g[j]=0
                    board()
                    ln+=len(f)
                    s+=100*len(f)*len(f)*(1+ln//10)
                    stat(102,ln)
                stat(58,s)
                p=nx
                nx=randint(0,6)
                nextp(nx)
                r=0
                x=3
                y=0
                t=0
                if not fits(p,r,x,y):break
                piece(p,r,x,y,CL[p])
            l=k
            show_screen()
            for i in range(D):pass
        draw_string(250,150,"GAME OVER",(220,0,0))
        draw_string(250,170,"OK: again",K,"small")
        show_screen()
        while getkey():pass
        k=0
        while k!=24 and k!=95 and k!=12:k=getkey()
        if k==12:return

main()
