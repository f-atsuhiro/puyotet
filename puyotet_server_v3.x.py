from tkinter import *
from random import randint as rnd
from tkinter import font as ft
import pygame
import threading
import socket
import time
import pickle
reconnectP2,reconnectP1=0,0
getip=[[0,0],[0,0]]
ip_address="127.0.0.1"#自身のaddress
port=25567
true,false=0,1
mainhaikei=[0]
player=[0,0]#プレイヤー1と2がどちらを選択したか
clickimage=[0,0,0,0]
gameover=[0]#ゲームオーバー時に表示するpngを詰める
GameOvercnt=0#他の動作に終了の判定を与える
playeronedamage,playertwodamage=0,0
ojyapuyo=[0,0,0,0,0,0]
ojyamino=[0,0,0,0,0]
tetrisatklist=[0,4,5,6,8,10,13,16,20,24,28,33,38,43,49,55,61,68,75,83,92,102,113,125,138,152,167,183,200,218,237,157,278,300,323,347,372,398,425,453,482,512,543,575,608,642,677,713,750,788,827,867,908,950,993,1037,1082,1128,1175,1223,1272]
beginimage=[0,0,0,0,0]
gamestartflag=false

def initialize():
    global getip,ip_address,player,playeronedamage,playertwodamage,GameOvercnt,gamestartflag
    getip=[[0,0],[0,0]]
    ip_address="192.168.0.9"
    player=[0,0]#プレイヤー1と2がどちらを選択したか
    GameOvercnt=0#他の動作に終了の判定を与える
    playeronedamage,playertwodamage=0,0
    gamestartflag=false
    threadmain=threading.Thread(target=main)
    threadclient=threading.Thread(target=tcpreceive)
    threadmain.start()
    threadclient.start()

pygame.init()
#---------------------------------------------------------------------------ゲーム選択
def tetrisone():
    global player
    player[0]=1#tetris
    senddata=[4,0,1]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def tetristwo():
    global player
    player[1]=1#tetris
    senddata=[4,0,2]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def puyopuyoone():
    global player
    player[0]=2
    senddata=[4,1,1]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def puyopuyotwo():
    global player
    player[1]=2
    senddata=[4,1,2]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def gamebefore():
    global gamestartflag
    gamestartbef()
    gamestartflag=true

def gamestartbef():
    global btn1,btn2,btn3,btn4,btn5
    if gamestartflag==true:
        if player[0]==0 or player[1]==0:
            return
        
        cv.delete('all')
        mainpic=rnd(0,3)
        mainhaikei[0]=PhotoImage(file=f"./main/main{mainpic}.png")
        senddata=[2,mainpic]
        threadsend=threading.Thread(target=tcpsend(senddata))
        threadsend.start()

        senddata=[3,[player[0],player[1]]]
        threadsend=threading.Thread(target=tcpsend(senddata))
        threadsend.start()
        gameReady()

def gameReady():
    cv.after(1000,gameGo)

def gameGo():
    cv.after(1000,gamestart)

def gamestart():
    cv.delete("settinggo")
    if player[0]==1:
        tetrisoneplay.main()
    elif player[0]==2:
        puyopuyooneplay.main()
    if player[1]==1:
        tetristwoplay.main()
    elif player[1]==2:
        puyopuyotwoplay.main()
#------------------------------------------------------------------------------tetris 1player
class tetrisplay():
    def __init__(self):
        global master,GameOvercnt,sc
        self.lencntdoublecheck=0
        self.senddata=[-1,-1,-1,-1]
        self.firstin=true
        self.moveflag=false
        self.doublemove=false
        self.BtbFlag=false
        self.Btb=false
        self.playernum=0
        self.o=0
        self.TspinCnt=0
        self.Tspin=false
        self.spincheck=false
        self.lamp=0
        self.height=20
        self.lenght=10
        self.size=30
        self.minosize=4
        self.form=0
        self.direction=0
        self.moveend=false
        self.lencnt=0
        self.holdcnt=0
        self.holdsave=0
        self.holdmax=0
        self.score=0
        self.progend=0
        self.x=4
        self.y=-2
        self.speed=500
        self.MAX=0
        self.i=0
        self.Tspinmini=false
        self.nextmino=[[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]],[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]],[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]],[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]]]
        self.sound=[0,0,0,0,0,0,0]
        self.tec=[[0,0,0,0,0,0],[0],[0],[0]]#ts,tetris,perfect,btb
        self.colors = ["#00ffff", #I:0
          "#0000ff", #J:1
          "#ffa500", #L:2
          "#ffff00", #O:3
          "#008000", #S:4
          "#800080", #T:5
          "#ff0000", #Z:6
          "#EEEEEE", #haikei:7
          "#808000", #壁:8
          "#696969", #お邪魔ミノ:9
          0]#お邪魔ぷよ
        self.RotPattern=[[[[0,-1],[-1,-1],[2,0],[2,-1]],[[0,1],[-1,1],[2,0],[2,1]]],#右回転,左回転 A=0
		                [[[0,1],[1,1],[-2,0],[-2,1]],[[0,1],[1,1],[-2,0],[-2,1]]],#B=1
		                [[[0,1],[-1,1],[2,0],[2,1]],[[0,-1],[1,-1],[2,0],[2,-1]]],#C=2
		                [[[0,-1],[1,-1],[-2,0],[-2,-1]],[[0,-1],[1,-1],[2,0],[2,-1]]]]#D=3
        self.RotPatternI=[[[[0,-2],[0,1],[1,-2],[2,1]],[[0,-1],[0,2],[-2,-1],[1,2]]],
                        [[[0,-1],[0,2],[-2,-1],[1,2]],[[0,2],[0,-1],[-1,1],[2,-1]]],
                        [[[0,2],[0,-1],[-1,2],[2,-1]],[[0,1],[0,-2],[2,2],[-1,-2]]],
                        [[[0,-2],[0,1],[2,1],[-1,-2]],[[0,1],[0,-2],[1,-2],[-2,1]]]]
        self.string=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.colors[10]=PhotoImage(file="./picture/tetris/mino/atkpuyo.png")
        self.mino_result=[[0,0],[0,0],[0,0],[0,0]] #ミノの下の座標を保存する
        self.mino_resultsec=[[0,0],[0,0],[0,0],[0,0]]
        self.mino_end=[[0,0],[0,0],[0,0],[0,0]]
        self.lencntbef=0 #len終了処理用
        self.haikei =    [[8,7,7,7,7,7,7,7,7,7,7,8],                                 #背景(内部)
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,8,8,8,8,8,8,8,8,8,8,8]]



