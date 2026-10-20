from spacelib import *
import spacelib as L

def main():
    while True:
        clear_screen()
        box(0,0,384,192,K)
        draw_string(80,30,"SPACE SHOOTER",SC,"large")
        draw_string(60,75,"Left/Right: move   OK: fire",WH,"small")
        draw_string(60,95,"Shoot the aliens before they",WH,"small")
        draw_string(60,107,"cross the red line at the bottom",WH,"small")
        draw_string(60,127,"Best "+str(L.best),WH,"small")
        draw_string(60,150,"OK: start",(255,255,0))
        show_screen()
        if key()==12:return
        box(0,0,384,192,K)
        for i in range(50):
            set_pixel(randint(0,383),randint(14,185),(randint(90,255),)*3)
        box(0,187,384,1,RD)
        s=0
        l=3
        w=1
        n=0
        x=180
        bu=[]
        al=[]
        bo=[]
        ex=[]
        lk=0
        f=0
        hud(s,l,w)
        ship(x,172,SC)
        while l>0:
            k=getkey()
            if k==12:return
            if k==23 and x>0 or k==25 and x<362:
                ship(x,172,K)
                x+=(k-24)*6
                ship(x,172,SC)
            if (k==24 or k==95 or k==14) and k!=lk and len(bu)<3:bu.append([x+7,166])
            lk=k
            for e in ex[:]:
                e[2]-=1
                if e[2]==0:
                    box(e[0],e[1],14,10,K)
                    ex.remove(e)
            for b in bu[:]:
                box(b[0],b[1],2,5,K)
                b[1]-=6
                if b[1]<14:bu.remove(b)
                else:box(b[0],b[1],2,5,(255,255,0))
            for b in bo[:]:
                box(b[0],b[1],2,4,K)
                b[1]+=4
                if b[1]>180:bo.remove(b)
                elif x-1<b[0]<x+16 and b[1]>168:
                    bo.remove(b)
                    l-=1
                    say("SHIP HIT!",RD)
                    show_screen()
                    for i in range(D*15):pass
                    say("",K)
                    hud(s,l,w)
                    ship(x,172,SC)
                    if l<1:break
                else:box(b[0],b[1],2,4,RD)
            if len(al)<2+w and randint(0,max(4,25-2*w))==0:
                al.append([randint(0,26)*14,14,randint(-1,1),randint(0,2)])
            for e in al[:]:
                if f%max(1,5-w) or l<1:continue
                alien(e,K)
                e[1]+=2
                e[0]+=e[2]*2
                if e[0]<0 or e[0]>370:e[2]=-e[2]
                e[0]=max(0,min(370,e[0]))
                if w>2 and randint(0,60)==0 and len(bo)<3:bo.append([e[0]+6,e[1]+10])
                hit=0
                for b in bu[:]:
                    if e[0]-2<b[0]<e[0]+14 and e[1]<b[1]+5 and b[1]<e[1]+10:
                        box(b[0],b[1],2,5,K)
                        bu.remove(b)
                        hit=1
                if hit:
                    al.remove(e)
                    box(e[0]+3,e[1]+1,8,8,(255,200,0))
                    ex.append([e[0],e[1],3])
                    s+=10*w
                    n+=1
                    if n%10==0:
                        w+=1
                        say("WAVE "+str(w),(255,255,0))
                        show_screen()
                        for i in range(D*15):pass
                        say("",K)
                    hud(s,l,w)
                elif e[1]>172 or e[1]>160 and x-13<e[0]<x+15:
                    al.remove(e)
                    l-=1
                    box(0,187,384,1,WH)
                    say(("ALIEN GOT THROUGH!","SHIP HIT!")[e[1]<=172],RD)
                    show_screen()
                    for i in range(D*15):pass
                    say("",K)
                    box(0,187,384,1,RD)
                    hud(s,l,w)
                    ship(x,172,SC)
                    if l<1:break
                else:alien(e,AC[e[3]])
            show_screen()
            for i in range(D):pass
            f+=1
        L.best=max(L.best,s)
        say("GAME OVER",RD)
        draw_string(130,120,"Score "+str(s)+"  OK: again",WH,"small")
        show_screen()
        if key()==12:return

main()
