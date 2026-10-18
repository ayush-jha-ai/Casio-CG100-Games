from casioplot import *
from math import sqrt

S=26
K=(0,0,0)
WH=(255,255,255)
CO=(WH,(220,30,30),(240,200,0))
O=(3,2,4,1,5,0,6)
V=(0,1,2,3,2,1,0)
DP=(0,2,4,7)
LV=("Two players","vs CPU: Easy","vs CPU: Medium","vs CPU: Hard")
NK=(61,71,72,73,81,82,83)

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def disc(x,y,c):
    for d in range(-10,11):
        w=int(sqrt(110-d*d))
        box(x-w,y+d,2*w+1,1,c)

def key():
    k=0
    while not k:k=getkey()
    while getkey():pass
    return int(k)

def txt(y,s,c=K):
    box(208,y,176,18,WH)
    draw_string(208,y,s,c)

def score(lv,sc):
    n=("Red","Yel")
    if lv:n=("You","CPU")
    txt(100,n[0]+":"+str(sc[1])+" "+n[1]+":"+str(sc[2])+" D:"+str(sc[0]))

def won(b,i,p):
    for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            a=i%7+dx*s
            c=i//7+dy*s
            while 0<=a<7 and 0<=c<6 and b[c*7+a]==p:
                n+=1
                a+=dx*s
                c+=dy*s
        if n>3:return 1
    return 0

def ng(b,h,p,d,a,z,e):
    best=-999
    for c in O:
        r=h[c]
        if r<6:
            i=r*7+c
            b[i]=p
            h[c]=r+1
            if won(b,i,p):v=100+d
            elif d<2:v=e+V[c]
            else:v=-ng(b,h,3-p,d-1,-z,-a,-e-V[c])
            b[i]=0
            h[c]=r
            if v>best:best=v
            if best>a:a=best
            if a>=z:break
    if best==-999:return 0
    return best

def bot(b,h,lv):
    best=-9999
    m=3
    for c in O:
        if h[c]>5:continue
        i=h[c]*7+c
        b[i]=2
        h[c]+=1
        v=100
        if not won(b,i,2):v=-ng(b,h,1,DP[lv]-1,-9999,-best,-V[c])
        h[c]-=1
        b[i]=0
        if v>best:
            best=v
            m=c
    return m

def play(lv,t,sc):
    b=[0]*42
    h=[0]*7
    clear_screen()
    box(12,32,S*7,S*6,(30,80,200))
    for i in range(42):disc(25+i%7*S,45+i//7*S,WH)
    draw_string(208,8,"CONNECT 4",K)
    draw_string(208,32,LV[lv],K,"small")
    c=3
    for n in range(42):
        score(lv,sc)
        if lv and t==2:
            txt(60,"Thinking...")
            show_screen()
            c=bot(b,h,lv)
        else:
            box(208,60,176,18,WH)
            while True:
                disc(25+c*S,17,CO[t])
                show_screen()
                g=key()
                if g==12:return -1
                disc(25+c*S,17,WH)
                if g==23 and c>0:c-=1
                if g==25 and c<6:c+=1
                if g in NK:c=(8-g//10)*3+g%10-1
                if (g in NK or g in (24,95,34)) and h[c]<6:break
        r=h[c]
        disc(25+c*S,45+(5-r)*S,CO[t])
        b[r*7+c]=t
        h[c]=r+1
        if won(b,r*7+c,t):return t
        t=3-t
    return 0

def main():
    clear_screen()
    draw_string(111,12,"CONNECT 4",CO[1],"large")
    for i in range(4):draw_string(40,60+i*28,str(i+1)+"  "+LV[i],K)
    show_screen()
    lv=0
    while lv not in (81,82,83,71):
        lv=key()
        if lv==12:return
    lv=(81,82,83,71).index(lv)
    sc=[0,0,0]
    st=1
    while True:
        q=play(lv,st,sc)
        if q<0:return
        sc[q]+=1
        txt(60,(("Draw!","Red wins!","Yellow wins!"),("Draw!","You win!","CPU wins!"))[lv>0][q],(K,CO[1],(200,150,0))[q])
        score(lv,sc)
        draw_string(208,172,"OK: play again",K,"small")
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=key()
        if k==12:return
        st=3-st

main()
