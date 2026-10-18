from paclib import *

def draw(p,g,f):
    for a,b in CIR:
        u=(a-3)*p[2]+(b-3)*p[3]
        if f%6>2 or u<=0 or abs((a-3)*p[3]-(b-3)*p[2])>=u:set_pixel(4+p[0]+a,8+p[1]+b,PY)
    for j in range(4):
        e=g[j]
        box(4+e[0],9+e[1],7,6,GC[4 if e[5] else j])
        box(5+e[0],10+e[1],5,2,WH)

def main():
    while True:
        sc=0
        lv=1
        li=3
        clear_screen()
        draw_string(232,8,"PAC-MAN",PY,"large")
        while li:
            if lv>0:
                left=0
                for r in range(22):
                    dt[r]=0
                    for c in range(W):
                        if MZ[r*W+c] in ".o":
                            dt[r]|=1<<c
                            left+=1
                for i in range(594):tile(i%W,i//W)
                lv=-lv
            p=[104,128,0,0]
            g=[[104,64,-1,0,0,0],[104,80,0,0,30,0],[88,80,0,0,120,0],[120,80,0,0,210,0]]
            st=[sc,left,0]
            text(50,"Score "+str(sc))
            text(80,"Lives "+str(li)+"  Lv "+str(-lv))
            text(110,"READY!",PY)
            draw(p,g,0)
            show_screen()
            while getkey():pass
            nd=-1
            f=fr=ch=0
            dead=False
            while not dead and st[1]:
                k=getkey()
                if k==12:return
                if k in KD:nd=KD[k]
                if nd<0:continue
                if f==0:text(110,"")
                for e in [p]+g:under(e[0],e[1])
                pmove(p,nd,st)
                if st[2]:
                    st[2]=0
                    fr=max(60,250+30*lv)
                    ch=0
                    for e in g:
                        if e[4]==0:e[5]=1
                for j in range(4):
                    e=g[j]
                    if e[4]:
                        e[4]-=1
                        if e[4]==0:e[0],e[1],e[2],e[3]=104,64,-1,0
                    elif not ((e[5] and f%2) or (not e[5] and f%(5-lv)==0)):gmove(e,j,p)
                if fr:
                    fr-=1
                    if fr==0:
                        for e in g:e[5]=0
                for e in g:
                    if e[4]==0 and abs(e[0]-p[0])<6 and abs(e[1]-p[1])<6:
                        if e[5]:
                            st[0]+=200<<ch
                            ch+=1
                            e[0],e[1],e[2],e[3],e[4],e[5]=104,80,0,0,90,0
                        else:dead=True
                if st[0]!=sc:
                    sc=st[0]
                    text(50,"Score "+str(sc))
                draw(p,g,f)
                show_screen()
                for i in range(150):pass
                f+=1
            left=st[1]
            for e in [p]+g:under(e[0],e[1])
            if dead:li-=1
            else:lv=1-lv
        text(110,"GAME OVER",(220,0,0))
        text(140,"OK: again")
        show_screen()
        k=0
        while k!=24 and k!=95 and k!=12:k=getkey()
        if k==12:return

main()