#テトミノが確実に4つの四角形で構成されることを利用して4*4の範囲にテトミノがあると考えて進める
        self.mino_data = [[[[2, 0], [2, 1], [2, 2], [2, 3]], #I:0:ここから4行でIミノの状態(回転後を含めて4種類)を定義する
              [[0, 1], [1, 1], [2, 1], [3, 1]],
              [[1, 0], [1, 1], [1, 2], [1, 3]],
              [[0, 2], [1, 2], [2, 2], [3, 2]]],
             [[[1, 0], [2, 0], [2, 1], [2, 2]], #J:1:以下同様
              [[1, 1], [1, 2], [2, 1], [3, 1]],
              [[2, 0], [2, 1], [2, 2], [3, 2]],
              [[1, 1], [2, 1], [3, 0], [3, 1]]],
             [[[1, 2], [2, 0], [2, 1], [2, 2]], #L:2
              [[1, 1], [2, 1], [3, 1], [3, 2]],
              [[2, 0], [2, 1], [2, 2], [3, 0]],
              [[1, 0], [1, 1], [2, 1], [3, 1]]],
             [[[1, 1], [1, 2], [2, 1], [2, 2]], #O:3
              [[1, 1], [1, 2], [2, 1], [2, 2]],
              [[1, 1], [1, 2], [2, 1], [2, 2]],
              [[1, 1], [1, 2], [2, 1], [2, 2]]],
             [[[1, 1], [1, 2], [2, 0], [2, 1]], #S:4
              [[1, 1], [2, 1], [2, 2], [3, 2]],
              [[2, 1], [2, 2], [3, 0], [3, 1]],
              [[1, 0], [2, 0], [2, 1], [3, 1]]],
             [[[1, 1], [2, 0], [2, 1], [2, 2]], #T:5
              [[1, 1], [2, 1], [2, 2], [3, 1]],
              [[2, 0], [2, 1], [2, 2], [3, 1]],
              [[1, 1], [2, 0], [2, 1], [3, 1]]],
             [[[1, 0], [1, 1], [2, 1], [2, 2]], #Z:6
              [[1, 2], [2, 1], [2, 2], [3, 1]],
              [[2, 0], [2, 1], [3, 1], [3, 2]],
              [[1, 1], [2, 0], [2, 1], [3, 0]]]]
        self.mino = [[7,7,7,7],
        [7,7,7,7],
        [7,7,7,7],
        [7,7,7,7]] #テトミノを4*4として背景を設置する(のちにmino_dataを被せる
        self.minohold=[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]]
        self.next=[7,7,7,7]
        self.usedmino=[0,0,0,0,0,0,0]
        self.nextimage=PhotoImage(file="./picture/tetris/word/next.png")
    def main(self):
        self.colors[0]=PhotoImage(file="./picture/tetris/mino/i_mino.png")
        self.colors[1]=PhotoImage(file="./picture/tetris/mino/j_mino.png")
        self.colors[2]=PhotoImage(file="./picture/tetris/mino/l_mino.png")
        self.colors[3]=PhotoImage(file="./picture/tetris/mino/o_mino.png")
        self.colors[4]=PhotoImage(file="./picture/tetris/mino/s_mino.png")
        self.colors[5]=PhotoImage(file="./picture/tetris/mino/t_mino.png")
        self.colors[6]=PhotoImage(file="./picture/tetris/mino/z_mino.png")
        self.colors[7]=PhotoImage(file="./picture/tetris/mino/no_mino.png")
        self.colors[9]=PhotoImage(file="./picture/tetris/mino/ojya_mino.png")
        self.string[0]=PhotoImage(file="./picture/tetris/word/0.png")
        self.string[1]=PhotoImage(file="./picture/tetris/word/1.png")
        self.string[2]=PhotoImage(file="./picture/tetris/word/2.png")
        self.string[3]=PhotoImage(file="./picture/tetris/word/3.png")
        self.string[4]=PhotoImage(file="./picture/tetris/word/4.png")
        self.string[5]=PhotoImage(file="./picture/tetris/word/5.png")
        self.string[6]=PhotoImage(file="./picture/tetris/word/6.png")
        self.string[7]=PhotoImage(file="./picture/tetris/word/7.png")
        self.string[8]=PhotoImage(file="./picture/tetris/word/8.png")
        self.string[9]=PhotoImage(file="./picture/tetris/word/9.png")
        self.string[10]=PhotoImage(file="./picture/tetris/word/renstring.png")
        self.string[11]=PhotoImage(file="./picture/tetris/word/score.png")
        self.string[12]=PhotoImage(file="./picture/tetris/word/tetris.png")
        self.tec[0][0]=PhotoImage(file="./picture/tetris/technique/TSS.png")    #T spin single
        self.tec[0][1]=PhotoImage(file="./picture/tetris/technique/TSSM.png")   #T spin single mini
        self.tec[0][2]=PhotoImage(file="./picture/tetris/technique/TSD.png")    #T spin double
        self.tec[0][3]=PhotoImage(file="./picture/tetris/technique/TSDM.png")   #T spin double mini
        self.tec[0][4]=PhotoImage(file="./picture/tetris/technique/TST.png")    #T spin triple
        self.tec[0][5]=PhotoImage(file="./picture/tetris/technique/TST.png")    #T spin triple (mini)
        self.tec[3][0]=PhotoImage(file="./picture/tetris/technique/BTB.png")    #Back To Back
        self.sound[0]=pygame.mixer.Sound("./sound/tetris/minodelete.ogg")  #ren sound
        #cv.create_image(500+self.playernum*300,470,image=self.tec[0][1],tag=f"tetone{self.playernum}")
        self.MinoMove()
        self.MinoCreate()
        self.HaikeiDraw()
        self.MinoDraw()
        self.ScoreCnt()
    def HaikeiDraw(self):
        cv.delete(f"tetone{self.playernum}")
        if GameOvercnt==0:
            #self.senddata=[0,self.playernum,0,self.haikei,[self.lencnt,self.BtbFlag,self.Tspinmini,self.Tspin,self.lencntdoublecheck,self.holdsave,self.minohold]]
            #threadsend=threading.Thread(target=tcpsend(self.senddata))
            #threadsend.start()
            #textnext.place_forget()
            self.haikeidrawflag=true
            self.nextdraw()###############################未編集

    def MinoCreate(self):
        self.form=rnd(0,6)
        self.usedmino[self.form]=1
        for self.minomakeside in range(4):
            self.next[self.minomakeside] =rnd(0,6)
            self.nextcheck()
        for i in range(len(self.mino_data[self.form][self.direction%4])):
            y=self.mino_data[self.form][self.direction%4][i][0]
            x=self.mino_data[self.form][self.direction%4][i][1]
            self.mino[y][x]=self.form
        #self.nextdraw()

    def MinoDraw(self):
        self.senddata=[0,self.playernum,1,[self.y,self.x]]
        threadsend=threading.Thread(target=tcpsend(self.senddata))
        threadsend.start()

    def nextcheck(self):#乱数調整
        if self.usedmino[self.next[self.minomakeside]]==1:
            self.next[self.minomakeside]=rnd(0,6)
            self.nextcheck()#乱数調整終了まで再帰
        else:
            self.usedmino[self.next[self.minomakeside]]=1

    def minomake_first(self):
        self.next[self.minomakeside]=rnd(0,6)
        self.nextcheck()
    #----------------------------------drop
    def MinoMove(self):
        if GameOvercnt==0 and self.doublemove==false:
                checkcnt=0
                self.moveflag=false
                self.doublemove=true
                if self.moveend==true:
                    self.drop_end_sidemove()
                    self.doublemove=false
                    self.moveend=false
                    cv.after(self.speed,self.MinoMove)
                    return
                self.senddata=[0,self.playernum,5,[self.y,self.x,self.form,self.mino]]
                threadsend=threading.Thread(target=tcpsend(self.senddata))
                threadsend.start()
                rock=0
                self.spincheck=false
                for i in range(4):
                    check_y=self.y+self.mino_data[self.form][self.direction%4][i][0]+1
                    check_x=self.x+self.mino_data[self.form][self.direction%4][i][1]
                    if self.haikei[check_y][check_x] == 7:
                        checkcnt+=1
                if (self.haikei[1][5]==7 or self.haikei[1][6]==7 or self.haikei[1][7]==7 or self.haikei[1][8]==7) and checkcnt==4:
                    self.y+=1
                    for ydraw in range(self.minosize):
                        for xdraw in range(self.minosize):
                            if self.mino[ydraw][xdraw]==self.form:
                                rock=self.MinoSearch()
                    if self.moveend==true:
                        self.drop_end_sidemove()
                        self.moveend=false
                        self.doublemove=false
                        cv.after(self.speed,self.MinoMove)
                        return
                else:
                    for ydraw in range(self.minosize):
                        for xdraw in range(self.minosize):
                            if self.mino[xdraw][ydraw]==self.form:
                                rock=self.MinoSearch()
                if self.haikei[1][5]!=7 or self.haikei[1][6]!=7 or self.haikei[1][7]!=7 or self.haikei[0][8]!=7:
                    GameOver(self.playernum+1)
                    return
                self.i=0
                if rock!=8:
                    if self.moveend==true:
                        self.drop_end_sidemove()
                        self.moveend=false
                    cv.after(self.speed,self.MinoMove)
                    
                else:
                    rock=cv.after(self.speed,self.rockfunc)
                
                self.doublemove=false
                if self.firstin==true:
                    dropcheckthread=threading.Thread(target=self.endmove)
                    dropcheckthread.start()
                    self.firstin=false

    def endmove(self):
            
            if self.moveend==true and self.moveflag==true:
                self.drop_end_sidemove()
                self.moveend=false
                self.moveflag=false
            cv.after(1,self.endmove)

    def rockfunc(self):
        rock=0
        for isec in range(4):
            rock=self.MinoSearchSecond(isec)
            if rock==8:
                break
        if rock==8:
            self.drop_end()
        else:
            if self.moveend==true:
                self.drop_end_sidemove()
                self.moveend=false
            self.MinoMove()
            
    def drop_end(self):
        if GameOvercnt==0:
            self.lencntbef+=1
            if self.lencntbef>=2:
                self.lencnt=0
                self.GraphicRenCnt(self.lencnt)
            for ydraw in range(self.minosize):
                ydraw1=(ydraw+self.y-1)*self.size
                for xdraw in range(self.minosize):
                    xdraw1=(xdraw+self.x-1)*self.size
                    if self.mino[ydraw][xdraw]==self.form:
                        self.haikei[ydraw+self.y][xdraw+self.x]=self.form
            
            if xdraw==3:
                self.x,self.y=4,-2
                self.direction=0
                self.TetrisLen()
                self.MinoRnd()
                if self.playernum==0:
                    self.damagetetrisone()
                else:
                    self.damagetetristwo()
                self.MinoMove()
                self.holdmax=0
                #self.nextdraw()

    def damagetetrisone(self):
        global playeronedamage
        if playeronedamage<=6:#一度のせり上がりが6段まで
            damageloopcnt=playeronedamage
        else:
            damageloopcnt=6
        for damageloop in range(damageloopcnt):
            for damageup in range(len(self.haikei)-1):
                for damageupsub in range(len(self.haikei[damageup])):
                    self.haikei[damageup][damageupsub]=self.haikei[damageup+1][damageupsub]
                    tetrishole=rnd(1,10)
            if player[1]==1:#相手によってお邪魔ミノorぷよ
                self.haikei[20]=[8,9,9,9,9,9,9,9,9,9,9,8]
            if player[1]==2:
                self.haikei[20]=[8,10,10,10,10,10,10,10,10,10,10,8]
            self.haikei[20][tetrishole]=7#一マス穴をあける
            playeronedamage-=1
        self.HaikeiDraw()
        OnePlayerReceveDamegeG(0)

    def damagetetristwo(self):
        global playertwodamage
        if playertwodamage<=6:#一度のせり上がりが6段まで
            damageloopcnt=playertwodamage
        else:
            damageloopcnt=6
        for damageloop in range(damageloopcnt):
            for damageup in range(len(self.haikei)-1):
                for damageupsub in range(len(self.haikei[damageup])):
                    self.haikei[damageup][damageupsub]=self.haikei[damageup+1][damageupsub]
            tetrishole=rnd(1,10)
            if player[1]==1:#相手によってお邪魔ミノorぷよ
                self.haikei[20]=[8,9,9,9,9,9,9,9,9,9,9,8]
            if player[1]==2:
                self.haikei[20]=[8,10,10,10,10,10,10,10,10,10,10,8]
            self.haikei[20][tetrishole]=7#一マス穴をあける
            playertwodamage-=1
        self.HaikeiDraw()
        TwoPlayerReceveDamegeG(0)   

    def drop_end_sidemove(self):
        if GameOvercnt==0:
            self.Tspin=false
            self.TspinCnt=0
            self.lencntbef+=1
            if self.lencntbef>=2:
                self.lencnt=0
                self.GraphicRenCnt(self.lencnt)
            for ydraw in range(self.minosize):                                                                   
                for xdraw in range(self.minosize):                                                                   
                    if self.mino[ydraw][xdraw] == self.form:     
                        self.haikei[ydraw+self.y][xdraw+self.x]=self.form
            if xdraw==3:
                if self.form==5:
                    if self.haikei[self.y+1][self.x+0]!=7:
                        self.TspinCnt+=1
                    if self.haikei[self.y+1][self.x+2]!=7:
                        self.TspinCnt+=1
                    if self.haikei[self.y+3][self.x+0]!=7:
                        self.TspinCnt+=1
                    if self.haikei[self.y+3][self.x+2]!=7:
                        self.TspinCnt+=1
                    if self.direction%2==1:
                        if self.haikei[self.y+4][self.x+1]!=7:
                            self.Tspinmini=true
                    elif self.direction%4==0:
                        if self.haikei[self.y+3][self.x+1]!=7:
                            self.Tspinmini=true
                    if self.TspinCnt>=3:
                        self.Tspin=true
                self.x,self.y=4,-2
                self.direction=0
                self.TetrisLen()
                self.MinoRnd()
                if self.playernum==0:
                    self.damagetetrisone()
                else:
                    self.damagetetristwo()
                self.holdmax=0
                #self.nextdraw()
    def MinoRnd(self):
        self.mino=[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]]
        self.form=self.next[0]
        for j in range(3):
            self.next[j]=self.next[j+1]
        self.next[3]=rnd(0,6)
        self.checkmino()
        for i in range(len(self.mino_data[self.form][self.direction%4])):
            y=self.mino_data[self.form][self.direction%4][i][0]
            x=self.mino_data[self.form][self.direction%4][i][1]
            self.mino[y][x]=self.form
        #if self.lencnt==0 and self.lamp!=0:
        #    damageattwoplayer(self.lamp)
        

    def checkmino(self):
        if self.usedmino[self.next[3]]==0:
            self.usedmino[self.next[3]]=1
        else:
            self.minomake()

    def minomake(self):
        if self.usedmino==[1,1,1,1,1,1,1]:
            self.usedmino=[0,0,0,0,0,0,0]
        else:
            self.next[3]=rnd(0,6)
            self.checkmino()



    def MinoSearch(self):
        Search_y=self.mino_data[self.form][self.direction%4][self.i][0]
        Search_x=self.mino_data[self.form][self.direction%4][self.i][1]
        self.mino_result[self.i][0]=self.y+1+Search_y
        self.mino_result[self.i][1]=self.x+Search_x
        if self.haikei[self.mino_result[self.i][0]][self.mino_result[self.i][1]]!=7:
            rock=8
            return rock
        self.i+=1

    def MinoSearchSecond(self,isec):
        Search_y=self.mino_data[self.form][self.direction%4][isec][0]
        Search_x=self.mino_data[self.form][self.direction%4][isec][1]
        self.mino_result[isec][0]=self.y+1+Search_y
        self.mino_result[isec][1]=self.x+Search_x
        if self.haikei[self.mino_result[isec][0]][self.mino_result[isec][1]]!=7:
            rock=8
            return rock

    def MinoSearch_side(self):
        Search_y=self.mino_data[self.form][self.direction%4][self.o][0]
        Search_x=self.mino_data[self.form][self.direction%4][self.o][1]
        self.mino_result[self.o][0]=self.y+1+Search_y
        self.mino_result[self.o][1]=self.x+Search_x
        if self.haikei[self.mino_result[self.o][0]][self.mino_result[self.o][1]]!=7:
            rock=8
            return rock
        self.o=self.o+1
   

