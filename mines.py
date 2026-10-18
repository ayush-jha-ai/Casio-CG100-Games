from casioplot import *
from random import randint

C=16
R=8
N=20
S=22
X=16
Y=16
K=(0,0,0)
WH=(255,255,255)
CV=(150,160,175)
OP=(228,228,228)
NC=((0,0,0),(0,0,230),(0,130,0),(220,0,0),(0,0,120),(130,0,0),(0,130,130),(0,0,0),(110,110,110))

m=[0]*(C*R)
n=[0]*(C*R)
s=[0]*(C*R)

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def key():
    k=0
    while not k:k=getkey()
    while getkey():pass
    return int(k)

def nb(i):
    x=i%C
    y=i//C
    r=[]
    for b in (-1,0,1):
        for a in (-1,0,1):
            if (a or b) and x+a>=0 and x+a<C and y+b>=0 and y+b<R:
                r.append(i+b*C+a)
    return r

def cell(i,bg=OP):
    x=X+i%C*S
    y=Y+i//C*S
    if s[i]==1:
        box(x,y,S-1,S-1,bg)
        if m[i]:box(x+5,y+5,11,11,K)
        elif n[i]:draw_string(x+5,y+2,str(n[i]),NC[n[i]])
    else:
        box(x,y,S-1,S-1,CV)
        if s[i]==2:
            box(x+12,y+4,2,13,K)
            box(x+6,y+4,6,6,(220,0,0))

def cur(i):
    x=X+i%C*S
    y=Y+i//C*S
    c=(255,200,0)
    box(x,y,S-1,2,c)
    box(x,y+S-3,S-1,2,c)
    box(x,y,2,S-1,c)
    box(x+S-3,y,2,S-1,c)

def hud(t,c=K):
    box(0,0,384,15,WH)
    draw_string(X,2,t,c,"small")
    draw_string(250,2,"OK open  EXE flag",K,"small")

def lay(c):
    a=nb(c)+[c]
    k=0
    while k<N:
        i=randint(0,C*R-1)
        if not m[i] and i not in a:
            m[i]=1
            k+=1
    for i in range(C*R):
        n[i]=0
        for j in nb(i):n[i]+=m[j]

def flood(i):
    o=0
    st=[i]
    while st:
        j=st.pop()
        if s[j]!=0:continue
        s[j]=1
        o+=1
        cell(j)
        if n[j]==0 and not m[j]:
            for q in nb(j):
                if s[q]==0:st.append(q)
    return o

def main():
    while True:
        for i in range(C*R):
            m[i]=0
            n[i]=0
            s[i]=0
        clear_screen()
        for i in range(C*R):cell(i)
        c=C*(R//2)+C//2
        f=0
        o=0
        first=True
        end=0
        hud("Mines left: "+str(N))
        while end==0:
            cur(c)
            show_screen()
            k=key()
            if k==12:return
            p=c
            if k==14 and c>=C:c-=C
            elif k==34 and c<C*(R-1):c+=C
            elif k==23 and c%C>0:c-=1
            elif k==25 and c%C<C-1:c+=1
            elif k==95 and s[c]!=1:
                s[c]=2-s[c]
                f+=1 if s[c] else -1
                hud("Mines left: "+str(N-f))
            elif k==24:
                if first:
                    lay(c)
                    first=False
                t=[]
                if s[c]==0:t=[c]
                elif s[c]==1 and n[c]:
                    g=0
                    for q in nb(c):
                        if s[q]==2:g+=1
                    if g==n[c]:t=nb(c)
                for q in t:
                    if s[q]!=0:continue
                    if m[q]:
                        end=q+1
                    else:o+=flood(q)
                if end==0 and o==C*R-N:end=-1
            cell(p)
        for i in range(C*R):
            if m[i] and s[i]!=2:
                s[i]=1+(end<0)
                cell(i)
        if end>0:
            cell(end-1,(230,60,60))
            hud("BOOM!  OK: again",(220,0,0))
        else:hud("CLEARED!  OK: again",(0,150,0))
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=key()
        if k==12:return

main()
