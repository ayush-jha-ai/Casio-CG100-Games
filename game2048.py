from casioplot import *
from random import randint

X=150
Y=6
S=44
C=[(205,193,180),(238,228,218),(237,224,200),(242,177,121),(245,149,99),(246,124,95),(246,94,59),(237,207,114),(237,204,97),(237,200,80),(237,197,63),(237,194,46),(60,58,50)]

def box(x,y,w,h,c):
    for a in range(x,x+w):
        for b in range(y,y+h):
            set_pixel(a,b,c)

def new(b):
    e=[]
    for i in range(16):
        if b[i]==0:e.append(i)
    if e:
        p=e[randint(0,len(e)-1)]
        if randint(1,10)==1:b[p]=4
        else:b[p]=2

def merge(a):
    n=[]
    for x in a:
        if x:n.append(x)
    r=[]
    s=0
    i=0
    while i<len(n):
        if i+1<len(n) and n[i]==n[i+1]:
            r.append(n[i]*2)
            s+=n[i]*2
            i+=2
        else:
            r.append(n[i])
            i+=1
    while len(r)<4:r.append(0)
    return r,s

def move(b,d):
    o=b[:]
    s=0
    for n in range(4):
        if d==0:ids=[n,n+4,n+8,n+12]
        elif d==1:ids=[n+12,n+8,n+4,n]
        elif d==2:ids=[n*4,n*4+1,n*4+2,n*4+3]
        else:ids=[n*4+3,n*4+2,n*4+1,n*4]
        a=[]
        for i in ids:a.append(b[i])
        a,t=merge(a)
        s+=t
        for i in range(4):b[ids[i]]=a[i]
    return b!=o,s

def over(b):
    for x in b:
        if x==0:return False
    for y in range(4):
        for x in range(4):
            i=y*4+x
            if x<3 and b[i]==b[i+1]:return False
            if y<3 and b[i]==b[i+4]:return False
    return True

def tile(i,v):
    x=X+4+i%4*S
    y=Y+4+i//4*S
    e=0
    n=v
    while n>1:
        n//=2
        e+=1
    box(x,y,S-4,S-4,C[min(e,12)])
    if v:
        s=str(v)
        c=(255,255,255)
        if v<8:c=(119,110,101)
        if v<1000:draw_string(x+(S-4-12*len(s))//2,y+11,s,c)
        else:draw_string(x+(S-4-8*len(s))//2,y+15,s,c,"small")

def draw(b,o,sc):
    for i in range(16):
        if b[i]!=o[i]:
            tile(i,b[i])
            o[i]=b[i]
    box(8,74,110,18,(255,255,255))
    draw_string(8,74,str(sc),(0,0,0))
    if 2048 in b:draw_string(8,100,"YOU WIN!",(0,160,0))
    show_screen()

def main():
    while True:
        b=[0]*16
        o=[-1]*16
        sc=0
        new(b)
        new(b)
        clear_screen()
        box(X,Y,S*4+4,S*4+4,(187,173,160))
        draw_string(8,8,"2048",(119,110,101),"large")
        draw_string(8,54,"Score",(0,0,0))
        draw(b,o,sc)
        while not over(b):
            k=getkey()
            if k==12:return
            d=-1
            if k==14:d=0
            elif k==34:d=1
            elif k==23:d=2
            elif k==25:d=3
            if d>=0:
                c,s=move(b,d)
                if c:
                    sc+=s
                    new(b)
                    draw(b,o,sc)
                while getkey():pass
        draw_string(8,125,"GAME OVER",(255,0,0))
        draw_string(8,150,"OK: again",(0,0,0),"small")
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=getkey()
        if k==12:return
        while getkey():pass

main()