#---------------------------------------------------------------

    def MinoMoveKey(self,adddire,addy,addx,drop):
        if GameOvercnt==0:
            self.moveflag=true
            if addy!=0 or addx!=0 or drop==1:
                self.spincheck=false
                rock,movecheck=0,0
                for i in range(4):
                    Search_y=self.mino_data[self.form][self.direction%4][i][0]                                             #Search_yに現在のミノの位置(4*4内)のy座標を保存
                    Search_x=self.mino_data[self.form][self.direction%4][i][1] 
                    self.mino_result[i][0]=self.y+Search_y+addy
                    self.mino_result[i][1]=self.x+Search_x+addx
                    if self.haikei[self.mino_result[i][0]][self.mino_result[i][1]]==7:
                        movecheck+=1
                    if movecheck==4:
                        
                        sendx=self.x
                        sendy=self.y
                        self.x+=addx
                        self.y+=addy
                        if addx!=0 or addy!=0:
                            self.senddata=[0,self.playernum,6,[sendy,sendx,self.form,self.mino,addy,addx,0,0]]
                            threadsend=threading.Thread(target=tcpsend(self.senddata))
                            threadsend.start()
                            for ydraw in range(self.minosize):
                                for xdraw in range(self.minosize):
                                    if self.mino[ydraw][xdraw]==self.form:
                                        rock=self.MinoSearch_side()
                            if addx!=0:
                                pygame.mixer.Sound("./sound/tetris/move.ogg").play()
                            self.o=0
                            if rock==8:
                                self.moveend=true
                        if drop==1:
                            pygame.mixer.Sound("./sound/tetris/drop.ogg").play()
                            pygame.mixer.Sound("./sound/tetris/move.ogg").play()
                            while True:
                                drop=0
                                for i in range(4):
                                    Search_y=self.mino_data[self.form][self.direction%4][i][0]                                             #Search_yに現在のミノの位置(4*4内)のy座標を保存
                                    Search_x=self.mino_data[self.form][self.direction%4][i][1]                                             #Search_xに現在のミノの位置(4*4内)のx座標を保存
                                    self.mino_result[i][0]=self.y+1+Search_y                                                          #mino_result[i][1]に現在のミノのブロックの一マス横のy座標を保存
                                    self.mino_result[i][1]=self.x+Search_x
                                    if self.haikei[self.mino_result[i][0]][self.mino_result[i][1]]==7:
                                        drop+=1
                                if drop>=4:
                                    self.y+=1
                                else:
                                    break
                            sendy=self.y
                            sendx=self.x
                            
                            self.senddata=[0,self.playernum,6,[sendy,sendx,self.form,self.mino,0,0,drop,0]]
                            threadsend=threading.Thread(target=tcpsend(self.senddata))
                            threadsend.start()
                            self.moveend=true
                            
            if adddire!=0:#rightrot=-1,leftrot=1,none=0
                
                RotDirection=self.direction
                cant,RotAfterEnd=0,0
                RotDirection+=adddire
                mino_C=[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]]
                for RotI in range(self.minosize):
                    Cy=self.mino_data[self.form][RotDirection%4][RotI][0]
                    Cx=self.mino_data[self.form][RotDirection%4][RotI][1]
                    mino_C[Cy][Cx]=self.form
                    if self.x+Cx==12 or self.x+Cx==-1 or self.y+ Cy==-1 or self.y+Cy==22:
                        break
                    if self.haikei[self.y+Cy][self.x+Cx]==7:
                        cant+=1
                if cant>=4:
                    self.senddata=[0,self.playernum,6,[self.y,self.x,self.form,self.mino,0,0,0,0]]
                    threadsend=threading.Thread(target=tcpsend(self.senddata))
                    threadsend.start()  
                    self.direction+=adddire
                    
                     
                    for xdraw in range(self.minosize):
                        xdraw1=(xdraw+self.y-1)*self.size
                        for ydraw in range(self.minosize):
                            ydraw1=(ydraw+self.x-1)*self.size
                            if self.mino[xdraw][ydraw] == self.form:
                                self.mino[xdraw][ydraw]=7
                    for RotI in range(len(self.mino_data[self.form][self.direction % 4])):
                        Gy = self.mino_data[self.form][self.direction % 4][RotI][0]                                            #この３行で一ブロックを生成(？)恐らく、mino_dataの[form][direction%4]がrnd=3と仮定するとoミノの一番上の配列となりそれのi番目の0番目をここでみて
                        Gx = self.mino_data[self.form][self.direction % 4][RotI][1]                                            #この行でdirection=1番目の1番目の数値を検出して
                        self.mino[Gy][Gx] = self.form
                    self.senddata=[0,self.playernum,6,[self.y,self.x,self.form,self.mino,0,0,0,adddire]]
                    threadsend=threading.Thread(target=tcpsend(self.senddata))
                    threadsend.start()   
                    for xdraw in range(self.minosize):                                                           #変数vをminosize(ミノの領域)回続ける
                        xdraw1 = (xdraw + self.y - 1) * self.size                                           #上2行でミノ１ブロックの始まり座標と終わり座標を算出(そのためミノの数(v)回同じ処理をして4つミノを成立させる
                        for ydraw in range(self.minosize):                                                       #変数sを用意してもう一度minosize回のループを生成する
                            ydraw1 = (ydraw + self.x - 1) * self.size                                                          #s2にs1+size☆\\前行+一マス当たりのサイズ
                            if self.mino[xdraw][ydraw] == self.form:   #その１ブロックの始まり座標から終わり座標までをcolors[form]で指定された色にする:要点:今まではミノについての内部処理でその内部情報をここで初めて出力している
                                if self.haikei[self.y+xdraw+1][self.x+ydraw]!=7:#イライラ棒() ここの関数でxdrawとydrawが逆の意味でつかわれてるのに気付くのに1時間とかマジで()
                                    RotAfterEnd+=1
                    if RotAfterEnd>=1:
                        self.moveend=true


                else:
                    pattern_one,pattern_two,pattern_three,pattern_four,BreakPoint=0,0,0,0,0
                    
                    if adddire==1:#右回転
                        direcheck=0
                    elif adddire==-1:#左回転
                        direcheck=1
                    for i in range(self.minosize):
                        for RotI in range(self.minosize):
                            Cy=self.mino_data[self.form][RotDirection%4][RotI][0]
                            Cx=self.mino_data[self.form][RotDirection%4][RotI][1]
                            if self.x+Cx==12 or self.x+Cx==-1:
                                break
                            
                            if (self.form != 0 and self.haikei[self.y+Cy+self.RotPattern[(self.direction)%4][direcheck][i][0]][self.x+Cx+self.RotPattern[(self.direction)%4][direcheck][i][1]]==7) or (self.form==0 and self.haikei[self.y+Cy+self.RotPatternI[self.direction%4][direcheck][i][0]][self.x+Cx+self.RotPatternI[self.direction%4][direcheck][i][1]]==7):
                                
                                if i == 0:
                                    pattern_one+=1
                                    if pattern_one==4:
                                        BreakPoint=1
                                        break
                                elif i == 1:
                                    pattern_two+=1
                                    if pattern_two==4:
                                        BreakPoint=2
                                        break
                                elif i == 2:
                                    pattern_three+=1
                                    if pattern_three==4:
                                        BreakPoint=3
                                        break
                                elif i == 3:
                                    pattern_four+=1
                                    if pattern_four==4:
                                        BreakPoint=4
                                        break
                    #ここまでで移動可能or移動不可を判定
                        
                        if BreakPoint != 0:
                            break
                    if BreakPoint != 0:
                        self.senddata=[0,self.playernum,7,[self.y,self.x,self.form,self.mino,0]]
                        threadsend=threading.Thread(target=tcpsend(self.senddata))
                        threadsend.start()  
                        for xdraw in range(self.minosize):
                            xdraw1 = (xdraw + self.y - 1) * self.size
                            for ydraw in range(self.minosize):
                                ydraw1 = (ydraw + self.x - 1) * self.size
                                if self.mino[xdraw][ydraw] == self.form:
                                    self.mino[xdraw][ydraw] = 7
                        if self.form !=0:
                            self.y+=self.RotPattern[self.direction%4][direcheck][i][0]
                            self.x+=self.RotPattern[self.direction%4][direcheck][i][1]
                        elif self.form ==0:
                            self.y+=self.RotPatternI[self.direction%4][direcheck][i][0]
                            self.x+=self.RotPatternI[self.direction%4][direcheck][i][1]
                        self.direction += adddire
                        self.mino=[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]]
                        for RotI in range(len(self.mino_data[self.form][self.direction % 4])):
                            
                            Gy = self.mino_data[self.form][self.direction % 4][RotI][0]                                            #この３行で一ブロックを生成(？)恐らく、mino_dataの[form][direction%4]がrnd=3と仮定するとoミノの一番上の配列となりそれのi番目の0番目をここでみて
                            Gx = self.mino_data[self.form][self.direction % 4][RotI][1]                                            #この行でdirection=1番目の1番目の数値を検出して
                            self.mino[Gy][Gx] = self.form  
                        if self.form==5:
                            self.spincheck=true
                        self.senddata=[0,self.playernum,7,[self.y,self.x,self.form,self.mino,1]]
                        threadsend=threading.Thread(target=tcpsend(self.senddata))
                        threadsend.start()  
                        for xdraw in range(self.minosize):                                                           #変数vをminosize(ミノの領域)回続ける
                            xdraw1 = (xdraw + self.y - 1) * self.size                                           #上2行でミノ１ブロックの始まり座標と終わり座標を算出(そのためミノの数(v)回同じ処理をして4つミノを成立させる
                            for ydraw in range(self.minosize):                                                       #変数sを用意してもう一度minosize回のループを生成する
                                ydraw1 = (ydraw + self.x - 1) * self.size                                                          #s2にs1+size☆\\前行+一マス当たりのサイズ
                                if self.mino[xdraw][ydraw] == self.form:                                                  #ここでミノ内の座標(4*4の中が)[v][s]がform(今回はrndで3が抽選されているとする)なら
                                       #その１ブロックの始まり座標から終わり座標までをcolors[form]で指定された色にする:要点:今まではミノについての内部処理でその内部情報をここで初めて出力している
                                    if self.haikei[self.y+xdraw+1][self.x+ydraw]!=7:
                                        RotAfterEnd+=1
                           
                        if RotAfterEnd>=1:
                            self.moveend=true
