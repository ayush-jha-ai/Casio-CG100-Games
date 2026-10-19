from footlib import *
from random import randint

def main():
    while True:
        a=b=f=0
        ko=1
        for i in range(12):box(i*32,14,32,178,((40,150,40),(60,170,60))[i%2])
        for x,y,w,h in LN:box(x,y,w,h,WH)
        while f<5400:
            hud(a,b,f//60)
            u=[150,96]
            v=[264,96]
            gk=[[12,96],[372,96]]
            ball=[192*16,96*16,0,0]
            hv=ko
            dr=(1,0)
            go=0
            while not go and f<5400:
                k=getkey()
                if k==12:return
                o=[u[:],v[:],gk[0][:],gk[1][:],(ball[0]//16,ball[1]//16)]
                d=((0,-1),(-1,0),(0,1),(1,0))[(14,23,34,25).index(k)] if k in (14,23,34,25) else (0,0)
                if d!=(0,0):dr=d
                u[0]=max(6,min(378,u[0]+3*d[0]))
                u[1]=max(24,min(186,u[1]+3*d[1]))
                bx=ball[0]//16
                by=ball[1]//16
                tx=bx-v[0]
                ty=by-v[1]
                if hv==2:tx,ty=-v[0]+20,96-v[1]
                v[0]+=(tx>2)*2-(tx<-2)*2
                v[1]+=(ty>2)*2-(ty<-2)*2
                for g in gk:g[1]+=(by>g[1]+1)-(by<g[1]-1)
                for g in gk:g[1]=max(76,min(116,g[1]))
                for i,p in ((1,u),(2,v)):
                    if abs(p[0]-bx)<7 and abs(p[1]-by)<7 and (hv!=i and randint(0,(3,12)[i-1])==0 or hv==0):hv=i
                if hv==1:
                    ball[0]=(u[0]+6*dr[0])*16
                    ball[1]=(u[1]+6*dr[1])*16
                    if k==24 or k==95:
                        ball[2]=dr[0]*120
                        ball[3]=dr[1]*120+randint(-20,20)
                        hv=0
                elif hv==2:
                    ball[0]=(v[0]-6)*16
                    ball[1]=v[1]*16
                    if v[0]<110 or randint(0,60)==0:
                        ball[2]=-110
                        ball[3]=(96-v[1])*2+randint(-30,30)
                        hv=0
                        v[0]+=10
                else:
                    go=kick(ball,gk)
                    if go:ko=go%2+1
                    a+=go==1
                    b+=go==2
                ball[0]=max(0,min(383*16,ball[0]))
                ball[1]=max(16*16,min(188*16,ball[1]))
                for p in o[:4]:bg(p[0]-3,p[1]-9,7,14)
                bg(o[4][0]-2,o[4][1]-2,5,5)
                man(u,BL)
                man(v,RD)
                man(gk[0],(0,40,160))
                man(gk[1],(160,0,0))
                box(ball[0]//16-2,ball[1]//16-2,5,5,WH)
                if f%60==0:hud(a,b,f//60)
                show_screen()
                for i in range(D):pass
                f+=1
            for p in (u,v,gk[0],gk[1]):bg(p[0]-3,p[1]-9,7,14)
            bg(ball[0]//16-2,ball[1]//16-2,5,5)
            if go:
                hud(a,b,f//60)
                draw_string(150,60,"GOAL!",WH,"large")
                show_screen()
                for i in range(D*40):pass
                bg(150,60,90,24)
        r="DRAW"
        if a>b:r="YOU WIN"
        if b>a:r="CPU WINS"
        hud(a,b,90)
        box(100,62,184,96,(20,20,20))
        draw_string(120,70,"FULL TIME",WH,"large")
        draw_string(150,100,r,WH)
        draw_string(140,130,"OK: again",WH)
        show_screen()
        while getkey():pass
        k=0
        while k!=24 and k!=95 and k!=12:k=getkey()
        if k==12:return

main()
