from casioplot import *
from random import randint

E=2
O=0
X=1
S=56
L=14
T=12
K=(0,0,0)
WH=(255,255,255)
CO=((0,90,255),(255,140,0))

w=((1,2,3),(4,5,6),(7,8,9),
(1,4,7),(2,5,8),(3,6,9),
(1,5,9),(3,5,7))

def box(x,y,a,b,c):
    for i in range(x,x+a):
        for j in range(y,y+b):
            set_pixel(i,j,c)

def xy(i):
    return L+(i-1)%3*S,T+(9-i)//3*S

def grid():
    for n in (1,2):
        box(L+n*S-1,T,3,S*3,K)
        box(L,T+n*S-1,S*3,3,K)

def mark(i,v):
    x,y=xy(i)
    if v==X:
        for j in range(34):
            for t in range(3):
                set_pixel(x+11+j+t,y+11+j,CO[X])
                set_pixel(x+45-j-t,y+11+j,CO[X])
    else:
        for a in range(-18,19):
            for b in range(-18,19):
                d=a*a+b*b
                if d>=196 and d<=324:set_pixel(x+28+a,y+28+b,CO[O])

def cur(i,c):
    x,y=xy(i)
    box(x+4,y+4,S-8,2,c)
    box(x+4,y+S-6,S-8,2,c)
    box(x+4,y+4,2,S-8,c)
    box(x+S-6,y+4,2,S-8,c)

def line(t):
    x1,y1=xy(t[0])
    x2,y2=xy(t[2])
    for s in range(41):
        box(x1+26+(x2-x1)*s//40,y1+26+(y2-y1)*s//40,5,5,(220,0,0))

def txt(y,s,c=K):
    box(196,y,188,18,WH)
    draw_string(196,y,s,c)

def key():
    k=0
    while k==0:k=getkey()
    while getkey():pass
    return k

def menu(t,o):
    clear_screen()
    draw_string(93,12,"TIC TAC TOE",CO[O],"large")
    draw_string(40,52,t,K)
    n=1
    while True:
        for i in range(len(o)):
            c=WH
            if i+1==n:c=CO[X]
            box(40,85+i*28,8,8,c)
            draw_string(56,80+i*28,str(i+1)+"  "+o[i],K)
        show_screen()
        k=key()
        if k==12:return 0
        if k==14 and n>1:n-=1
        if k==34 and n<len(o):n+=1
        if k==24 or k==95:return n
        if k>=81 and k<81+len(o):return k-80

def win(b):
    for a,c,d in w:
        if b[a]!=E and b[a]==b[c] and b[a]==b[d]:
            return b[a]
    return E

def full(b):
    for i in range(1,10):
        if b[i]==E:return False
    return True

def winning(b,v):
    for i in range(1,10):
        if b[i]==E:
            b[i]=v
            z=win(b)
            b[i]=E
            if z==v:return i
    return 0

def rnd(b):
    n=0
    for i in range(1,10):
        if b[i]==E:n+=1
    r=randint(1,n)
    n=0
    for i in range(1,10):
        if b[i]==E:
            n+=1
            if n==r:return i

def mm(b,maxi,d,a,z):
    q=win(b)
    if q==X:return 10-d
    if q==O:return d-10
    if full(b):return 0

    if maxi:
        best=-100
        for i in range(1,10):
            if b[i]==E:
                b[i]=X
                s=mm(b,False,d+1,a,z)
                b[i]=E
                if s>best:best=s
                if best>a:a=best
                if z<=a:break
        return best
    else:
        best=100
        for i in range(1,10):
            if b[i]==E:
                b[i]=O
                s=mm(b,True,d+1,a,z)
                b[i]=E
                if s<best:best=s
                if best<z:z=best
                if z<=a:break
        return best

def bot(b,d):
    if d==1:return rnd(b)

    m=winning(b,X)
    if m:return m

    m=winning(b,O)
    if m:return m

    if d==2:
        if b[5]==E:return 5
        return rnd(b)

    if b[5]==E:return 5

    best=-100
    move=0
    a=-100

    for i in range(1,10):
        if b[i]==E:
            b[i]=X
            s=mm(b,False,0,a,100)
            b[i]=E
            if s>best:
                best=s
                move=i
            if best>a:a=best
    return move

def score(m,sc):
    n=("O","X")
    if m==2:n=("You","CPU")
    txt(90,n[0]+":"+str(sc[O])+" "+n[1]+":"+str(sc[X])+" D:"+str(sc[E]))

def play(m,d,t,sc):
    b=[E]*10
    clear_screen()
    grid()
    draw_string(196,8,"TIC TAC TOE",K)
    if m==2:draw_string(196,32,"vs CPU: "+("Easy","Medium","Impossible")[d-1],K,"small")
    else:draw_string(196,32,"Two players",K,"small")
    draw_string(196,130,"1-9 or arrows",K,"small")
    draw_string(196,145,"OK/EXE: place",K,"small")
    score(m,sc)
    c=5
    while True:
        if m==2 and t==X:
            txt(55,"Thinking...")
            show_screen()
            k=bot(b,d)
        else:
            if m==2:txt(55,"Your turn",CO[O])
            else:txt(55,"OX"[t]+" to play",CO[t])
            cur(c,(0,180,0))
            show_screen()
            k=0
            while k==0:
                g=key()
                if g==12:return -1
                n=c
                r=(9-c)//3
                q=(c-1)%3
                if g==14 and r>0:n=c+3
                elif g==34 and r<2:n=c-3
                elif g==23 and q>0:n=c-1
                elif g==25 and q<2:n=c+1
                elif g==24 or g==95:
                    if b[c]==E:k=c
                elif g//10>5 and g//10<9 and g%10>0 and g%10<4:
                    n=(8-g//10)*3+g%10
                    if b[n]==E:k=n
                if n!=c:
                    cur(c,WH)
                    c=n
                    cur(c,(0,180,0))
                    show_screen()
            cur(c,WH)
        b[k]=t
        mark(k,t)
        q=win(b)
        if q!=E or full(b):
            for l in w:
                if q!=E and b[l[0]]==q and b[l[1]]==q and b[l[2]]==q:line(l)
            return q
        t=1-t

def main():
    m=menu("Mode",("Two players","vs Computer"))
    if m==0:return
    d=0
    if m==2:
        d=menu("Level",("Easy","Medium","Impossible"))
        if d==0:return
    sc=[0,0,0]
    st=O
    while True:
        q=play(m,d,st,sc)
        if q<0:return
        sc[q]+=1
        if m==2:r=("You win!","CPU wins!","Draw!")[q]
        else:r=("O wins!","X wins!","Draw!")[q]
        txt(55,r,(CO[O],CO[X],K)[q])
        score(m,sc)
        draw_string(196,165,"OK: play again",K,"small")
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=key()
        if k==12:return
        st=1-st

main()
