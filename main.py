#coding:utf-8
import random,time,pygame,math
from pygame.locals import *

pygame.init()

btex,btey=500.,600.
btx,bty=1280.,1024.
io = pygame.display.Info()
mtx,mty=io.current_w,io.current_h
tex,tey=float(btex/btx*mtx),float(btey/bty*mty)

fenetre=pygame.display.set_mode([int(tex),int(tey)])

font=pygame.font.SysFont("Serif",20)
font1=pygame.font.SysFont("Serif",15)

################################################################

dim="images/"

panims=[[["p1-1.png","p1-2.png","p1-3.png","p1-4.png","p1-5.png","p1-6.png","p1-7.png","p1-8.png","p1-9.png","p1-10.png","p1-11.png","p1-12.png","p1-13.png","p1-14.png","p1-15.png"],["p1-1.png","p1-2.png","p1-3.png","p1-4.png","p1-5.png","p1-6.png","p1-7.png","p1-8.png","p1-9.png","p1-10.png","p1-11.png","p1-12.png","p1-13.png","p1-14.png","p1-15.png"]]]

obstacles=[["ford","v1.png",100,120]]



btez=float(math.sqrt((btex)**2.+(btey)**2.))
tez=float(math.sqrt((tex)**2.+(tey)**2.))

def rx(x): return float(x/btex*tex)
def ry(y): return float(y/btey*tey)
def rz(z): return float(z/btez*tez)

pv1_1=[rx(214.),ry(221.)]
pv1_2=[rx(75.),ry(585.)]
pv2_1=[rx(248.),ry(221.)]
pv2_2=[rx(254.),ry(584.)]
pv3_1=[rx(283.),ry(221.)]
pv3_2=[rx(418.),ry(583.)]

rt1x,rt1y=0.25,0.25
rt2x,rt2y=1.5,1.5
taillez=rz(500.)

lz1,lz2=rz(0.),taillez


class Perso:
    def __init__(self,z,keys,tpim,nom):
        self.nom=nom
        self.py=0.
        self.pz=float(lz2)
        self.tx=rx(100.)
        self.ty=ry(150.)
        self.tz=rz(5.)
        self.voie=random.randint(1,3)
        self.vitsaut=ry(200.)
        self.vitz=rz(20.)
        self.imgs=[]
        self.imgs_s=[]
        for i in panims[tpim][0]:
            self.imgs.append( pygame.transform.scale(pygame.image.load(dim+i),[int(self.tx),int(self.ty)]) )
        for i in panims[tpim][1]:
            self.imgs_s.append( pygame.transform.scale(pygame.image.load(dim+i),[int(self.tx),int(self.ty)]) )
        self.an=0
        self.img=self.imgs[self.an]
        self.dan=time.time()
        self.tpan=0.03
        self.dbg=time.time()
        self.tbg=0.1
        self.nbs=0
        self.nbts=1
        self.dupd=time.time()
        self.tupd=0.01
        self.issauter=False
        self.keyup=keys[0]
        self.keydown=keys[1]
        self.keyleft=keys[2]
        self.keyright=keys[3]
        self.keyjump=keys[4]
        self.bot=False
        self.vie_tot=5
        self.vie=self.vie_tot
        self.score=0
    def anim(self):
        if time.time()-self.dan >= self.tpan:
            self.dan=time.time()
            if not self.issauter:
                self.an+=1
                if self.an>=len(self.imgs): self.an=0
                self.img=self.imgs[self.an]
            else:
                if self.an<len(self.imgs_s)-1: self.an+=1
                self.img=self.imgs_s[self.an]
    def bouger(self,aa):
        if time.time()-self.dbg>=self.tbg:
            self.dbg=time.time()
            if aa=="up":
                if not self.issauter:
                    self.pz-=self.vitz
                    if self.pz<lz1: self.pz=lz1
            elif aa=="down":
                if not self.issauter:
                    self.pz+=self.vitz
                    if self.pz>lz2: self.pz=lz2
            elif aa=="left":
                if self.voie>1: self.voie-=1
            elif aa=="right":
                if self.voie<3: self.voie+=1
            elif aa=="jump":
                if self.py==0:
                    self.py+=self.vitsaut
                    self.nbs+=1
                    self.issauter=True
                    self.an=0
                elif self.nbs<self.nbts:
                    self.py+=self.vitsaut
                    self.nbs+=1
                    self.issauter=True
                    self.an=0
    def update(self):
        if self.vie>0:
            if time.time()-self.dupd >= self.tupd:
                self.dupd=time.time()
                if self.py>=0: self.py=self.py-0.75
                if self.issauter and self.py<=1: self.issauter,self.nbs,self.py=False,0,0
                self.score+=1