#----------------------------------------------------Len処理
    def TetrisLen(self):
        self.lencntdoublecheck=0
        lenchance=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for LenI in range(20):
        
            for LenJ in range(10):
                if self.haikei[LenI+1][LenJ+1]!=7:
                    lenchance[LenI]+=1
        for LenI in range(20):
        
            if lenchance[LenI]>=10:
                self.lencntdoublecheck+=1
                for LenJ in range(10):
                    self.haikei[LenI+1][LenJ+1]=7
                Dropcnt=20                              #以下動作未テスト
                for Drop in range(LenI):
                    Dropcnt-=1
                    for DropX in range(10):
                        self.haikei[-Drop+LenI+1][DropX+1]=self.haikei[-Drop+LenI][DropX+1]
                        self.haikei[-Drop+LenI][DropX+1]=7
        if self.lencntdoublecheck>=1:
            pygame.mixer.Sound(self.sound[0]).play()
            self.LenAfterDrop(LenI)
            self.Score()
        if self.lencntdoublecheck==0:#8/11
            self.lencnt=0
            if self.lamp!=0:
                if self.playernum==0:
                    damageattwoplayer(self.lamp)
                else:
                    damageatoneplayer(self.lamp)
                self.lamp=0
    

    def LenAfterDrop(self,LenI):#ここで削除後の浮いたミノを落とす
        global lencnt,lencntbef,score,playeronedamage
        self.lencntbef=0#次のlenを判定する
        
        self.ScoreCnt()
        self.lencnt+=1#現在のlen数をカウントする
        if player[1]==1:
            if self.lencnt>=2:
                if self.lencnt<=4:
                    self.lamp+=1
                elif self.lencnt<=6:
                    self.lamp+=2
                elif self.lencnt<=8:
                    self.lamp+=3
                elif self.lencnt<=11:
                    self.lamp+=4
                elif self.lencnt>=12:
                    self.lamp+=5
        else:#elif player[1]==2:
            if self.lencnt>=2:
                if self.lencnt<=4 :
                    self.lamp+=1
                elif self.lencnt<=6:
                    self.lamp+=2
                elif self.lencnt<=8:
                    self.lamp+=3
                elif self.lencnt<=11:
                    self.lamp+=4
                else:
                    self.lamp+=5
        if self.haikei==[[8,7,7,7,7,7,7,7,7,7,7,8],                                 #背景(内部)
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,7,7,7,7,7,7,7,7,7,7,8],
             [8,8,8,8,8,8,8,8,8,8,8,8]]:
            self.lamp+=10
            self.score+=15000
            font4=ft.Font(size=35,family='Menlo')
            tetris=Label(master,text='Perfect',font=font4)
            tetris.place(x=400+self.playernum*300,y=560)
            cv.after(2000,self.tetrisdelete)
        if player[1]==2:
            while playeronedamage>0 and self.lamp>0:
                playeronedamage-=1
                self.lamp-=1
        if self.lencnt>=2:
            self.score=self.score+(500*(self.lencnt))
        
        if self.Tspin!=false and self.lencntdoublecheck!=4:
            self.BtbFlag=false

        self.GraphicRenCnt(self.lencnt)
        #self.HaikeiDraw()
        if self.lencntdoublecheck==1:
            if self.Tspin==true:
                if self.BtbFlag==true:
                    self.lamp+=1
                self.BtbFlag=true
                self.lamp+=2
                if self.Tspinmini==true:
                    self.lamp+=1
                #self.Tspin=false
                #self.Tspinmini=false
                #self.TspinCnt=0


        if self.lencntdoublecheck==2:
            self.lamp+=1
            self.score+=500
            if self.Tspin==true:#TSD判定
                if self.BtbFlag==true:
                    self.lamp+=1
                self.BtbFlag=true
                self.lamp+=3
                if self.Tspinmini==true:
                    self.lamp+=1
                #self.Tspin=false
                #self.Tspinmini=false
                #self.TspinCnt=0


        if self.lencntdoublecheck==3:
            self.lamp+=2
            self.score+=1250
            if self.Tspin==true:
                if self.BtbFlag==true:
                    self.lamp+=1
                self.BtbFlag=true
                self.lamp+=4
                if self.Tspinmini==true:
                    self.lamp+=1
                #self.Tspin=false
                #self.Tspinmini=false
                #self.TspinCnt=0
        if self.lencntdoublecheck==4:
            if self.BtbFlag==true:
                self.lamp+=1
            self.BtbFlag=true
            self.lamp+=4
            self.score+=4000
            cv.after(10,self.tetrismain)
        cv.after(2000,self.tecGraphicDelete)

    def tecGraphicDelete(self):
        cv.delete(f"Tspin{self.playernum}")
        cv.delete(f"BTB{self.playernum}")

    def tetrismain(self):
            cv.create_image(150+self.playernum*900,500,image=self.string[12],tag="tetrisG")
            cv.after(2000,self.tetrisdelete)
            #self.tetrismove+=1

    def tetrisdelete(self):
        cv.delete("tetrisG")

    def GraphicRenCnt(self,lencnt):
        firren=(int(lencnt%10))-1#ren(1桁
        if firren>0:
            lencnt+=1

    def hold(self):
            if self.holdmax==0:
                self.holdcnt+=1
                if self.holdcnt==1:                                                                  #一回目
                    self.holdsave=self.form
                    self.senddata=[0,self.playernum,9,[self.holdsave,self.minohold,0,self.y,self.x,self.mino,self.form]]
                    threadsend=threading.Thread(target=tcpsend(self.senddata))
                    threadsend.start()
                    self.y = -2                             
                    self.x = 4
                    self.direction=0
                    self.MinoRnd()
                elif self.holdcnt>=1:                                                                #二回目以降
                    self.form,self.holdsave=self.holdsave,self.form
                    self.y = -2                             
                    self.x = 4
                    self.direction=0
                    self.HaikeiDraw()
                    self.MinoHold()
            self.HoldMinoDraw()        
            self.holdmax+=1

    def MinoHold(self):                                                                   #変数宣言:global関数 form＆mino
        self.mino=[[7,7,7,7],[7,7,7,7],[7,7,7,7],[7,7,7,7]]                                                                        #formに0~6の乱数を代入する
        for i in range(len(self.mino_data[self.form][self.direction % 4])):                                    #mino_data[form][direction%4]の配列の長さ回繰り返す:初期:direction=0       :現状directionが1~になることはない(3次元配列の構造上direction=回転状態(?)                            
            y = self.mino_data[self.form][self.direction % 4][i][0]                                            #この３行で一ブロックを生成(？)恐らく、mino_dataの[form][direction%4]がrnd=3と仮定するとoミノの一番上の配列となりそれのi番目の0番目をここでみて
            x = self.mino_data[self.form][self.direction % 4][i][1]                                            #この行でdirection=1番目の1番目の数値を検出して
            self.mino[y][x] = self.form
      

    def HoldMinoDraw(self):
        for i in range(len(self.mino_data[self.holdsave][self.direction % 4])):                                    #mino_data[form][direction%4]の配列の長さ回繰り返す:初期:direction=0       :現状directionが1~になることはない(3次元配列の構造上direction=回転状態(?)                            
            y = self.mino_data[self.holdsave][0][i][0]                                            #この３行で一ブロックを生成(？)恐らく、mino_dataの[form][direction%4]がrnd=3と仮定するとoミノの一番上の配列となりそれのi番目の0番目をここでみて
            x = self.mino_data[self.holdsave][0][i][1]                                            #この行でdirection=1番目の1番目の数値を検出して
            self.minohold[y][x] = self.holdsave
            
        #self.senddata=[0,self.playernum,9,[self.holdsave,self.minohold,1]]
        #threadsend=threading.Thread(target=tcpsend(self.senddata))
        #threadsend.start()
        #self.HoldMinoDraw()
        self.nextdraw()
    def Score(self):
        self.score+=1000
    
        self.ScoreCnt()

    def ScoreCnt(self):
        global sc
        if GameOvercnt==0:
            self.senddata=[0,self.playernum,10,[self.score]]
            threadsend=threading.Thread(target=tcpsend(self.senddata))
            threadsend.start()



    def nextdraw(self):
        if GameOvercnt==0:
            for nextblock in range(4):
                for i in range(4):                                    #mino_data[form][direction%4]の配列の長さ回繰り返す:初期:direction=0       :現状directionが1~になることはない(3次元配列の構造上direction=回転状態(?)                            
                    y = self.mino_data[self.next[nextblock]][0][i][0]                                            #この３行で一ブロックを生成(？)恐らく、mino_dataの[form][direction%4]がrnd=3と仮定するとoミノの一番上の配列となりそれのi番目の0番目をここでみて
                    x = self.mino_data[self.next[nextblock]][0][i][1]                                            #この行でdirection=1番目の1番目の数値を検出して
                    self.nextmino[nextblock][y][x] = self.next[nextblock]
            if self.haikeidrawflag==true:
                self.senddata=[0,self.playernum,0,self.haikei,[self.lencnt,self.BtbFlag,self.Tspinmini,self.Tspin,self.lencntdoublecheck,self.holdsave,self.minohold]]
                threadsend=threading.Thread(target=tcpsend(self.senddata))
                threadsend.start()
                self.Tspin=false
                self.Tspinmini=false
                self.TspinCnt=0
            else:
                self.senddata=[0,self.playernum,9,[self.holdsave,self.minohold,1]]
                threadsend=threading.Thread(target=tcpsend(self.senddata))
                threadsend.start()
            self.haikeidrawflag=false
            self.NextMinoDraw_()

    def NextMinoDraw_(self):
        self.senddata=[0,self.playernum,4,[self.mino,self.next,self.nextmino]]
        #print(f'nextdraw:{self.senddata}')
        threadsend=threading.Thread(target=tcpsend(self.senddata))
        threadsend.start()
