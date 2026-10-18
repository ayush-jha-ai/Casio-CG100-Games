import casioplot
from random import randint

N=4
S=38
X=110
Y=18

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
    score=0
    i=0
    while i<len(n):
        if i+1<len(n) and n[i]==n[i+1]:
            v=n[i]*2
            r.append(v)
            score+=v
            i+=2
        else:
            r.append(n[i])
            i+=1
    while len(r)<4:r.append(0)
    return r,score

def move(b,d):
    old=b[:]
    score=0

    for n in range(4):
        if d==0:
            ids=[n,n+4,n+8,n+12]
        elif d==1:
            ids=[n+12,n+8,n+4,n]
        elif d==2:
            ids=[n*4,n*4+1,n*4+2,n*4+3]
        else:
            ids=[n*4+3,n*4+2,n*4+1,n*4]

        a=[]
        for i in ids:a.append(b[i])

        a,s=merge(a)
        score+=s

        for i in range(4):
            b[ids[i]]=a[i]

    return b!=old,score

def over(b):
    for x in b:
        if x==0:return False

    for y in range(4):
        for x in range(4):
            i=y*4+x
            if x<3 and b[i]==b[i+1]:return False
            if y<3 and b[i]==b[i+4]:return False

    return True

def draw(b,score):
    casioplot.clear_screen()

    casioplot.draw_string(10,10,"2048",(0,0,0))
    casioplot.draw_string(10,30,"Score:",(0,0,0))
    casioplot.draw_string(10,45,str(score),(0,0,0))

    for y in range(5):
        for x in range(153):
            casioplot.set_pixel(X+x,Y+y*38,(0,0,0))

    for x in range(5):
        for y in range(153):
            casioplot.set_pixel(X+x*38,Y+y,(0,0,0))

    for y in range(4):
        for x in range(4):
            v=b[y*4+x]
            if v:
                px=X+x*38+8
                py=Y+y*38+12

                if v<10:px+=7
                elif v<100:px+=3

                casioplot.draw_string(px,py,str(v),(0,0,0))

    casioplot.show_screen()

def main():
    b=[0]*16
    score=0

    new(b)
    new(b)
    draw(b,score)

    while True:
        k=str(casioplot.getkey())
        d=-1

        if k=="14":d=0
        elif k=="34":d=1
        elif k=="23":d=2
        elif k=="25":d=3
        elif k=="12":return

        if d>=0:
            changed,s=move(b,d)

            if changed:
                score+=s
                new(b)
                draw(b,score)

                if over(b):break

    casioplot.clear_screen()
    casioplot.draw_string(145,65,"GAME OVER",(255,0,0))
    casioplot.draw_string(145,90,"Score: "+str(score),(0,0,0))
    casioplot.show_screen()

    while casioplot.getkey()==0:
        pass

main()