class Obstacl():
    def __init__(self,tp):
        self.vie=1
        self.nom=tp[0]
        self.tx=tp[2]
        self.ty=tp[3]
        self.tz=20.
        self.img=pygame.transform.scale(pygame.image.load(dim+tp[1]),[self.tx,self.ty])
        self.voie=random.randint(1,3)
        self.pz=random.randint(int(-lz2),0)
        self.py=0.
        self.vit=1
        self.dbg=time.time()
        self.tbg=0.01
    def update(self,persos):
        if self.vie>0:
            if time.time()-self.dbg>=self.tbg:
                self.dbg=time.time()
                self.pz+=self.vit
            for p in persos:
                if p.vie>0 and self.voie==p.voie and p.pz>=self.pz-self.tz and p.pz<=self.pz and pygame.Rect(0,self.py,self.tx,self.ty).colliderect(pygame.Rect(0,p.py,p.tx,p.ty)):
                    p.vie-=1
                    self.vie-=1
        
        

def aff_jeu(persos,obs,fps,imgbg):
    fenetre.blit(imgbg,[0,0])
    nlts=[]
    lts=[]
    for o in obs+persos:
        if o.vie>0: lts.append(o)
    while lts!=[]:
        lpz=lts[0]
        for l in lts:
            if not l in nlts and l.pz<=lpz.pz: lpz=l
        nlts.append(lpz)
        del(lts[lts.index(lpz)])
    for p in nlts:
        if p.pz>=lz1 and p.pz<=lz2:
            pd=p.pz/taillez
            ptx=p.tx*(rt1x+pd*(rt2x-rt1x))
            pty=p.ty*(rt1y+pd*(rt2y-rt1y))
            if p.voie==1:
                ppx=(pv1_1[0]+pd*(pv1_2[0]-pv1_1[0]))-ptx/2
                ppy=(pv1_1[1]+pd*(pv1_2[1]-pv1_1[1])-p.py)-pty/2.0
            elif p.voie==2:
                ppx=(pv2_1[0]+pd*(pv2_2[0]-pv2_1[0]))-ptx/2
                ppy=(pv2_1[1]+pd*(pv2_2[1]-pv2_1[1])-p.py)-pty/2.0
            else:
                ppx=(pv3_1[0]+pd*(pv3_2[0]-pv3_1[0]))-ptx/2
                ppy=(pv3_1[1]+pd*(pv3_2[1]-pv3_1[1])-p.py)-pty/2.0
            fenetre.blit(pygame.transform.scale(p.img,[int(ptx),int(pty)]),[int(ppx),int(ppy)])
    yy=25
    for p in persos:
        fenetre.blit(font.render(p.nom,20,(0,0,0)),[rx(5),ry(yy)])
        pygame.draw.rect(fenetre,(250-(p.vie/p.vie_tot*200),0,0),(rx(100),ry(yy),rx(p.vie/p.vie_tot*100),ry(25)),0)
        pygame.draw.rect(fenetre,(0,0,0),(rx(100),ry(yy),rx(100),ry(25)),2)
        fenetre.blit(font.render(str(p.score),20,(0,0,0)),[rx(205),ry(yy)])
        yy+=45
    fenetre.blit(font1.render("fps : "+str(fps),20,(255,255,255)),[rx(5),ry(5)])
    pygame.display.update()

