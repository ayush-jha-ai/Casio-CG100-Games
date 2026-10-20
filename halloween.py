from hwlib import *
import hwlib as L

def main():
    while True:
        clear_screen()
        box(0,0,384,192,BG)
        for d in range(-16,17):
            w=int((289-d*d)**0.5)
            box(340-w,40+d,2*w,1,(250,240,200))
        box(0,176,384,16,(20,60,20))
        draw_string(306,80,"TRICK",OR)
        draw_string(306,100,"OR",OR)
        draw_string(306,120,"TREAT",OR)
        draw_string(10,20,"Catch sweets, dodge ghosts and bats",WH,"small")
        draw_string(10,36,"Golden lollipop 50  Heart = extra life",WH,"small")
        draw_string(10,52,"Catch in a row to build a combo",WH,"small")
        draw_string(10,80,"Best "+str(L.best)+"   OK: start",(255,255,0))
        show_screen()
        if key()==12:return
        box(0,0,300,176,BG)
        s=0
        l=3
        c=0
        lv=1
        x=138
        it=[]
        hud(s,l,1,lv)
        pump(x,152,4)
        mt=0
        while l>0:
            k=getkey()
            if k==12:return
            if k==23 and x>0 or k==25 and x<276:
                box(x,152,24,24,BG)
                x+=(k-24)*6
                pump(x,152,4)
            if len(it)<2+lv and randint(0,max(6,22-2*lv))==0:
                r=randint(0,99)
                t=4
                for q,v in ((62,0),(80,2),(93,3),(98,1)):
                    if r<q:
                        t=v
                        break
                it.append([randint(0,30)*9,18,t,(1,-1)[randint(0,1)],CC[randint(0,3)]])
            for e in it[:]:
                item(e,0)
                e[1]+=1+lv//2+(e[2]==2)
                if e[2]==3:
                    e[0]+=e[3]*2
                    if e[0]<1 or e[0]>286:e[3]=-e[3]
                if e[1]>140 and e[1]<164 and x-10<e[0]<x+22:
                    it.remove(e)
                    t=e[2]
                    if t==2 or t==3:
                        l-=1
                        c=0
                        say("BOO!")
                        mt=40
                    elif t==4:l=min(5,l+1)
                    else:
                        c+=1
                        s+=(10,50)[t]*min(5,1+c//5)
                    if s>=lv*250:
                        lv+=1
                        say("LEVEL "+str(lv))
                        mt=40
                    hud(s,l,min(5,1+c//5),lv)
                    pump(x,152,4)
                    if l<1:break
                elif e[1]>162:
                    it.remove(e)
                    if e[2]<2 and c:
                        c=0
                        hud(s,l,1,lv)
                else:item(e,e[4])
            show_screen()
            if mt:
                mt-=1
                if mt==0:say("")
            for i in range(D):pass
        L.best=max(L.best,s)
        say("GAME OVER")
        draw_string(110,90,"Score "+str(s)+"  OK: again",WH,"small")
        show_screen()
        if key()==12:return

main()