#------------------------------------------------------------------------------puyopuyo1 player
class puyopuyoplay():
    def __init__(self):
        self.playernum=0
        self.bonus_rensa=[0,0,8,16,32,64,96,128,160,192,224,256,288,320,352,384,416,448,480,512]
        self.bonus_renketu=[0,0,0,0,0,2,3,4,5,6,7,10]
        self.bonus_color=[0,0,3,6,12,24]
        self.bonus_rensa_cnt,bonus_renketu_cnt=0,0
        self.damage=0
        self.damageloopcnt=0
        self.rencntcheck=0
        self.encnt=0
        self.renafterdelete=0
        self.height = 12                         #基盤の縦のマス数
        self.length = 6                         #基盤の横のマス数
        self.size = 50                           #1マスの大きさ
        self.puyosize = 2                        #ミノの(縦横最大の)ブロック数
        self.form,self.direction,self.lencnt,self.candrop,self.holdsave,self.holdmax,self.score=0,0,0,0,0,0,0                  #ミノの種類,ミノの向き,現在のlenカウント       
        self.y = -1                              #ぷよのy座標
        self.x = 2                               #ぷよのx座標(尚、実際の表示ではpuyodetaでの軸がx=1なので3となる
        self.speed = 500                         #落下速度
        self.MAX=0
        self.ren=["0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "ren",
            "score"]
        self.gameover=["0"]
        self.mainhaikei=["0"]
        self.sound=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0]
        self.puyo_color=["red",
                "blue",
                "yellow",
                "green",
                "purple",
                "none",
                "wall",
                0,
                0]
        self.cantmove=false
        self.puyo_color[7]=PhotoImage(file="./picture/puyopuyo/puyo/ojya_mino_mino.png")
        self.puyo_color[8]=PhotoImage(file="./picture/puyopuyo/puyo/atkpuyo_puyo.png")

        self.puyopuyo= [[6,5,5,5,5,5,5,6],#盤面の内部データ
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,5,5,5,5,5,5,6],
                        [6,6,6,6,6,6,6,6]]

        self.puyo_check=     [[0,0,0,0,0,0,0,0],#盤面のチェックデータ
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0]]#1がチェック中2がチェック済み3が削除確定4が残留確定

        self.puyo_data=[[[1,1],[0,1]],#1,1が最初に下に来るぷよなので軸となる
                [[1,1],[1,2]],
                [[1,1],[2,1]],
                [[1,1],[1,0]]]

        self.puyo=[[5,5,5],#現在のぷよのデータを保管する
            [5,5,5],
            [5,5,5]]

        self.puyo_patern=[0,0]#現在＋nextのぷよのパターンを保管
        self.puyo_next1=[0,0]
        self.puyo_next2=[0,0]

    def puyo_Create(self):
        self.puyo_patern[0]=rnd(0,4)
        self.puyo_patern[1]=rnd(0,4)
        self.puyo_next1[0]=rnd(0,4)
        self.puyo_next1[1]=rnd(0,4)
        self.puyo_next2[0]=rnd(0,4)
        self.puyo_next2[1]=rnd(0,4)
        for i in range(self.puyosize):
            y=self.puyo_data[self.direction%4][i][0]
            x=self.puyo_data[self.direction%4][i][1]
            self.puyo[y][x]=self.puyo_patern[i]

    def puyo_Draw(self):
        self.senddata=[1,self.playernum,1,[self.y,self.x,self.puyo_patern,self.puyo]]
        threadsend=threading.Thread(target=tcpsend(self.senddata))
        threadsend.start()

    def HaikeiDraw(self):
        self.senddata=[1,self.playernum,0,self.puyopuyo,[self.puyo_next1,self.puyo_next2]]
        threadsend=threading.Thread(target=tcpsend(self.senddata))
        threadsend.start()
        cv.delete(f"puyo{self.playernum}")
        cv.delete(f"renpuyo{self.playernum}")
        self.puyo_Score()

    def puyo_Drop(self):
        if self.candrop==0 and GameOvercnt==0 and self.cantmove==false:
            self.cantmove=true
            cv.delete(f"renpuyo{self.playernum}")
            whileout=0
            firpuyocan,scopuyocan=self.puyo_Drop_check()
            if firpuyocan==5 and scopuyocan==5:
                #self.puyo_Delete()
                self.y+=1
                self.puyo_Draw()
            elif firpuyocan==5:#二つ目ぷよが落下可能で軸が落下不可の場合
                self.puyopuyo[self.y+self.puyo_data[self.direction%4][1][0]][self.x+self.puyo_data[self.direction%4][1][1]]=self.puyo_patern[1]
                pygame.mixer.Sound("./sound/puyopuyo/drop.ogg").play()
                while True:
                    secondend=self.puyopuyo[self.y+self.puyo_data[self.direction%4][0][0]+1][self.x+self.puyo_data[self.direction%4][0][1]]
                    if secondend!=5:
                        self.puyopuyo[self.y+self.puyo_data[self.direction%4][0][0]][self.x+self.puyo_data[self.direction%4][0][1]]=self.puyo_patern[0]
                        self.puyo_Next()
                        break
                    else:
                        self.y+=1
                    

            elif scopuyocan==5:#二つ目ぷよのみが残った場合
                self.puyopuyo[self.y+self.puyo_data[self.direction%4][0][0]][self.x+self.puyo_data[self.direction%4][0][1]]=self.puyo_patern[0]
                pygame.mixer.Sound("./sound/puyopuyo/drop.ogg").play()
                while True:
                    firstend=self.puyopuyo[self.y+self.puyo_data[self.direction%4][1][0]+1][self.x+self.puyo_data[self.direction%4][1][1]]
                    if firstend!=5:
                        self.puyopuyo[self.y+self.puyo_data[self.direction%4][1][0]][self.x+self.puyo_data[self.direction%4][1][1]]=self.puyo_patern[1]
                        self.puyo_Next()
                        break
                    else:
                        self.y+=1
                    
            
            elif firpuyocan!=5 and scopuyocan!=5:
                pygame.mixer.Sound("./sound/puyopuyo/drop.ogg").play()
                self.puyopuyo[self.y+self.puyo_data[self.direction%4][1][0]][self.x+self.puyo_data[self.direction%4][1][1]]=self.puyo_patern[1]
                self.puyopuyo[self.y+self.puyo_data[self.direction%4][0][0]][self.x+self.puyo_data[self.direction%4][0][1]]=self.puyo_patern[0]
                self.puyo_Next()
            self.cantmove=false
            if self.candrop==0:
                cv.after(self.speed,self.puyo_Drop)

            

    def puyo_Drop_check(self):
        first=self.puyopuyo[self.y+self.puyo_data[self.direction%4][0][0]+1][self.x+self.puyo_data[self.direction%4][0][1]]
        second=self.puyopuyo[self.y+self.puyo_data[self.direction%4][1][0]+1][self.x+self.puyo_data[self.direction%4][1][1]]
        return first,second

    def puyo_Next(self):
        global puyopuyo,x,y,puyo_patern,puyo_next1,puyo_next2,puyo,direction
        self.puyo=[[5,5,5],#データリセット
                [5,5,5],
                [5,5,5]]
        self.puyo_patern[0]=self.puyo_next1[0]
        self.puyo_patern[1]=self.puyo_next1[1]
        self.x,self.y,self.direction=2,-1,0
        for i in range(self.puyosize):
            ypuyo=self.puyo_data[self.direction%4][i][0]
            xpuyo=self.puyo_data[self.direction%4][i][1]
            self.puyo[ypuyo][xpuyo]=self.puyo_patern[i]
        self.puyo_next1[0]=self.puyo_next2[0]
        self.puyo_next1[1]=self.puyo_next2[1]
        self.puyo_next2[0]=rnd(0,4)
        self.puyo_next2[1]=rnd(0,4)
        
        cv.delete(f"puyo{self.playernum}")
        self.HaikeiDraw()
        #puyo_Score()
        self.ren_Check()
            

    def damagepuyo_oneP(self):
        global playeronedamage,playertwodamage
        if player[0]==1:
            while playeronedamage>0 and playertwodamage>0:#相殺
                    playeronedamage-=1
                    playertwodamage-=1
            while puyopuyotwoplay.damage>0 and playertwodamage>0:#相殺
                    puyopuyotwoplay.damage-=1
                    playertwodamage-=1
            OnePlayerReceveDamegeG(0)
            TwoPlayerReceveDamegeG(0)
        self.n=len(self.puyopuyo)
        if playeronedamage<=36:#一度のせり上がりが6段まで
            if playeronedamage<6 and playeronedamage!=0:
                pygame.mixer.Sound(self.sound[1][0]).play()
            elif playeronedamage<=36 and playeronedamage!=0:
                pygame.mixer.Sound(self.sound[1][1]).play()
            self.damageloopcnt=playeronedamage
        else:
            pygame.mixer.Sound(self.sound[1][1]).play()
            self.damageloopcnt=36
        if self.damageloopcnt!=0:
            
            self.damagepuyo__oneP()

    def damagepuyo__oneP(self):
        self.candrop=1
        global playeronedamage
        self.n-=1
        if self.damageloopcnt>=6:
            for x in range(len(self.puyopuyo[self.n])):
                if self.puyopuyo[1][x]==5:
                    if player[0]==1:
                        self.puyopuyo[1][x]=7
                    else:
                        self.puyopuyo[1][x]=8
                    self.damageloopcnt-=1#今回受ける火力の消化
                    playeronedamage-=1#火力の消化
        else:
            for x in range(self.damageloopcnt):#残っている火力(6未満を消化)
                p=rnd(1,6)
                if self.puyopuyo[1][p]==5:
                    if player[0]==1:
                        self.puyopuyo[1][p]=7
                    else:
                        self.puyopuyo[1][p]=8
                    self.damageloopcnt-=1
                    playeronedamage-=1
        for downy in range(len(self.puyopuyo)):
            for x in range(len(self.puyopuyo[self.n])):
                if self.puyopuyo[len(self.puyopuyo)-1-downy][x]==7 or self.puyopuyo[len(self.puyopuyo)-1-downy][x]==8:
                    if self.puyopuyo[len(self.puyopuyo)-1-(downy)+1][x]==5:
                        self.puyopuyo[len(self.puyopuyo)-1-downy][x]=5
                        if player[0]==1:
                            self.puyopuyo[len(self.puyopuyo)-1-(downy)+1][x]=7
                        else:
                            self.puyopuyo[len(self.puyopuyo)-1-(downy)+1][x]=8#-1は最下段を見る必要がない+1は一つ下を見る(相殺できるが分かりやすく)
        self.HaikeiDraw()
        if self.n!=0:
            cv.after(20,self.damagepuyo__oneP)
        else:
            self.candrop=0
            cv.after(50,self.puyo_Drop)
            OnePlayerReceveDamegeG(0)
        


    def damagepuyo_twoP(self):
        global playeronedamage,playertwodamage

        if player[1]==1:
            while playeronedamage>0 and playertwodamage>0:#相殺
                    playeronedamage-=1
                    playertwodamage-=1
            while puyopuyooneplay.damage>0 and playeronedamage>0:#相殺
                    puyopuyooneplay.damage-=1
                    playeronedamage-=1
            OnePlayerReceveDamegeG(0)
            TwoPlayerReceveDamegeG(0)
        self.n=len(self.puyopuyo)
        if playertwodamage<=36:#一度のせり上がりが6段まで
            if playertwodamage<6 and playertwodamage!=0:
                pygame.mixer.Sound(self.sound[1][0]).play()
            elif playertwodamage<=36 and playertwodamage!=0:
                pygame.mixer.Sound(self.sound[1][1]).play()
            self.damageloopcnt=playertwodamage
        else:
            pygame.mixer.Sound(self.sound[1][1]).play()
            self.damageloopcnt=36
        if self.damageloopcnt!=0:
            self.damagepuyo__twoP()
            

    def damagepuyo__twoP(self):
        self.candrop=1
        global playertwodamage
        #senddata=[1,self.playernum,13,[self.puyopuyo,self.n,self.damageloopcnt,player]]
        self.n-=1
        if self.damageloopcnt>=6:
            for x in range(len(self.puyopuyo[self.n])):
                if self.puyopuyo[1][x]==5:
                    if player[0]==1:
                        self.puyopuyo[1][x]=7
                    else:
                        self.puyopuyo[1][x]=8
                    self.damageloopcnt-=1#今回受ける火力の消化
                    playertwodamage-=1#火力の消化
        else:
            for x in range(self.damageloopcnt):#残っている火力(6未満を消化)
                p=rnd(1,6)
                if self.puyopuyo[1][p]==5:
                    if player[0]==1:
                        self.puyopuyo[1][p]=7
                    else:
                        self.puyopuyo[1][p]=8
                    self.damageloopcnt-=1
                    playertwodamage-=1
        for downy in range(len(self.puyopuyo)):
            for x in range(len(self.puyopuyo[self.n])):
                if self.puyopuyo[len(self.puyopuyo)-1-downy][x]==7 or self.puyopuyo[len(self.puyopuyo)-1-downy][x]==8:
                    if self.puyopuyo[len(self.puyopuyo)-1-(downy)+1][x]==5:
                        self.puyopuyo[len(self.puyopuyo)-1-downy][x]=5
                        if player[0]==1:
                            self.puyopuyo[len(self.puyopuyo)-1-(downy)+1][x]=7
                        else:
                            self.puyopuyo[len(self.puyopuyo)-1-(downy)+1][x]=8#-1は最下段を見る必要がない+1は一つ下を見る(相殺できるが分かりやすく)
        self.HaikeiDraw()
        if self.n!=0:
            cv.after(20,self.damagepuyo__twoP)
        else:
            self.candrop=0
            cv.after(50,self.puyo_Drop)
            TwoPlayerReceveDamegeG(0)
        
    #----------------------------------------------------------------------------------------------------------------------------------操作処理
    def puyo_Move(self,adddire,addy,addx):
        global direction,puyo_data,y,x,puyo
        rotcheck=[5,5]
        rotcheck[0]=self.puyopuyo[self.y+self.puyo_data[(self.direction+adddire)%4][0][0]+addy][self.x+self.puyo_data[(self.direction+adddire)%4][0][1]+addx]
        rotcheck[1]=self.puyopuyo[self.y+self.puyo_data[(self.direction+adddire)%4][1][0]+addy][self.x+self.puyo_data[(self.direction+adddire)%4][1][1]+addx]
        if rotcheck[0]==5 and rotcheck[1]==5:
            #self.puyo_Delete()
            if adddire!=0:
                pygame.mixer.Sound("./sound/puyopuyo/rot.ogg").play()
                self.puyo=[[5,5,5],#データリセット
                    [5,5,5],
                    [5,5,5]]
                self.direction+=adddire
                self.y+=addy
                for i in range(self.puyosize):
                    puyoy=self.puyo_data[self.direction%4][i][0]
                    puyox=self.puyo_data[self.direction%4][i][1]
                    self.puyo[puyoy][puyox]=self.puyo_patern[i]
            if addy!=0:
                self.y+=addy
            if addx!=0:
                pygame.mixer.Sound("./sound/puyopuyo/move.ogg").play()
                self.x+=addx
            self.puyo_Draw()
        elif self.direction%2==0:
            if adddire!=0:
                #self.puyo_Delete()
                self.puyo=[[5,5,5],#データリセット
                        [5,5,5],
                        [5,5,5]]
                if self.puyopuyo[self.y+self.puyo_data[(self.direction)%4][0][0]][self.x+self.puyo_data[(self.direction)%4][0][1]+1]!=5 and self.puyopuyo[self.y+self.puyo_data[(self.direction)%4][1][0]][self.x+self.puyo_data[(self.direction)%4][1][1]+1]!=5 and self.puyopuyo[self.y+self.puyo_data[(self.direction+2)%4][0][0]][self.x+self.puyo_data[(self.direction+2)%4][0][1]]==5 and self.puyopuyo[self.y+self.puyo_data[(self.direction+2)%4][1][0]][self.x+self.puyo_data[(self.direction+2)%4][1][1]]==5:
                    self.direction+=2
                elif self.puyopuyo[self.y+self.puyo_data[(self.direction)%4][0][0]][self.x+self.puyo_data[(self.direction)%4][0][1]-1]!=5 and self.puyopuyo[self.y+self.puyo_data[(self.direction)%4][1][0]][self.x+self.puyo_data[(self.direction)%4][1][1]-1]!=5 and self.puyopuyo[self.y+self.puyo_data[(self.direction+2)%4][0][0]][self.x+self.puyo_data[(self.direction+2)%4][0][1]]==5 and self.puyopuyo[self.y+self.puyo_data[(self.direction+2)%4][1][0]][self.x+self.puyo_data[(self.direction+2)%4][1][1]]==5:
                    self.direction+=2
                for i in range(self.puyosize):
                    puyoy=self.puyo_data[self.direction%4][i][0]
                    puyox=self.puyo_data[self.direction%4][i][1]
                    self.puyo[puyoy][puyox]=self.puyo_patern[i]
                self.puyo_Draw()

    #-----------------------------------------------------------------------------------------------------------------------------------回転
    def right_Rot(self):
        if self.renafterdelete==0 and GameOvercnt==0:
            self.puyo_Move(1,0,0)

    def left_Rot(self):
        if self.renafterdelete==0 and GameOvercnt==0:
            self.puyo_Move(-1,0,0)
    #-----------------------------------------------------------------------------------------------------------------------------------移動
    def down_Move(self):
        if self.renafterdelete==0 and GameOvercnt==0:
            self.puyo_Move(0,1,0)

    def right_Move(self):
        if self.renafterdelete==0 and GameOvercnt==0:
            self.puyo_Move(0,0,1)

    def left_Move(self):
        if self.renafterdelete==0 and GameOvercnt==0:
            self.puyo_Move(0,0,-1)
    #--------------------------------------------------------------------------------------------------------------------------ren処理
    def ren_Check(self):
        self.puyo_check=[[0,0,0,0,0,0,0,0],#盤面のチェックデータ
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]#1がチェック中2がチェック済み3が削除確定4が残留確定

        self.bonus_renketu_cnt=[[0,0,0,0,0,0,0,0],#盤面のチェックデータ
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]
        color_bonus_check_sec=[0,0,0,0,0]
        checkx,checky,cnt,self.renafterdelete,can,puyo_delete_cnt,bonus_color_cnt,bonus_renketu_cnt_final=1,1,0,0,0,0,0,0
        for checky in range(12):                                                                                             #全てのマスを基点として検索
            for checkx in range(6):

                if self.puyopuyo[checky+1][checkx+1]!=5 and self.puyopuyo[checky+1][checkx+1]!=6 and self.puyo_check[checky+1][checkx+1]==0 and self.puyopuyo[checky+1][checkx+1]!=7 and self.puyopuyo[checky+1][checkx+1]!=8:#判定するマスにぷよがいるかを判定
                    cnt,breakpoint=0,0
                    self.checkpuyo=self.puyopuyo[checky+1][checkx+1]
                    self.puyo_check[checky+1][checkx+1]=1
                    while True:
                        breakpoint=self.ren_check_check(breakpoint)
                        if breakpoint==1:
                            break
                    
                    for tchecky in range(12):                                                                                #以後基点からつながっているぷよを検索
                        for tcheckx in range(6):
                            if self.puyo_check[tchecky+1][tcheckx+1]==2:
                                cnt+=1
                    
                    if cnt>=4:#4つ以上つながっていた時
                        for tchecky in range(12):                                                                                #以後基点からつながっているぷよを検索
                            for tcheckx in range(6):
                                if self.puyo_check[tchecky+1][tcheckx+1]==2:
                                    self.puyo_check[tchecky+1][tcheckx+1]=3
                                    bonus_color_check=self.puyopuyo[tchecky+1][tcheckx+1]
                                    color_bonus_check_sec[bonus_color_check]=1####削除色検知
                                    self.bonus_renketu_cnt[checky+1][checkx+1]+=1####連結数検知
                                    
                    else:#4つ以上つながっていなかったとき
                        for tchecky in range(12):                                                                                #以後基点からつながっているぷよを検索
                            for tcheckx in range(6):
                                if self.puyo_check[tchecky+1][tcheckx+1]==2:
                                    self.puyo_check[tchecky+1][tcheckx+1]=0
        for i in range(5):
            if color_bonus_check_sec[i]==1:
                bonus_color_cnt+=1
        for i in range(12):
            for j in range(6):
                if bonus_renketu_cnt_final<self.bonus_renketu_cnt[i+1][j+1]:
                    bonus_renketu_cnt_final=self.bonus_renketu_cnt[i+1][j+1]
        for tchecky in range(12):                                                                                #点滅用
            for tcheckx in range(6):
                if self.puyo_check[tchecky+1][tcheckx+1]==3:
                    puyo_delete_cnt+=1
                    self.renafterdelete=1
                    self.candrop=1#false
                    if self.rencntcheck<1:
                        self.lencnt+=1
                        pygame.mixer.Sound(self.sound[0][self.lencnt]).play()#ren音再生
                        
                        
                        
                        self.rencntcheck+=1
                else:
                    if self.candrop==1:
                        can+=1



        self.senddata=[1,self.playernum,2,[self.puyo_check,self.lencnt,self.puyopuyo]]
        threadsend=threading.Thread(target=tcpsend(self.senddata))
        threadsend.start()




        cv.after(200,self.puyo_Blinking)
        if can==72:
            self.candrop,self.renafterdelete=0,0
            self.lencnt=0
            cv.after(self.speed,self.puyo_Drop)
        if self.renafterdelete==1:
            addscore=puyo_delete_cnt*(self.bonus_rensa[self.lencnt]+self.bonus_renketu[bonus_renketu_cnt_final]+self.bonus_color[bonus_color_cnt])*10
            print(f'消した数:{puyo_delete_cnt},連鎖ボーナス:{self.bonus_rensa[self.lencnt]},連結ボーナス:{self.bonus_renketu[bonus_renketu_cnt_final]},色ボーナス:{self.bonus_color[bonus_color_cnt]}')
            self.damage+=int(addscore/70)
            if self.playernum==0:
                TwoPlayerReceveDamegeG(self.damage)
            if self.playernum==1:
                OnePlayerReceveDamegeG(self.damage)
            self.score+=addscore
            cv.delete("scoreone")
            self.puyo_Score()
            cv.after(400,self.puyo_blinkingafter)
        if self.lencnt==0:
            
            if self.puyopuyo[1][3]!=5:
                GameOver(self.playernum+1)#チェック
                return
            if self.playernum==0:#player1がプレイしているなら
                damageattwoplayer(self.damage)
                self.damagepuyo_oneP()
            elif self.playernum==1:#player2がプレイしているなら
                damageatoneplayer(self.damage)
                self.damagepuyo_twoP()
            #tmppin
            self.damage=0
        
    def puyo_blinkingafter(self):
        global rencntcheck,rencnt
        for tchecky in range(12):                                                                               #以後3を削除(ren確定ぷよを削除
            for tcheckx in range(6):
                if self.puyo_check[tchecky+1][tcheckx+1]==3:
                    self.puyo_check[tchecky+1][tcheckx+1]=0
                    self.puyopuyo[tchecky+1][tcheckx+1]=5###7以降に消えた後のぷよのpngをセットして+=7に変更する
                    if self.puyopuyo[tchecky+1+1][tcheckx+1]==7 or self.puyopuyo[tchecky+1+1][tcheckx+1]==8:
                        self.puyopuyo[tchecky+1+1][tcheckx+1]=5
                    if self.puyopuyo[tchecky+1-1][tcheckx+1]==7 or self.puyopuyo[tchecky+1-1][tcheckx+1]==8:
                        self.puyopuyo[tchecky+1-1][tcheckx+1]=5
                    if self.puyopuyo[tchecky+1][tcheckx+1+1]==7 or self.puyopuyo[tchecky+1][tcheckx+1+1]==8:
                        self.puyopuyo[tchecky+1][tcheckx+1+1]=5
                    if self.puyopuyo[tchecky+1][tcheckx+1-1]==7 or self.puyopuyo[tchecky+1][tcheckx+1-1]==8:
                        self.puyopuyo[tchecky+1][tcheckx+1-1]=5
                    

        if GameOvercnt==1:
            self.HaikeiDraw()
        cv.after(self.speed,self.Ren_Drop)

    def puyo_Blinking(self):

        for tchecky in range(12):                                                                                #点滅用
            for tcheckx in range(6):
                if self.puyo_check[tchecky+1][tcheckx+1]==3:
                    cv.create_image(tcheckx*self.size+327-300+self.playernum*900,tchecky*self.size+27 ,image=self.puyo_color[self.puyopuyo[tchecky+1][tcheckx+1]],tag=f"puyo{self.playernum}")
                    self.gocheck=1

    def ren_check_check(self,breakpoint):#そのぷよの周囲に同じぷよがあるかを判定し続ける
        global puyo_check,checkpuyo,ren
        breakcnt=0
        for dy in range(12):
                for dx in range(6):
                    breakpoint,rene=0,0
                    if self.puyo_check[dy+1][dx+1]==1:
                        if self.puyopuyo[dy+1+1][dx+1]==self.checkpuyo and self.puyo_check[dy+1+1][dx+1]!=2 and self.puyo_check[dy+1+1][dx+1]!=3:#ここからで周囲に同じ色があって判定済みでなければ
                            self.puyo_check[dy+1][dx+1]=2#自分自身を2にして
                            self.puyo_check[dy+1+1][dx+1]=1#該当ぷよを1にする
                        if self.puyopuyo[dy+1-1][dx+1]==self.checkpuyo and self.puyo_check[dy+1-1][dx+1]!=2 and self.puyo_check[dy+1-1][dx+1]!=3:
                            self.puyo_check[dy+1][dx+1]=2
                            self.puyo_check[dy+1-1][dx+1]=1
                        if self.puyopuyo[dy+1][dx+1+1]==self.checkpuyo and self.puyo_check[dy+1][dx+1+1]!=2 and self.puyo_check[dy+1][dx+1+1]!=3:
                            self.puyo_check[dy+1][dx+1]=2
                            self.puyo_check[dy+1][dx+1+1]=1
                        if self.puyopuyo[dy+1][dx+1-1]==self.checkpuyo and self.puyo_check[dy+1][dx+1-1]!=2 and self.puyo_check[dy+1][dx+1-1]!=3:
                            self.puyo_check[dy+1][dx+1]=2
                            self.puyo_check[dy+1][dx+1-1]=1
                        self.puyo_check[dy+1][dx+1]=2
                    else:
                        breakcnt+=1
                        if breakcnt==72:#全てが1で無ければ
                            breakpoint=1
                            return breakpoint

    def Ren_Drop(self):
        renendcheck,renendcheck_main=0,0

        for ty in range(12):
            for tx in range(6):
                if self.puyopuyo[12-ty][6-tx]!=5:#現在のマスにぷよがあれば
                    renendcheck+=1
                    if self.puyopuyo[(12-ty)+1][6-tx]==5:#⇑のマスから下のマスが開いているかを検知
                        dropcolor=self.puyo_color[self.puyopuyo[12-ty][6-tx]]#trueならpuyo_colorからぷよの種類データをdropcolorに代入
                        intdropcolor=self.puyopuyo[12-ty][6-tx]
                        self.puyopuyo[12-ty][6-tx]=5#現在のマスを空白にする
                        self.puyopuyo[(12-ty)+1][6-tx]=intdropcolor#一マス下に移動
                    else:
                        renendcheck_main+=1#下のマスが開いてなければ
        self.HaikeiDraw()#全て落ちた時に描写
        if renendcheck==renendcheck_main:#renendcheckは全てのぷよ数renendcheck_mainは下が開いていないすべてのぷよなので一致するとき全ての落下可能ぷよが存在しない
            ###レンカウント候補
            self.rencntcheck=0
            self.ren_Check()
            return
        cv.after(100,self.Ren_Drop)


    def puyo_Score(self):
        self.senddata=[1,self.playernum,3,[self.score]]
        threadsend=threading.Thread(target=tcpsend(self.senddata))
        threadsend.start()
    
    def main(self):
        #gameend=Tk()
        #gameend.title('GameOver!!')
        self.puyo_color[0]=PhotoImage(file="./picture/puyopuyo/puyo/red_puyo.png")
        self.puyo_color[1]=PhotoImage(file="./picture/puyopuyo/puyo/blue_puyo.png")
        self.puyo_color[2]=PhotoImage(file="./picture/puyopuyo/puyo/yellow_puyo.png")
        self.puyo_color[3]=PhotoImage(file="./picture/puyopuyo/puyo/green_puyo.png")
        self.puyo_color[4]=PhotoImage(file="./picture/puyopuyo/puyo/purple_puyo.png")
        self.puyo_color[5]=PhotoImage(file="./picture/puyopuyo/puyo/none.png")
        self.puyo_color[6]=PhotoImage(file="./picture/puyopuyo/puyo/wall.png")
        self.ren[0]=PhotoImage(file="./picture/puyopuyo/word/0.png")
        self.ren[1]=PhotoImage(file="./picture/puyopuyo/word/1.png")
        self.ren[2]=PhotoImage(file="./picture/puyopuyo/word/2.png")
        self.ren[3]=PhotoImage(file="./picture/puyopuyo/word/3.png")
        self.ren[4]=PhotoImage(file="./picture/puyopuyo/word/4.png")
        self.ren[5]=PhotoImage(file="./picture/puyopuyo/word/5.png")
        self.ren[6]=PhotoImage(file="./picture/puyopuyo/word/6.png")
        self.ren[7]=PhotoImage(file="./picture/puyopuyo/word/7.png")
        self.ren[8]=PhotoImage(file="./picture/puyopuyo/word/8.png")
        self.ren[9]=PhotoImage(file="./picture/puyopuyo/word/9.png")
        self.ren[10]=PhotoImage(file="./picture/puyopuyo/word/renstring.png")
        self.ren[11]=PhotoImage(file="./picture/puyopuyo/word/score.png")
        #本家版(音が混じってる)
        #self.sound[0][1]=pygame.mixer.Sound("./sound/puyopuyo/1ren.mp3")
        #self.sound[0][2]=pygame.mixer.Sound("./sound/puyopuyo/2ren.mp3")
        #self.sound[0][3]=pygame.mixer.Sound("./sound/puyopuyo/3ren.mp3")
        #self.sound[0][4]=pygame.mixer.Sound("./sound/puyopuyo/4ren.mp3")
        #self.sound[0][5]=pygame.mixer.Sound("./sound/puyopuyo/5ren.mp3")
        #self.sound[0][6]=pygame.mixer.Sound("./sound/puyopuyo/6ren.mp3")
        #self.sound[0][7]=pygame.mixer.Sound("./sound/puyopuyo/7ren.mp3")
        #self.sound[0][8]=pygame.mixer.Sound("./sound/puyopuyo/8ren.mp3")
        #self.sound[0][9]=pygame.mixer.Sound("./sound/puyopuyo/9ren.mp3")
        #self.sound[0][10]=pygame.mixer.Sound("./sound/puyopuyo/10ren.mp3")
        #self.sound[0][11]=pygame.mixer.Sound("./sound/puyopuyo/11ren.mp3")
        #self.sound[0][12]=pygame.mixer.Sound("./sound/puyopuyo/12ren.mp3")
        #self.sound[0][13]=pygame.mixer.Sound("./sound/puyopuyo/13ren.mp3")
        #self.sound[0][14]=pygame.mixer.Sound("./sound/puyopuyo/14ren.mp3")
        #self.sound[1][0]=pygame.mixer.Sound("./sound/puyopuyo/ojyamamin.mp3")
        #ぷよクエ版(apkから引用)
        self.sound[0][1]=pygame.mixer.Sound("./sound/puyopuyo/se_ing01_ren01.ogg")
        self.sound[0][2]=pygame.mixer.Sound("./sound/puyopuyo/se_ing02_ren02.ogg")
        self.sound[0][3]=pygame.mixer.Sound("./sound/puyopuyo/se_ing03_ren03.ogg")
        self.sound[0][4]=pygame.mixer.Sound("./sound/puyopuyo/se_ing04_ren04.ogg")
        self.sound[0][5]=pygame.mixer.Sound("./sound/puyopuyo/se_ing05_ren05.ogg")
        self.sound[0][6]=pygame.mixer.Sound("./sound/puyopuyo/se_ing06_ren06.ogg")
        self.sound[0][7]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][8]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][9]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][10]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][11]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][12]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][13]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][14]=pygame.mixer.Sound("./sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[1][0]=pygame.mixer.Sound("./sound/puyopuyo/ojyamamin.ogg")
        self.sound[1][1]=pygame.mixer.Sound("./sound/puyopuyo/ojyamamax.ogg")
        self.puyo_Create()
        self.HaikeiDraw()
        self.puyo_Score()
        self.puyo_Draw()
        self.puyo_Drop()


        #playeronedamageはプレイヤー1が受けるダメージ
#------------------------------------------------------------------------------
def damageatoneplayer(damage):#プレイヤー1に火力を送る#条件:puyo→連鎖が途切れた時
    global playeronedamage,playertwodamage
    if player[1]==2:#プレイヤー2がぷよぷよで
        if player[0]==1:
            damage=int(damage/4)
            for d in range(damage):
                playeronedamage+=1#この数値を元にプレイヤー1側のコードで火力を受ける
        if player[0]==2:
            playeronedamage+=damage
            while playeronedamage>0 and puyopuyooneplay.damage>0:
                playeronedamage-=1
                puyopuyooneplay.damage-=1
            while playertwodamage>0 and playeronedamage>0:
                playertwodamage-=1
                playeronedamage-=1
            TwoPlayerReceveDamegeG(0)
    else:#プレイヤー2がtetrisで
        if player[0]==1:
            playeronedamage+=damage
            
            while playeronedamage>0 and tetrisoneplay.lamp>0:#相殺 tetrisplayone.lampは1側のたまっている火力
                playeronedamage-=1#受けるダメージ
                tetrisoneplay.lamp-=1#2プレイヤーに与えるはずだったダメージ
        if player[0]==2:#相手がぷよなら
           
           playeronedamage+=tetrisatklist[damage]
    OnePlayerReceveDamegeG(0)

def damageattwoplayer(damage):#プレイヤー2に火力を送る#条件:puyo→連鎖が途切れた時
    global playertwodamage,playeronedamage
    if player[0]==2:#プレイヤー1がぷよぷよで
        if player[1]==1:#相手がテトリスなら
            damage=int(damage/4)
            for d in range(damage):
                playertwodamage+=1#この数値を元にプレイヤー2側のコードで火力を受ける
        if player[1]==2:
            playertwodamage+=damage
            while playertwodamage>0 and puyopuyotwoplay.damage>0:
                playertwodamage-=1
                puyopuyotwoplay.damage-=1
            while playertwodamage>0 and playeronedamage>0:
                playertwodamage-=1
                playeronedamage-=1
            OnePlayerReceveDamegeG(0)
    else:#プレイヤー1がtetrisで
        if player[1]==1:
            playertwodamage+=damage
            while tetristwoplay.lamp>0 and playertwodamage>0:#相殺
                tetristwoplay.lamp-=1
                playertwodamage-=1
        if player[1]==2:#相手がぷよなら
            playertwodamage+=tetrisatklist[damage]
    TwoPlayerReceveDamegeG(0)

def OnePlayerReceveDamegeG(lamp):
    global playeronedamage,playertwodamage
    cv.delete("damage1")
    GraMax=0
    if player[1]==1:
        if player[0]==1:
            graphicsdamage=playeronedamage
        elif player[0]==2:
            graphicsdamage=playeronedamage+tetrisatklist[lamp]
    elif player[1]==2:
        if player[0]==1:
            graphicsdamage=playeronedamage+int(lamp/4)
        elif player[0]==2:
            graphicsdamage=playeronedamage+lamp
    senddata=[50,15,[graphicsdamage,player[1]]]
    threadsend=threading.Thread(target=tcpsend(senddata))
    threadsend.start()
    oukan=int(graphicsdamage/720)
    graphicsdamage=graphicsdamage%720
    moon=int(graphicsdamage/360)
    graphicsdamage=graphicsdamage%320
    star=int(graphicsdamage/180)
    graphicsdamage=graphicsdamage%180
    rock=int(graphicsdamage/30)
    graphicsdamage=graphicsdamage%30
    large=int(graphicsdamage/6)
    small=graphicsdamage%6
    if player[0]==1:
        for g in range(oukan):
            if GraMax<6:
                cv.create_image(450-(GraMax*30),400,image=ojyamino[5],tag="damage1")
                GraMax+=1
        for g in range(moon):
            if GraMax<6:
                cv.create_image(450-(GraMax*30),400,image=ojyamino[4],tag="damage1")
                GraMax+=1
        for g in range(star):
            if GraMax<6:
                cv.create_image(450-(GraMax*30),400,image=ojyamino[3],tag="damage1")
                GraMax+=1
        for g in range(rock):
            if GraMax<6:
                cv.create_image(450-(GraMax*30),400,image=ojyamino[2],tag="damage1")
                GraMax+=1
        for g in range(large):
            if GraMax<6:
                cv.create_image(450-(GraMax*30),400,image=ojyamino[1],tag="damage1")
                GraMax+=1
        for g in range(small):
            if GraMax<6:
                cv.create_image(450-(GraMax*30),400,image=ojyamino[0],tag="damage1")
                GraMax+=1
    elif player[0]==2:
        for g in range(oukan):
            if GraMax<6:
                cv.create_image(565-(GraMax*30),400,image=ojyapuyo[5],tag="damage1")
                GraMax+=1
        for g in range(moon):
            if GraMax<6:
                cv.create_image(565-(GraMax*30),400,image=ojyapuyo[4],tag="damage1")
                GraMax+=1
        for g in range(star):
            if GraMax<6:
                cv.create_image(565-(GraMax*30),400,image=ojyapuyo[3],tag="damage1")
                GraMax+=1
        for g in range(rock):
            if GraMax<6:
                cv.create_image(565-(GraMax*30),400,image=ojyapuyo[2],tag="damage1")
                GraMax+=1
        for g in range(large):
            if GraMax<6:
                cv.create_image(565-(GraMax*30),400,image=ojyapuyo[1],tag="damage1")
                GraMax+=1
        for g in range(small):
            if GraMax<6:
                cv.create_image(565-(GraMax*30),400,image=ojyapuyo[0],tag="damage1")
                GraMax+=1


def TwoPlayerReceveDamegeG(lamp):
    global playeronedamage,playertwodamage
    cv.delete("damage2")
    GraMax=0
    if player[1]==1:
        if player[0]==1:
            graphicsdamage=playertwodamage
        elif player[0]==2:
            graphicsdamage=playertwodamage+tetrisatklist[lamp]
    elif player[1]==2:
        if player[0]==1:
            graphicsdamage=playertwodamage+int(lamp/4)
        elif player[0]==2:
            graphicsdamage=playertwodamage+lamp
    print('senddata')
    senddata=[50,14,[graphicsdamage,player[0]]]
    threadsend=threading.Thread(target=tcpsend(senddata))
    threadsend.start()
    oukan=int(graphicsdamage/720)
    graphicsdamage=graphicsdamage%720
    moon=int(graphicsdamage/360)
    graphicsdamage=graphicsdamage%320
    star=int(graphicsdamage/180)
    graphicsdamage=graphicsdamage%180
    rock=int(graphicsdamage/30)
    graphicsdamage=graphicsdamage%30
    large=int(graphicsdamage/6)
    small=graphicsdamage%6
    if player[0]==1:
        for g in range(oukan):
            if GraMax<6:
                cv.create_image(750-(GraMax*30),400,image=ojyamino[5],tag="damage2")
                GraMax+=1
        for g in range(moon):
            if GraMax<6:
                cv.create_image(750-(GraMax*30),400,image=ojyamino[4],tag="damage2")
                GraMax+=1
        for g in range(star):
            if GraMax<6:
                cv.create_image(750-(GraMax*30),400,image=ojyamino[3],tag="damage2")
                GraMax+=1
        for g in range(rock):
            if GraMax<6:
                cv.create_image(750-(GraMax*30),400,image=ojyamino[2],tag="damage2")
                GraMax+=1
        for g in range(large):
            if GraMax<6:
                cv.create_image(750-(GraMax*30),400,image=ojyamino[1],tag="damage2")
                GraMax+=1
        for g in range(small):
            if GraMax<6:
                cv.create_image(750-(GraMax*30),400,image=ojyamino[0],tag="damage2")
                GraMax+=1
    elif player[0]==2:
        for g in range(oukan):
            if GraMax<6:
                cv.create_image(865-(GraMax*30),400,image=ojyapuyo[5],tag="damage2")
                GraMax+=1
        for g in range(moon):
            if GraMax<6:
                cv.create_image(865-(GraMax*30),400,image=ojyapuyo[4],tag="damage2")
                GraMax+=1
        for g in range(star):
            if GraMax<6:
                cv.create_image(865-(GraMax*30),400,image=ojyapuyo[3],tag="damage2")
                GraMax+=1
        for g in range(rock):
            if GraMax<6:
                cv.create_image(865-(GraMax*30),400,image=ojyapuyo[2],tag="damage2")
                GraMax+=1
        for g in range(large):
            if GraMax<6:
                cv.create_image(865-(GraMax*30),400,image=ojyapuyo[1],tag="damage2")
                GraMax+=1
        for g in range(small):
            if GraMax<6:
                cv.create_image(865-(GraMax*30),400,image=ojyapuyo[0],tag="damage2")
                GraMax+=1


def GameOver(winplayer):
    global GameOvercnt,sc,sc2
    GameOvercnt=1#false
    cv.delete("all")
    gameoverdata=[5,winplayer]
    threading.Thread(target=tcpsend(gameoverdata)).start
    #initialize()
    #gameover[0]=PhotoImage(file="gameover.png")
    #font3=ft.Font(size=30,family='System')
    #cv.create_text(100,70,text=f"player{winplayer} win!!",font=font3)



def tcpreceive():
    global getip
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((ip_address,port))
        s.listen(2)#自分自身のipで2ipの受付
        
        while True:
            
            connect,address=s.accept()
            
            
            data=connect.recv(1024)
            data=pickle.loads(data)
            if getip[0][1]==0:
                getip[0][0]=data[1]
                getip[0][1]=data[2]
            elif getip[0][1]!=data[2]:
                getip[1][0]=data[1]
                getip[1][1]=data[2]
            TcpMoveThread=threading.Thread(target=TcpDataExecute(data))
            TcpMoveThread.start()

def TcpDataExecute(data):
    global gamestartflag
    if data[0]==99:
        if getip[1][0]==0:
            playernum=threading.Thread(playernumsend1([99,1]))
            playernum.start()
        elif getip[1][0]!=0:
            playernum=threading.Thread(playernumsend2([99,2]))
            playernum.start()

    elif data[0][0]==2:
        if data[0][1]==0:#上矢印入力があったなら
            if player[1]==1:
                movethread=threading.Thread(tetristwoplay.MinoMoveKey(0,0,0,1))
                movethread.start()
        elif data[0][1]==1:#右矢印入力があったなら
            if player[1]==2:
                movethread=threading.Thread(puyopuyotwoplay.right_Move())
                movethread.start()
            else:
                movethread=threading.Thread(tetristwoplay.MinoMoveKey(0,0,1,0))
                movethread.start()
        elif data[0][1]==2:#下矢印入力があったなら
            if player[1]==2:
                movethread=threading.Thread(puyopuyotwoplay.down_Move())
                movethread.start()
            else:
                movethread=threading.Thread(tetristwoplay.MinoMoveKey(0,1,0,0))
                movethread.start()
        elif data[0][1]==3:#左矢印入力があったなら
            if player[1]==2:
                movethread=threading.Thread(puyopuyotwoplay.left_Move())
                movethread.start()
            else:
                movethread=threading.Thread(tetristwoplay.MinoMoveKey(0,0,-1,0))
                movethread.start()
        elif data[0][1]==4:#a矢印入力があったなら
            if player[1]==2:
                movethread=threading.Thread(puyopuyotwoplay.left_Rot())
                movethread.start()
            else:
                movethread=threading.Thread(tetristwoplay.MinoMoveKey(1,0,0,0))
                movethread.start()
                time.sleep(0.1)
        elif data[0][1]==5:#s矢印入力があったなら
            if player[1]==1:
                movethread=threading.Thread(tetristwoplay.hold())
                movethread.start()
        elif data[0][1]==6:#d矢印入力があったなら
            if player[1]==2:
                movethread=threading.Thread(puyopuyotwoplay.right_Rot())
                movethread.start()
            else:
                movethread=threading.Thread(tetristwoplay.MinoMoveKey(-1,0,0,0))
                movethread.start()
                time.sleep(0.1)
        elif data[0][1]==[3,0]:
            tetristwo()
        elif data[0][1]==[3,1]:
            puyopuyotwo()
        elif data[0][1]==[3,2]:
            gamestartbef()
            gamestartflag=true

    elif data[0][0]==1:
        if data[0][1]==0:#上矢印入力があったなら
            if player[0]==1:
                movethread=threading.Thread(tetrisoneplay.MinoMoveKey(0,0,0,1))
                movethread.start()
        elif data[0][1]==1:#右矢印入力があったなら
            if player[0]==2:
                movethread=threading.Thread(puyopuyooneplay.right_Move())
                movethread.start()
            else:
                movethread=threading.Thread(tetrisoneplay.MinoMoveKey(0,0,1,0))
                movethread.start()
        elif data[0][1]==2:#下矢印入力があったなら
            if player[0]==2:
                movethread=threading.Thread(puyopuyooneplay.down_Move())
                movethread.start()
            else:
                movethread=threading.Thread(tetrisoneplay.MinoMoveKey(0,1,0,0))
                movethread.start()
        elif data[0][1]==3:#左矢印入力があったなら
            if player[0]==2:
                movethread=threading.Thread(puyopuyooneplay.left_Move())
                movethread.start()
            else:
                movethread=threading.Thread(tetrisoneplay.MinoMoveKey(0,0,-1,0))
                movethread.start()
        elif data[0][1]==4:#a矢印入力があったなら
            if player[0]==2:
                movethread=threading.Thread(puyopuyooneplay.left_Rot())
                movethread.start()
            else:
                movethread=threading.Thread(tetrisoneplay.MinoMoveKey(1,0,0,0))
                movethread.start()
                time.sleep(0.1)
        elif data[0][1]==5:#s矢印入力があったなら
            if player[0]==1:
                movethread=threading.Thread(tetrisoneplay.hold())
                movethread.start()
        elif data[0][1]==6:#d矢印入力があったなら
            if player[0]==2:
                movethread=threading.Thread(puyopuyooneplay.right_Rot())
                movethread.start()
            else:
                movethread=threading.Thread(tetrisoneplay.MinoMoveKey(-1,0,0,0))
                movethread.start()
                time.sleep(0.1)
        elif data[0][1]==[3,0]:
            tetrisone()
        elif data[0][1]==[3,1]:
            puyopuyoone()
        elif data[0][1]==[3,2]:
            gamestartbef()
            gamestartflag=true

def tcpsend(sendvalue):
        P1Send=threading.Thread(target=P1SendFunction(sendvalue))
        P2Send=threading.Thread(target=P2SendFunction(sendvalue))
        P1Send.start()
        P2Send.start()


def P1SendFunction(sendvalue):
    global reconnectP1
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s2:
        try:
            if getip[0][0]==0 or getip[0][1]==0:
                return
            s2.connect((getip[0][0],getip[0][1]))
            senddata=pickle.dumps(sendvalue)
            s2.sendto(senddata,(getip[0][0],getip[0][1]))
            s2.close()
        except:
            s2.close()
            reconnectP1+=1
            print(f'accesstry:{reconnectP1}')
            if reconnectP1>10:
                P2SendFunction([-2])
                print('lostconnection')
                return
            cv.after(5,tcpsend(sendvalue))#送れなかったら再帰
            
def P2SendFunction(sendvalue):
    global reconnectP2
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s2:
        try:
            if getip[1][0]==0 or getip[1][1]==0:
                return
            s2.connect((getip[1][0],getip[1][1]))
            senddata=pickle.dumps(sendvalue)
            s2.sendto(senddata,(getip[1][0],getip[1][1]))
            s2.close()
        except:
            s2.close()
            reconnectP2+=1
            print(f'accesstry:{reconnectP2}')
            if reconnectP2>10:
                P1SendFunction([-2])
                print('lostconnection')
                return
            cv.after(5,tcpsend(sendvalue))#送れなかったら再帰


def playernumsend1(sendvalue):
    global reconnectP1
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s2:
            try:
                print(getip)
                s2.connect((getip[0][0],getip[0][1]))
                senddata=pickle.dumps(sendvalue)
                s2.sendto(senddata,(getip[0][0],getip[0][1]))
                s2.close()
                
            except:
                s2.close()
                cv.after(5,tcpsend(sendvalue))#送れなかったら再帰

def playernumsend2(sendvalue):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s2:
            try:
                print(getip)
                s2.connect((getip[1][0],getip[1][1]))
                senddata=pickle.dumps(sendvalue)
                s2.sendto(senddata,(getip[1][0],getip[1][1]))
                s2.close()
                
            except:
                s2.close()
                cv.after(5,tcpsend(sendvalue))#送れなかったら再帰
def main():
    global cv,master,tetrisoneplay,tetristwoplay,puyopuyooneplay,puyopuyotwoplay,btn1,btn2,btn3,btn4,btn5,player
    master=Tk()
    master.title("puyotet_server_v2.x")
    master.resizable(0,0)
    master.attributes("-toolwindow",1)
    cv=Canvas(master, width=120, height=60)
    cv.pack()
    #master.state('zoomed')
    clickimage[0]=PhotoImage(file="./picture/start/tetrisclick.png")
    clickimage[1]=PhotoImage(file="./picture/start/puyopouyoclick.png")
    clickimage[2]=PhotoImage(file="./picture/start/tetselect.png")
    clickimage[3]=PhotoImage(file="./picture/start/puyoselect.png")
    ojyapuyo[0]=PhotoImage(file="./picture/puyopuyo/puyo/atk/smallpuyo.png")
    ojyapuyo[1]=PhotoImage(file="./picture/puyopuyo/puyo/atk/largepuyo.png")
    ojyapuyo[2]=PhotoImage(file="./picture/puyopuyo/puyo/atk/rockpuyo.png")
    ojyapuyo[3]=PhotoImage(file="./picture/puyopuyo/puyo/atk/starpuyo.png")
    ojyapuyo[4]=PhotoImage(file="./picture/puyopuyo/puyo/atk/moonpuyo.png")
    ojyapuyo[5]=PhotoImage(file="./picture/puyopuyo/puyo/atk/crounpuyo.png")
    ojyamino[0]=PhotoImage(file="./picture/tetris/mino/atk/smallmino.png")
    ojyamino[1]=PhotoImage(file="./picture/tetris/mino/atk/largemino.png")
    ojyamino[2]=PhotoImage(file="./picture/tetris/mino/atk/rockmino.png")
    ojyamino[3]=PhotoImage(file="./picture/tetris/mino/atk/starmino.png")
    ojyamino[4]=PhotoImage(file="./picture/tetris/mino/atk/moonmino.png")

    beginimage[0]=PhotoImage(file="./picture/main/leady.png")
    beginimage[1]=PhotoImage(file="./picture/main/go.png")
    beginimage[2]=PhotoImage(file="./picture/main/readytetris.png")
    beginimage[3]=PhotoImage(file="./picture/main/readypuyopuyo.png")

    tetrisoneplay=tetrisplay()
    tetristwoplay=tetrisplay()
    puyopuyooneplay=puyopuyoplay()
    puyopuyotwoplay=puyopuyoplay()
    tetrisoneplay.playernum=0
    tetristwoplay.playernum=1
    puyopuyooneplay.playernum=0
    puyopuyotwoplay.playernum=1
    master.mainloop()


if __name__ == "__main__":                                                                  #main関数が実行されるようにする
    threadmain=threading.Thread(target=main)
    threadclient=threading.Thread(target=tcpreceive)
    threadmain.start()
    threadclient.start()
    
    #相殺
    #tetris<>tetris
    #puyopuyo<>puyopuyo
    #tetris<-puyopuyo

