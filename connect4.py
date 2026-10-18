from casioplot import *
from random import randint
from math import sqrt

S=26
BX=12
BY=32
K=(0,0,0)
WH=(255,255,255)
BL=(30,80,200)
CO=(WH,(220,30,30),(240,200,0))
NM=("","Red","Yellow")
O=(3,2,4,1,5,0,6)
V=(0,1,2,3,2,1,0)
DP=(0,2,4,7)
KC={81:0,82:1,83:2,71:3,72:4,73:5,61:6}

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def disc(x,y,r,c):
    for d in range(-r,r+1):
        w=int(sqrt(r*r+r-d*d))
        for a in range(x-w,x+w+1):
            set_pixel(a,y+d,c)

def key():
    k=0
    while k==0:k=getkey()
    while getkey():pass
    return k

def at(c,r,p,s=10):
    disc(BX+13+c*S,BY+13+(5-r)*S,s,CO[p])

def txt(y,s,c=K):
    box(208,y,176,18,WH)
    draw_string(208,y,s,c)

def menu(t,o):
    clear_screen()
    draw_string(111,12,"CONNECT 4",CO[1],"large")
    draw_string(40,52,t,K)
    n=1
    while True:
        for i in range(len(o)):
            c=WH
            if i+1==n:c=CO[2]
            box(40,85+i*28,8,8,c)
            draw_string(56,80+i*28,str(i+1)+"  "+o[i],K)
        show_screen()
        k=key()
        if k==12:return 0
        if k==14 and n>1:n-=1
        if k==34 and n<len(o):n+=1
        if k==24 or k==95:return n
        if k>=81 and k<81+len(o):return k-80

def won(b,i,p):
    x=i%7
    y=i//7
    for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            a=x+dx*s
            c=y+dy*s
            while a>=0 and a<7 and c>=0 and c<6 and b[c*7+a]==p:
                n+=1
                a+=dx*s
                c+=dy*s
        if n>=4:return (dx,dy)
    return None

def ng(b,h,p,d,a,z,e):
    best=-999
    for c in O:
        r=h[c]
        if r<6:
            i=r*7+c
            b[i]=p
            h[c]=r+1
            if won(b,i,p):v=100+d
            elif d<=1:v=e+V[c]
            else:v=-ng(b,h,3-p,d-1,-z,-a,-e-V[c])
            b[i]=0
            h[c]=r
            if v>best:best=v
            if best>a:a=best
            if a>=z:break
    if best==-999:return 0
    return best

def bot(b,h,p,lv):
    f=[c for c in O if h[c]<6]
    for q in (p,3-p):
        for c in f:
            i=h[c]*7+c
            b[i]=q
            w=won(b,i,q)
            b[i]=0
            if w:return c
    if lv==1:return f[randint(0,len(f)-1)]
    best=-9999
    m=f[0]
    for c in f:
        r=h[c]
        b[r*7+c]=p
        h[c]=r+1
        v=-ng(b,h,3-p,DP[lv]-1,-9999,-best,-V[c])
        b[r*7+c]=0
        h[c]=r
        if v>best:
            best=v
            m=c
    return m

def score(m,sc):
    n=("Red","Yel")
    if m==2:n=("You","CPU")
    txt(100,n[0]+":"+str(sc[1])+" "+n[1]+":"+str(sc[2])+" D:"+str(sc[0]))

def play(m,lv,t,sc):
    b=[0]*42
    h=[0]*7
    clear_screen()
    box(BX,BY,S*7,S*6,BL)
    for c in range(7):
        for r in range(6):at(c,r,0)
    draw_string(208,8,"CONNECT 4",K)
    if m==2:draw_string(208,32,"vs CPU: "+("Easy","Medium","Hard")[lv-1],K,"small")
    else:draw_string(208,32,"Two players",K,"small")
    draw_string(208,140,"1-7 or arrows",K,"small")
    draw_string(208,155,"OK/EXE: drop",K,"small")
    score(m,sc)
    c=3
    for n in range(42):
        if m==2 and t==2:
            txt(60,"Thinking...")
            show_screen()
            c=bot(b,h,2,lv)
        else:
            if m==2:txt(60,"Your turn",CO[1])
            else:txt(60,NM[t]+" to play",CO[t])
            while True:
                disc(BX+13+c*S,17,10,CO[t])
                show_screen()
                g=key()
                if g==12:return -1
                disc(BX+13+c*S,17,10,WH)
                if g==23 and c>0:c-=1
                elif g==25 and c<6:c+=1
                elif g in KC:
                    c=KC[g]
                    if h[c]<6:break
                elif (g==24 or g==95 or g==34) and h[c]<6:break
        r=h[c]
        for q in range(5,r,-1):
            at(c,q,t)
            show_screen()
            for i in range(300):pass
            at(c,q,0)
        at(c,r,t)
        i=r*7+c
        b[i]=t
        h[c]=r+1
        w=won(b,i,t)
        if w:
            for s in (1,-1):
                x=c
                y=r
                while x>=0 and x<7 and y>=0 and y<6 and b[y*7+x]==t:
                    at(x,y,0,4)
                    x+=w[0]*s
                    y+=w[1]*s
            return t
        t=3-t
    return 0

def main():
    m=menu("Mode",("Two players","vs Computer"))
    if m==0:return
    lv=0
    if m==2:
        lv=menu("Level",("Easy","Medium","Hard"))
        if lv==0:return
    sc=[0,0,0]
    st=1
    while True:
        q=play(m,lv,st,sc)
        if q<0:return
        sc[q]+=1
        if m==2:r=("Draw!","You win!","CPU wins!")[q]
        else:r=("Draw!","Red wins!","Yellow wins!")[q]
        txt(60,r,(K,CO[1],(200,150,0))[q])
        score(m,sc)
        draw_string(208,172,"OK: play again",K,"small")
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=key()
        if k==12:return
        st=3-st

main()