def verif_key(persos):
    keys=pygame.key.get_pressed()
    for p in persos:
        if not p.bot:
            if keys[p.keyup]: p.bouger("up")
            if keys[p.keydown]: p.bouger("down")
            if keys[p.keyleft]: p.bouger("left")
            if keys[p.keyright]: p.bouger("right")
            if keys[p.keyjump]: p.bouger("jump")

def jeu():
    pause=False
    perdu=False
    nbobs=0
    animbg=[pygame.transform.scale(pygame.image.load(dim+"bg_1.png"),[int(tex),int(tey)]) ,pygame.transform.scale(pygame.image.load(dim+"bg_2.png"),[int(tex),int(tey)])]
    anbg=0
    imgbg=animbg[anbg]
    danbg=time.time()
    tanbg=0.1
    obs=[]
    nbobs=1
    daugob=time.time()
    taugob=5
    maxob=20
    persos=[]
    persos.append( Perso(1.,[K_UP,K_DOWN,K_LEFT,K_RIGHT,K_END],0,"player1") )
    fps=0
    encour=True
    while encour and not perdu:
        t1=time.time()
        aff_jeu(persos,obs,fps,imgbg)
        if not pause:
            #persos
            nbenv=0
            for p in persos:
                p.anim()
                p.update()
                if p.vie>0: nbenv+=2
            if nbenv==0: perdu=True
            #bg
            if time.time()-danbg>=tanbg:
                danbg=time.time()
                anbg+=1
                if anbg>=len(animbg): anbg=0
                imgbg=animbg[anbg]
            #obstacles
            if time.time()-daugob>=taugob:
                daugob=time.time()
                if nbobs<maxob: nbobs+=1
            for o in obs:
                if o.pz>=lz2 or o.vie<=0:
                    if o in obs: del(obs[obs.index(o)])
            while len(obs)<nbobs: obs.append( Obstacl(random.choice(obstacles)) )
            for o in obs:
                o.update(persos)
            verif_key(persos)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                elif event.key==K_p: pause=not pause
        t2=time.time()
        tt=(t2-t1)
        if tt!=0:
            fps=int(1./tt)
    encour2=True
    fenetre.fill((0,0,0))
    fenetre.blit(font.render("Crushed",20,(255,50,50)),[rx(200),ry(50)])
    yy=100
    for p in persos:
        fenetre.blit(font.render("-"+p.nom+" : "+str(p.score),20,(255,255,255)),[rx(150),ry(yy)])
        yy+=50
    fenetre.blit(font.render("press space to continue",20,(255,255,255)),[rx(100),ry(500)])
    pygame.display.update()
    while encour2:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key in [K_ESCAPE,K_SPACE]: encour2=False




def aff_menu(imgbg,tfps):
    pygame.draw.rect(fenetre,(33,158,173),(rx(0),ry(0),rx(80),ry(30)),0)
    fenetre.blit(font1.render(tfps,20,(255,255,255)),[rx(5),ry(5)])
    pygame.display.update()
    

def menu():
    imgbg=pygame.transform.scale(pygame.image.load(dim+"menu_bg.png"),[int(tex),int(tey)])
    bts=[pygame.Rect(rx(163),ry(371),rx(371-163),ry(506-371))]
    encoure=True
    tfps="fps : 0"
    fenetre.blit(imgbg,[0,0])
    while encoure:
        t1=time.time()
        aff_menu(imgbg,tfps)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN and event.key==K_ESCAPE: encoure=False
            elif event.type==MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                for b in bts:
                    if b!=None and b.collidepoint(pos):
                        i=bts.index(b)
                        if i==0:
                            jeu()
                            fenetre.blit(imgbg,[0,0])
        t2=time.time()
        tt=(t2-t1)
        if tt!=0:
            tfps="fps : "+str(int(1./tt))

menu()









