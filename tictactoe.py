from turtle import *
from random import randint

E=2
O=0
X=1

p=[[0,0],[-100,-60],[-5,-60],[85,-60],
[-100,-5],[-5,-5],[85,-5],
[-100,45],[-5,45],[85,45]]

w=((1,2,3),(4,5,6),(7,8,9),
(1,4,7),(2,5,8),(3,6,9),
(1,5,9),(3,5,7))

def grid():
    for x in (-50,50):
        penup();goto(x,75);pendown();goto(x,-75)
    for y in (-25,25):
        penup();goto(-125,y);pendown();goto(125,y)
    penup()

def mark(k,v):
    x,y=p[k]
    penup();goto(x,y);pendown()
    if v==X:
        pencolor("orange")
        goto(x+10,y+10)
        penup();goto(x,y+10);pendown();goto(x+10,y)
    else:
        pencolor("blue")
        goto(x+10,y);goto(x+10,y+10)
        goto(x,y+10);goto(x,y)
    penup()

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

def getmove(b):
    while True:
        k=int(input("Position: "))
        if k>=1 and k<=9 and b[k]==E:
            return k
        print("Try again")

def result(v,mode):
    clear()
    pencolor("black")
    penup();goto(-80,0);pendown()
    if mode==2:
        if v==O:write("YOU WON!")
        elif v==X:write("YOU LOST!")
        else:write("DRAW!")
    else:
        if v==O:write("NOUGHTS WIN!")
        elif v==X:write("CROSSES WIN!")
        else:write("DRAW!")
    penup()

def main():
    b=[E]*10
    turn=O

    speed(2)
    width(3)
    hideturtle()

    print("TIC TAC TOE")
    print("1 Two Players")
    print("2 Computer")
    mode=int(input("Mode: "))

    d=0
    if mode==2:
        print("1 Easy")
        print("2 Medium")
        print("3 Impossible")
        d=int(input("Level: "))

    grid()

    while True:
        print("7 8 9")
        print("4 5 6")
        print("1 2 3")

        if mode==2 and turn==X:
            print("Computer...")
            k=bot(b,d)
            print("Computer:",k)
        else:
            k=getmove(b)

        b[k]=turn
        mark(k,turn)

        q=win(b)

        if q!=E:
            result(q,mode)
            break

        if full(b):
            result(E,mode)
            break

        if turn==O:turn=X
        else:turn=O

    input()

main()
