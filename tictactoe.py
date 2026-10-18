from casioplot import *
from random import randint

E=2
O=0
X=1
S=56
K=(0,0,0)
WH=(255,255,255)
CO=((0,90,255),(255,140,0))
LV=("Two players","vs CPU: Easy","vs CPU: Medium","vs CPU: Impossible")
w=((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))

def box(x,y,a,b,c):
    for i in range(x,x+a):
        for j in range(y,y+b):
            set_pixel(i,j,c)

def xy(i):
    return 14+(i-1)%3*S,12+(9-i)//3*S

def mark(i,v):
    x,y=xy(i)
    for j in range(34):
        if v==X:
            box(x+11+j,y+11+j,3,1,CO[X])
            box(x+43-j,y+11+j,3,1,CO[X])
    if v==O:
        for a in range(-18,19):
            for b in range(-18,19):
                if 196<=a*a+b*b<=324:set_pixel(x+28+a,y+28+b,CO[O])

def txt(y,s,c=K):
    box(196,y,188,18,WH)
    draw_string(196,y,s,c)

def key():
    k=0
    while k==0:k=getkey()
    while getkey():pass
    return k


def win(b):
    for a,c,d in w:
        if b[a]!=E and b[a]==b[c]==b[d]:return a
    return 0

def mm(b,p,d,a,z):
    if win(b):return d-10
    if E not in b[1:]:return 0
    for i in range(1,10):
        if b[i]==E:
            b[i]=p
            s=-mm(b,1-p,d+1,-z,-a)
            b[i]=E
            if s>a:a=s
            if a>=z:break
    return a

def bot(b,d):
    e=[i for i in range(1,10) if b[i]==E]
    if d==1:return e[randint(0,len(e)-1)]
    for v in (X,O):
        for i in e:
            b[i]=v
            q=win(b)
            b[i]=E
            if q:return i
    if b[5]==E:return 5
    if d==2:return e[randint(0,len(e)-1)]
    m=e[0]
    a=-99
    for i in e:
        b[i]=X
        s=-mm(b,O,1,-99,-a)
        b[i]=E
        if s>a:
            a=s
            m=i
    return m

def score(d,sc):
    n=("O","X")
    if d:n=("You","CPU")
    txt(90,n[0]+":"+str(sc[O])+" "+n[1]+":"+str(sc[X])+" D:"+str(sc[E]))
    return n

def play(d,t,sc):
    b=[E]*10
    clear_screen()
    for n in (1,2):
        box(13+n*S,12,3,S*3,K)
        box(14,11+n*S,S*3,3,K)
    draw_string(196,8,"TIC TAC TOE",K)
    draw_string(196,32,LV[d],K,"small")
    draw_string(196,130,"Keys 1-9 match",K,"small")
    draw_string(196,144,"the board",K,"small")
    while True:
        n=score(d,sc)
        if d and t==X:
            txt(55,"Thinking...")
            show_screen()
            k=bot(b,d)
        else:
            txt(55,n[t]+" to play",CO[t])
            show_screen()
            k=0
            while k==0:
                g=key()
                if g==12:return -1
                if g>60 and g<84 and 0<g%10<4 and b[(8-g//10)*3+g%10]==E:k=(8-g//10)*3+g%10
        b[k]=t
        mark(k,t)
        q=win(b)
        if q:return t
        if E not in b[1:]:return E
        t=1-t

def main():
    clear_screen()
    draw_string(93,12,"TIC TAC TOE",CO[O],"large")
    for i in range(4):draw_string(40,60+i*28,str(i+1)+"  "+LV[i],K)
    show_screen()
    d=0
    while d<81 or d>84:
        d=key()
        if d==12:return
    d-=81
    sc=[0,0,0]
    st=O
    while True:
        q=play(d,st,sc)
        if q<0:return
        sc[q]+=1
        txt(55,(("O wins!","X wins!"),("You win!","CPU wins!"))[d>0][q] if q<2 else "Draw!",(CO[O],CO[X],K)[q])
        score(d,sc)
        draw_string(196,165,"OK: play again",K,"small")
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=key()
        if k==12:return
        st=1-st

main()
