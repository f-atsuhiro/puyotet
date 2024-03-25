
from tkinter import *
from random import randint as rnd
from tkinter import font as ft
import pygame
import threading
import socket
import pickle
import json
import time

setting=open('./setting.json','r')
settingdata=json.load(setting)
ip_address=settingdata["ip_address"]
port=settingdata["serverport"]
portrec=settingdata["clientport"]
accesstry=settingdata["accesstry"]

print(f"{port},{portrec},{ip_address}")
buffer_size = 4092
mainhaikei=[0,0,0,0,0,0]
ojyapuyo=[0,0,0,0,0,0]
ojyamino=[0,0,0,0,0]
servermsg=[[0],[0,0,0]]#connection,error
connecting,connectingcount=[0,0,0],0
mainback=0
switchback=0
#-----------------gameflag等
GameOverCnt=0
usedata=[-1,-1,-1,-1]
true,false=0,1
drawthreadinit=false
beginimage=[0,0,0,0]
selectgame=false
gameoverimage=[0,0,0]
returnflag=false

pygame.init()



def gamebefore():
    if selectgame==true:
        btn5.place_forget()
        senddata=[playerflag,[3,2]]
        sendthread=threading.Thread(target=tcpsend(senddata))
        sendthread.start()
    else:
        cv.delete("ServerError")
        cv.create_image(900,550,image=servermsg[1][0],tag="ServerError")


def tetrisoneExecute():
    global selectgame
    selectgame=true
    cv.delete("ServerError")
    tetrisone()
    tetrisonepic()

def puyopuyooneExecute():
    global selectgame
    selectgame=true
    cv.delete("ServerError")
    puyopuyoone()
    puyopuyoonepic()

def tetristwoExecute():
    global selectgame
    selectgame=true
    cv.delete("ServerError")
    tetristwo()
    tetristwopic()

def puyopuyotwoExecute():
    global selectgame
    selectgame=true
    cv.delete("ServerError")
    puyopuyotwo()
    puyopuyotwopic()

def tetrisone():
    senddata=[playerflag,[3,0]]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def tetrisonepic():
    cv.delete("player1")
    cv.create_image(250,250,image=clickimage[0],tag='player1')

def puyopuyoone():
    senddata=[playerflag,[3,1]]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def puyopuyoonepic():
    cv.delete("player1")
    cv.create_image(250,250,image=clickimage[1],tag='player1')

def tetristwo():
    senddata=[playerflag,[3,0]]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def tetristwopic():
    cv.delete("player2")
    cv.create_image(900,250,image=clickimage[0],tag='player2')

def puyopuyotwo():
    senddata=[playerflag,[3,1]]
    sendthread=threading.Thread(target=tcpsend(senddata))
    sendthread.start()

def puyopuyotwopic():
    cv.delete("player2")
    cv.create_image(900,250,image=clickimage[1],tag='player2')

def gamestartfunction(usedata):
    btn1.place_forget()
    btn2.place_forget()
    btn3.place_forget()
    btn4.place_forget()
    cv.delete("switchback")
    if usedata[1][0]==1:
        cv.create_image(150,300,image=beginimage[2],tag="setting")
    elif usedata[1][0]==2:
        cv.create_image(150,300,image=beginimage[3],tag="setting")
    if usedata[1][1]==1:
        cv.create_image(1050,300,image=beginimage[2],tag="setting")
    elif usedata[1][1]==2:
        cv.create_image(1050,300,image=beginimage[3],tag="setting")
    #cv.create_image(600,300,tag="setting")
    cv.create_image(600,300,image=beginimage[0],tag="settingbef")
    pygame.mixer.Sound("./assets/sound/main/ready.ogg").play()
    cv.after(1000,gameGo)

def gameGo():
    cv.delete("settingbef")
    cv.create_image(600,300,image=beginimage[1],tag="settinggo")
    pygame.mixer.Sound("./assets/sound/main/go.ogg").play()
    cv.after(1000,deletesetting)

def deletesetting():
    cv.delete("settinggo")

class tetdraw():
    def __init__(self):
        global master,GameOvercnt,sc
        self.senddata=[[-1],[-1],[-1]]
        self.deletemain=0
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
        self.progend=0
        self.x=4
        self.y=-2
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
        self.colors[10]=PhotoImage(file="./assets/picture/tetris/mino/atkpuyo.png")
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
        self.nextimage=PhotoImage(file="./assets/picture/tetris/word/next.png")
        self.colors[0]=PhotoImage(file="./assets/picture/tetris/mino/i_mino.png")
        self.colors[1]=PhotoImage(file="./assets/picture/tetris/mino/j_mino.png")
        self.colors[2]=PhotoImage(file="./assets/picture/tetris/mino/l_mino.png")
        self.colors[3]=PhotoImage(file="./assets/picture/tetris/mino/o_mino.png")
        self.colors[4]=PhotoImage(file="./assets/picture/tetris/mino/s_mino.png")
        self.colors[5]=PhotoImage(file="./assets/picture/tetris/mino/t_mino.png")
        self.colors[6]=PhotoImage(file="./assets/picture/tetris/mino/z_mino.png")
        self.colors[7]=PhotoImage(file="./assets/picture/tetris/mino/no_mino.png")
        self.colors[9]=PhotoImage(file="./assets/picture/tetris/mino/ojya_mino.png")
        self.string[0]=PhotoImage(file="./assets/picture/tetris/word/0.png")
        self.string[1]=PhotoImage(file="./assets/picture/tetris/word/1.png")
        self.string[2]=PhotoImage(file="./assets/picture/tetris/word/2.png")
        self.string[3]=PhotoImage(file="./assets/picture/tetris/word/3.png")
        self.string[4]=PhotoImage(file="./assets/picture/tetris/word/4.png")
        self.string[5]=PhotoImage(file="./assets/picture/tetris/word/5.png")
        self.string[6]=PhotoImage(file="./assets/picture/tetris/word/6.png")
        self.string[7]=PhotoImage(file="./assets/picture/tetris/word/7.png")
        self.string[8]=PhotoImage(file="./assets/picture/tetris/word/8.png")
        self.string[9]=PhotoImage(file="./assets/picture/tetris/word/9.png")
        self.string[10]=PhotoImage(file="./assets/picture/tetris/word/renstring.png")
        self.string[11]=PhotoImage(file="./assets/picture/tetris/word/score.png")
        self.string[12]=PhotoImage(file="./assets/picture/tetris/word/tetris.png")
        self.tec[0][1]=PhotoImage(file="./assets/picture/tetris/technique/TSS.png")    #T spin single
        self.tec[0][0]=PhotoImage(file="./assets/picture/tetris/technique/TSSM.png")   #T spin single mini
        self.tec[0][3]=PhotoImage(file="./assets/picture/tetris/technique/TSD.png")    #T spin double
        self.tec[0][2]=PhotoImage(file="./assets/picture/tetris/technique/TSDM.png")   #T spin double mini
        self.tec[0][5]=PhotoImage(file="./assets/picture/tetris/technique/TST.png")    #T spin triple
        self.tec[0][4]=PhotoImage(file="./assets/picture/tetris/technique/TST.png")    #T spin triple (mini)
        self.tec[3][0]=PhotoImage(file="./assets/picture/tetris/technique/BTB.png")    #Back To Back
        self.sound[0]=pygame.mixer.Sound("./assets/sound/tetris/minodelete.ogg")  #ren sound
    def NextMinoDraw(self,usedata):
        for nextblock in range(4):
            for xdraw in range(self.minosize):                                                           #変数vをminosize(ミノの領域)回続ける
                xdraw1 = (xdraw - 1) * 20+(120+20*nextblock*5-50)                                            #上2行でミノ１ブロックの始まり座標と終わり座標を算出(そのためミノの数(v)回同じ処理をして4つミノを成立させる
                for ydraw in range(self.minosize):                                                       #変数sを用意してもう一度minosize回のループを生成する
                    ydraw1 = (ydraw - 1) * 20+(12*20+250)                                                         #s2にs1+size☆\\前行+一マス当たりのサイズ
                    cv.create_image(ydraw1+usedata[1]*300+15, xdraw1+15,  image = self.colors[7],tag=f"tetone{usedata[1]}{self.deletemain}")
                    if usedata[3][2][nextblock][xdraw][ydraw] == usedata[3][1][nextblock]:
                        cv.create_image(ydraw1+usedata[1]*300+15, xdraw1+15,image = self.colors[usedata[3][1][nextblock]],tag=f"tetone{usedata[1]}{self.deletemain}")
                        
    def MoveDraw(self,usedata):
        for i in range(3):
            cv.delete(f"tetone{usedata[1]}{self.deletemain-i}NaDrop")
        cv.delete(f"tetone{usedata[1]}tec")
        if self.haikei[1][5]==7 or self.haikei[1][6]==7 or self.haikei[1][7]==7 or self.haikei[1][8]==7:
            usedata[3][0]+=1
            for ydraw in range(self.minosize):
                ydraw1=(ydraw+usedata[3][0]-1)*self.size
                for xdraw in range(self.minosize):
                    xdraw1=(xdraw+usedata[3][1]-1)*self.size
                    if usedata[3][3][ydraw][xdraw]==usedata[3][2]:
                        cv.create_image(xdraw1+usedata[1]*900+15,ydraw1+15,image = self.colors[usedata[3][2]],tag=f"tetone{usedata[1]}{self.deletemain}NaDrop")

    def KeyMove(self,usedata):
        cv.delete(f"tetone{usedata[1]}{self.deletemain}NaDrop")
        if usedata[3][5]!=0 or usedata[3][4]!=0:#addy!=0 or addx!=0
            for ydraw in range(self.minosize):
                ydraw1=(ydraw+usedata[3][0]+usedata[3][4]-1)*self.size
                for xdraw in range(self.minosize):
                    xdraw1=(xdraw+usedata[3][1]+usedata[3][5]-1)*self.size
                    if usedata[3][3][ydraw][xdraw]==usedata[3][2]:
                        cv.create_image(xdraw1+usedata[1]*900+15,ydraw1+15,image=self.colors[usedata[3][2]],tag=f"tetone{usedata[1]}{self.deletemain}NaDrop")
            if usedata[3][5]!=0:
                pygame.mixer.Sound("./assets/sound/tetris/move.ogg").play()
        if usedata[3][6]==1:#drop==true
            pygame.mixer.Sound("./assets/sound/tetris/drop.ogg").play()
            for ydraw in range(self.minosize):
                ydraw1 = (ydraw + usedata[3][0] - 1) * self.size
                for xdraw in range(self.minosize):
                    xdraw1 = (xdraw + usedata[3][1] - 1) * self.size
                    if usedata[3][3][ydraw][xdraw]==usedata[3][2]:
                        cv.create_image(xdraw1+usedata[1]*900+15, ydraw1+15, image = self.colors[usedata[3][2]],tag=f"tetone{usedata[1]}{self.deletemain}NaDrop")
        if usedata[3][7]!=0:#adddire!=0
            for ydraw in range(self.minosize):
                ydraw1 = (ydraw + usedata[3][0] - 1) * self.size
                for xdraw in range(self.minosize):
                    xdraw1 = (xdraw + usedata[3][1] - 1) * self.size
                    if usedata[3][3][ydraw][xdraw] == usedata[3][2]:
                        cv.create_image(xdraw1 + usedata[1] * 900 + 15, ydraw1 + 15, image = self.colors[usedata[3][2]],tag=f"tetone{usedata[1]}{self.deletemain}NaDrop")

    def SuperRotation(self,usedata):
        cv.delete(f"tetone{usedata[1]}{self.deletemain}NaDrop")
        if usedata[3][4]!=0:
            for ydraw in range(self.minosize):
                ydraw1 = (ydraw + usedata[3][0] - 1) * self.size
                for xdraw in range(self.minosize):
                    xdraw1 = (xdraw + usedata[3][1] - 1) * self.size
                    if usedata[3][3][ydraw][xdraw] == usedata[3][2]:
                        cv.create_image(xdraw1 + usedata[1] * 900 + 15, ydraw1 + 15, image = self.colors[usedata[3][2]], tag=f"tetone{usedata[1]}{self.deletemain}NaDrop")

    def TecAndRenDraw(self,usedata):
        #print(f'tecdata={usedata}')
        #print(f"tspintrue={usedata[4][3]}")
        #print(f"tspinminitrue={usedata[4][2]}")
        if usedata[4][1]==true:
            cv.create_image(395 + usedata[1] * 300, 450, image=self.tec[3][0],tag=f"tetone{usedata[1]}tec")
        if usedata[4][3]==true:
            if usedata[4][2]==false:
                #print('runfalse')
                cv.create_image(400 + usedata[1] * 300, 400, image=self.tec[0][usedata[4][4]*2-2],tag=f"tetone{usedata[1]}tec")
            if usedata[4][2]==true:
                #print('runtrue')
                cv.create_image(400 + usedata[1] * 300, 400, image=self.tec[0][usedata[4][4]*2-1],tag=f"tetone{usedata[1]}tec")
        if usedata[4][4]==7:
            cv.create_image(150+usedata[1]*900,500,image=self.string[12],tag="tetrisG")
        deletethread=threading.Thread(target=self.AfterDeleteTec(usedata))
        deletethread.start()
        
    def AfterDeleteTec(self,usedata):
        #print('deletebef')
        time.sleep(2)
        #print('deletetec')
        cv.delete(f"tetone{usedata[1]}tec")



    def HaikeiDraw(self,usedata):
        self.haikei=usedata[3]
        if GameOverCnt==0:
            self.deletemain+=1
            for xdraw in range(self.height):
                xdraw1=xdraw*self.size
                for ydraw in range(self.lenght):
                    ydraw1=ydraw*self.size
                    for c in range(len(self.colors)):
                        if self.haikei[xdraw+1][ydraw+1]==c:
                            if c==10:
                                cv.create_image(ydraw1+15+usedata[1]*900,xdraw1+15,image=self.colors[c],tag=f"tetone{usedata[1]}{self.deletemain}")
                            else:
                                cv.create_image(ydraw1+usedata[1]*900+15,xdraw1+15,image=self.colors[c],tag=f"tetone{usedata[1]}{self.deletemain}")
            cv.create_image(510+usedata[1]*300,25,image=self.nextimage)
            self.HoldDraw([usedata[0],usedata[1],usedata[2],[0,0,2,0,usedata[4][5],usedata[4][6]]])
            #self.NextMinoDraw([usedata[0],usedata[1],usedata[2],[usedata[3][1],usedata[3][2],usedata[3][3]]])
            for i in range(1,25):
                cv.delete(f"tetone{usedata[1]}{self.deletemain-i}")

    def HoldDraw(self,usedata):
        if usedata[3][2]==0:
            cv.delete(f"tetone{usedata[1]}{self.deletemain}NaDrop")
        elif usedata[3][2]==1:
            for xdraw in range(self.minosize):                                                           #変数vをminosize(ミノの領域)回続ける
                xdraw1 = (xdraw - 1) * self.size+120                                           #上2行でミノ１ブロックの始まり座標と終わり座標を算出(そのためミノの数(v)回同じ処理をして4つミノを成立させる
                for ydraw in range(self.minosize):                                                       #変数sを用意してもう一度minosize回のループを生成する
                    ydraw1 = (ydraw - 1) * self.size+(12*self.size)                                                     #s2にs1+size☆\\前行+一マス当たりのサイズ
                    cv.create_image(ydraw1+usedata[1]*300+15, xdraw1+15, image = self.colors[7],tag=f"tetone{usedata[1]}{self.deletemain}")
                    if usedata[3][1][xdraw][ydraw] == usedata[3][0]:
                        cv.create_image(ydraw1+usedata[1]*300+15, xdraw1+15,image = self.colors[usedata[3][0]],tag=f"tetone{usedata[1]}{self.deletemain}")
        elif usedata[3][2]==2:
            for xdraw in range(self.minosize):                                                           #変数vをminosize(ミノの領域)回続ける
                xdraw1 = (xdraw - 1) * self.size+120                                           #上2行でミノ１ブロックの始まり座標と終わり座標を算出(そのためミノの数(v)回同じ処理をして4つミノを成立させる
                for ydraw in range(self.minosize):                                                       #変数sを用意してもう一度minosize回のループを生成する
                    ydraw1 = (ydraw - 1) * self.size+(12*self.size)                                                     #s2にs1+size☆\\前行+一マス当たりのサイズ
                    cv.create_image(ydraw1+usedata[1]*300+15, xdraw1+15, image = self.colors[7],tag=f"tetone{usedata[1]}{self.deletemain}")
                    if usedata[3][5][xdraw][ydraw] == usedata[3][4]:
                        cv.create_image(ydraw1+usedata[1]*300+15, xdraw1+15,image = self.colors[usedata[3][4]],tag=f"tetone{usedata[1]}{self.deletemain}")

    def Minodraw(self,usedata):
        for xdraw in range(self.minosize):
            xdraw1=(xdraw+usedata[3][0]-1)*self.size
            for ydraw in range(self.minosize):
                ydraw1=(ydraw+usedata[3][0]-1)*self.size
                if self.mino[xdraw][ydraw]==self.form:
                    cv.create_image(ydraw1+usedata[1]*900+15,xdraw1+15,image=self.colors[self.form],tag=f"tetone{usedata[1]}{self.deletemain}NaDrop")

    def ScoreDraw(self,usedata):
        cv.delete(f'score{usedata[1]}')
        cv.create_image(77+300+usedata[1]*300,500,image=self.string[11],tag=f'score{usedata[1]}')
        handMscore=int((usedata[3][0]%1000000000)/100000000)
        tenMscore=int((usedata[3][0]%100000000)/10000000)
        oneMscore=int((usedata[3][0]%10000000)/1000000)
        handKscore=int((usedata[3][0]%1000000)/100000)
        tenKscore=int((usedata[3][0]%100000)/10000)
        oneKscore=int((usedata[3][0]%10000)/1000)
        handscore=int((usedata[3][0]%1000)/100)
        tenscore=int((usedata[3][0]%100)/10)
        onescore=int(usedata[3][0]%10)
        cv.create_image(40+300+usedata[1]*300,550,image=self.string[handMscore],tag=f'score{usedata[1]}')
        cv.create_image(70+300+usedata[1]*300,550,image=self.string[tenMscore],tag=f'score{usedata[1]}')
        cv.create_image(100+300+usedata[1]*300,550,image=self.string[oneMscore],tag=f'score{usedata[1]}')
        cv.create_image(130+300+usedata[1]*300,550,image=self.string[handKscore],tag=f'score{usedata[1]}')
        cv.create_image(160+300+usedata[1]*300,550,image=self.string[tenKscore],tag=f'score{usedata[1]}')
        cv.create_image(190+300+usedata[1]*300,550,image=self.string[oneKscore],tag=f'score{usedata[1]}')
        cv.create_image(220+300+usedata[1]*300,550,image=self.string[handscore],tag=f'score{usedata[1]}')
        cv.create_image(250+300+usedata[1]*300,550,image=self.string[tenscore],tag=f'score{usedata[1]}')
        cv.create_image(280+300+usedata[1]*300,550,image=self.string[onescore],tag=f'score{usedata[1]}')






class puyodraw():
    def __init__(self):
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
        self.form,self.direction,self.lencnt,self.candrop,self.holdsave,self.holdmax=0,0,0,0,0,0            #ミノの種類,ミノの向き,現在のlenカウント       
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
        self.puyo_color[7]=PhotoImage(file="./assets/picture/puyopuyo/puyo/ojya_mino_mino.png")
        self.puyo_color[8]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atkpuyo_puyo.png")
        self.deletemain=0
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
        self.puyo_color[0]=PhotoImage(file="./assets/picture/puyopuyo/puyo/red_puyo.png")
        self.puyo_color[1]=PhotoImage(file="./assets/picture/puyopuyo/puyo/blue_puyo.png")
        self.puyo_color[2]=PhotoImage(file="./assets/picture/puyopuyo/puyo/yellow_puyo.png")
        self.puyo_color[3]=PhotoImage(file="./assets/picture/puyopuyo/puyo/green_puyo.png")
        self.puyo_color[4]=PhotoImage(file="./assets/picture/puyopuyo/puyo/purple_puyo.png")
        self.puyo_color[5]=PhotoImage(file="./assets/picture/puyopuyo/puyo/none.png")
        self.puyo_color[6]=PhotoImage(file="./assets/picture/puyopuyo/puyo/wall.png")
        self.ren[0]=PhotoImage(file="./assets/picture/puyopuyo/word/0.png")
        self.ren[1]=PhotoImage(file="./assets/picture/puyopuyo/word/1.png")
        self.ren[2]=PhotoImage(file="./assets/picture/puyopuyo/word/2.png")
        self.ren[3]=PhotoImage(file="./assets/picture/puyopuyo/word/3.png")
        self.ren[4]=PhotoImage(file="./assets/picture/puyopuyo/word/4.png")
        self.ren[5]=PhotoImage(file="./assets/picture/puyopuyo/word/5.png")
        self.ren[6]=PhotoImage(file="./assets/picture/puyopuyo/word/6.png")
        self.ren[7]=PhotoImage(file="./assets/picture/puyopuyo/word/7.png")
        self.ren[8]=PhotoImage(file="./assets/picture/puyopuyo/word/8.png")
        self.ren[9]=PhotoImage(file="./assets/picture/puyopuyo/word/9.png")
        self.ren[10]=PhotoImage(file="./assets/picture/puyopuyo/word/renstring.png")
        self.ren[11]=PhotoImage(file="./assets/picture/puyopuyo/word/score.png")
        self.sound[0][1]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing01_ren01.ogg")
        self.sound[0][2]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing02_ren02.ogg")
        self.sound[0][3]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing03_ren03.ogg")
        self.sound[0][4]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing04_ren04.ogg")
        self.sound[0][5]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing05_ren05.ogg")
        self.sound[0][6]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing06_ren06.ogg")
        self.sound[0][7]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][8]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][9]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][10]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][11]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][12]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][13]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[0][14]=pygame.mixer.Sound("./assets/sound/puyopuyo/se_ing07_ren07.ogg")
        self.sound[1][0]=pygame.mixer.Sound("./assets/sound/puyopuyo/ojyamamin.ogg")
        self.sound[1][1]=pygame.mixer.Sound("./assets/sound/puyopuyo/ojyamamax.ogg")

    def HaikeiDraw(self,usedata):
        
        self.deletemain+=1
        for ydraw in range(self.height):
            ydraw1 = ydraw * self.size + 27
            for xdraw in range(self.length):
                xdraw1 = xdraw * self.size + 27
                for c in range(len(self.puyo_color)):
                    if usedata[3][ydraw+1][xdraw+1] == c:
                        cv.create_image(xdraw1 + usedata[1] * 900, ydraw1, image=self.puyo_color[c],tag=f"puyo{usedata[1]}{self.deletemain}")
        for next in range(2):
            cv.create_image(250 + 300 + usedata[1] * 300,100 - (next*self.size),image=self.puyo_color[usedata[4][0][next]],tag=f"puyo{usedata[1]}{self.deletemain}")
            cv.create_image(190 + 300 + usedata[1] * 300,170 - (next*self.size),image=self.puyo_color[usedata[4][1][next]],tag=f"puyo{usedata[1]}{self.deletemain}")
        for i in range(1,25):
            cv.delete(f"puyo{usedata[1]}{self.deletemain-i}")
            cv.delete(f"renpuyo{usedata[1]}{self.deletemain-i}")

    #def PuyoDrop(self):
        

    def PuyoDraw(self,usedata):
        cv.delete(f"droppuyo{usedata[1]}")
        for ydraw in range(len(self.puyo)):          #27は位置調整
            ydrawpoint=(ydraw+usedata[3][0])*self.size+27-self.size     #※debug実行時に判明:単純に27をずらしただけだとx+xdraw=0の時に1の場所に表示されるため一マス分ずらしておく(そのための-size)
            for xdraw in range(len(self.puyo)):
                xdrawpoint=(xdraw+usedata[3][1])*self.size+27-self.size
                for i in range(self.puyosize):
                    if usedata[3][3][ydraw][xdraw] == usedata[3][2][i]:
                        cv.create_image(xdrawpoint+usedata[1]*900, ydrawpoint ,image=self.puyo_color[usedata[3][2][i]],tag=f"droppuyo{usedata[1]}")
    
    
    def RenAndBlinkingFirst(self,usedata):
        for tchecky in range(12):                                                                                #点滅用
            for tcheckx in range(6):
                if usedata[3][0][tchecky+1][tcheckx+1]==3:
                    cv.create_image((tcheckx)*self.size+27+usedata[1]*900,(tchecky)*self.size+27 ,image=self.puyo_color[5],tag=f"puyo{usedata[1]}")
                    if usedata[3][1]>=1:
                        cv.delete(f"renpuyo{usedata[1]}")
                        cv.create_image(250+300+usedata[1]*300, 470 ,image=self.ren[10],tag=f"renpuyo{usedata[1]}")
                        secren=int(usedata[3][1]/10)#ren(2桁
                        firren=int(usedata[3][1]%10)#ren(1桁
                        cv.create_image(200+300+usedata[1]*300, 470 ,image=self.ren[firren],tag=f"renpuyo{usedata[1]}")
                        if secren!=0:
                            cv.create_image(170+300+usedata[1]*300,470,image=self.ren[secren],tag=f"renpuyo{usedata[1]}")
                        pygame.mixer.Sound(self.sound[0][usedata[3][1]]).play()#ren音再生
        threading.Thread(target=self.PuyoBlinkingSecond(usedata)).start()
    
    def PuyoBlinkingSecond(self,usedata):
        cv.after(200,self.ExecuteBlinkingSecond(usedata))

    def ExecuteBlinkingSecond(self,usedata):
        for tchecky in range(12):                                                                                #点滅用
            for tcheckx in range(6):
                if usedata[3][0][tchecky+1][tcheckx+1]==3:
                    cv.create_image(tcheckx*self.size+327-300+usedata[1]*900,tchecky*self.size+27 ,image=self.puyo_color[usedata[3][2][tchecky+1][tcheckx+1]],tag=f"puyo{usedata[1]}")
                    
    def PuyoScore(self,usedata):
        cv.delete(f"score{usedata[1]}")
        cv.create_image(77+300+usedata[1]*300,500,image=self.ren[11],tag=f'score{usedata[1]}')#score.pngにscoreの文字画像
        handMscore=int((usedata[3][0]%1000000000)/100000000)
        tenMscore=int((usedata[3][0]%100000000)/10000000)
        oneMscore=int((usedata[3][0]%10000000)/1000000)
        handKscore=int((usedata[3][0]%1000000)/100000)
        tenKscore=int((usedata[3][0]%100000)/10000)
        oneKscore=int((usedata[3][0]%10000)/1000)
        handscore=int((usedata[3][0]%1000)/100)
        tenscore=int((usedata[3][0]%100)/10)
        onescore=int(usedata[3][0]%10)
        cv.create_image(40+300+usedata[1]*300,550,image=self.ren[handMscore],tag=f'score{usedata[1]}')
        cv.create_image(70+300+usedata[1]*300,550,image=self.ren[tenMscore],tag=f'score{usedata[1]}')
        cv.create_image(100+300+usedata[1]*300,550,image=self.ren[oneMscore],tag=f'score{usedata[1]}')
        cv.create_image(130+300+usedata[1]*300,550,image=self.ren[handKscore],tag=f'score{usedata[1]}')
        cv.create_image(160+300+usedata[1]*300,550,image=self.ren[tenKscore],tag=f'score{usedata[1]}')
        cv.create_image(190+300+usedata[1]*300,550,image=self.ren[oneKscore],tag=f'score{usedata[1]}')
        cv.create_image(220+300+usedata[1]*300,550,image=self.ren[handscore],tag=f'score{usedata[1]}')
        cv.create_image(250+300+usedata[1]*300,550,image=self.ren[tenscore],tag=f'score{usedata[1]}')
        cv.create_image(280+300+usedata[1]*300,550,image=self.ren[onescore],tag=f'score{usedata[1]}')
        





def GameOver(usedata):
    cv.create_image(600,300,image=gameoverimage[2])
    cv.create_image(150+(usedata[1]-1)*900,300,image=gameoverimage[1])
    if usedata[1]==1:
        cv.create_image(1050,300,image=gameoverimage[0])
    else:
        cv.create_image(150,300,image=gameoverimage[0])


def OnePlayerRecevedamageG(usedata):
    if usedata[2][0]!=0:
        print('damage1')
    cv.delete("damage1")
    GraMax=0
    oukan=int(usedata[2][0]/720)
    usedata[2][0]=usedata[2][0]%720
    moon=int(usedata[2][0]/360)
    usedata[2][0]=usedata[2][0]%320
    star=int(usedata[2][0]/180)
    usedata[2][0]=usedata[2][0]%180
    rock=int(usedata[2][0]/30)
    usedata[2][0]=usedata[2][0]%30
    large=int(usedata[2][0]/6)
    small=usedata[2][0]%6
    if usedata[2][1]==1:
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
    elif usedata[2][1]==2:
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

def TwoPlayerReceveDamageG(usedata):
    if usedata[2][0]!=0:
        print('damage2')
    cv.delete("damage2")
    GraMax=0
    oukan=int(usedata[2][0]/720)
    usedata[2][0]=usedata[2][0]%720
    moon=int(usedata[2][0]/360)
    usedata[2][0]=usedata[2][0]%320
    star=int(usedata[2][0]/180)
    usedata[2][0]=usedata[2][0]%180
    rock=int(usedata[2][0]/30)
    usedata[2][0]=usedata[2][0]%30
    large=int(usedata[2][0]/6)
    small=usedata[2][0]%6
    if usedata[2][1]==1:
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
    elif usedata[2][1]==2:
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


def lostconnection():
    cv.delete("all")
    cv.create_image(900,550,image=servermsg[1][2],tag="ServerError")
    #cv.create_image(900,550,image=servermsg[1][2],tag="ServerError")
    #cv.after(3000,lambda :cv.delete("all"))



def tcpsend(value):
    global connectingcount
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # サーバーに接続を要求する
            try:
                s.connect((ip_address, port))
                # データを送信する
                value=[value,socket.gethostbyname(socket.gethostname()),portrec]
                senddata=pickle.dumps(value)
                s.send(senddata)
                s.close()
            except:
                cv.delete("connecting")
                connectingcount+=1
                cv.create_image(600,300,image=mainback,tag="connecting")
                cv.create_image(300,300,image=connecting[connectingcount%3],tag="connecting")
                s.close()
                if connectingcount>accesstry:
                    cv.create_image(900,550,image=servermsg[1][1],tag="ServerError")
                    return
                tcpsend(value)#もし運べなかったら再帰

def recevedata():
    global returnflag
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s2:#sとしてsocket
        s2.bind((socket.gethostbyname(socket.gethostname()),portrec))#port ip を紐付け
        s2.listen()#接続最大数
        while True:#受け取り続ける(マルチスレッドなので回し続けてもほかに影響はない)
            
            connect,address=s2.accept()#connectに接続されたipを記録
            data=connect.recv(1024)#運ばれたデータをデコードする
            sendvalue=pickle.loads(data)#pickleで受け取ったデータの復元dataは二次元配列で一つ目の要素にゲーム番号二つ目の要素に何の描写か、3つめの要素にデータの本体を格納
            
            if sendvalue[0]==5 or sendvalue[0]==-2:
                try:
                    if sendvalue[0]==5:
                        GameOver(sendvalue)
                finally:
                    s2.close()
                    returnflag=true
            drawthread=threading.Thread(target=drawfunction(sendvalue))
            drawthread.start()
            if returnflag==true:
                return

def drawfunction(usedata):
    global playerflag
    if usedata[0]==99:
        if usedata[1]==1:
            playerflag=1
            try:
                cv.delete("connecting")
                cv.create_image(900,500,image=servermsg[0][0],tag="接続確立")
            finally:
                connect()
        elif usedata[1]==2:
            playerflag=2
            try:
                cv.delete("connecting")
                cv.create_image(900,500,image=servermsg[0][0],tag="接続確立")
            finally:
                connect()
    if usedata[0]==0:
        if usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==0:
            tetris.HaikeiDraw(usedata)
            if usedata[4][0] != 0:
                threading.Thread(target = tetris.TecAndRenDraw,args = ([usedata])).start()
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==1:
            tetris.Minodraw(usedata)
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==4:
            threading.Thread(target = tetris.NextMinoDraw,args = ([usedata])).start()
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==5:
            tetris.MoveDraw(usedata)
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==6:
            tetris.KeyMove(usedata)
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==7:
            tetris.SuperRotation(usedata)
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==8:
            tetris.TecDraw(usedata)
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==9:
            tetris.HoldDraw(usedata)
        elif usedata[0]==0 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==10:
            tetris.ScoreDraw(usedata)
    if usedata[0]==1:
        if usedata[0]==1 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==0:
            puyopuyo.HaikeiDraw(usedata)
        if usedata[0]==1 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==1:
            puyopuyo.PuyoDraw(usedata)
        if usedata[0]==1 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==2:
            puyopuyo.RenAndBlinkingFirst(usedata)
        if usedata[0]==1 and (usedata[1]==0 or usedata[1]==1) and usedata[2]==3:
            puyopuyo.PuyoScore(usedata)
    if usedata[0]==2:
        gamestartimage=usedata[1]
        mainhaikei[0]=PhotoImage(file=f"./assets/main/main{usedata[1]}.png")
        cv.create_image(600,300,image=mainhaikei[0],tag="main")
    if usedata[0]==3:#startflag
        gamestartfunction(usedata)
    if usedata[0]==4:
        if usedata[2]==1:
            if usedata[1]==0:
                tetrisonepic()
            if usedata[1]==1:
                puyopuyoonepic()
        elif usedata[2]==2:
            if usedata[1]==0:
                tetristwopic()
            if usedata[1]==1:
                puyopuyotwopic()
    if usedata[0]==50:
        if usedata[1]==14:
            TwoPlayerReceveDamageG(usedata)
        elif usedata[1]==15:
            OnePlayerRecevedamageG(usedata)
    if usedata[0]==-2:
        lostconnection()

def connect():
    global btn1,btn2,btn3,btn4,btn5,switchback
    cv.create_image(600,300,image=switchback,tag="switchback")
    if playerflag==1:
        btn1=Button(image=clickimage[2],text="tetris",command=tetrisoneExecute)
        btn1.place(x=350,y=175)
        btn2=Button(image=clickimage[3],text="puyopuyo",command=puyopuyooneExecute)
        btn2.place(x=350,y=275)
        btn3=Button(image=clickimage[2],text="tetris",state=DISABLED)
        btn3.place(x=650,y=175)
        btn4=Button(image=clickimage[3],text="puyopuyo",state=DISABLED)
        btn4.place(x=650,y=275)
    elif playerflag==2:
        btn1=Button(image=clickimage[2],text="tetris",state=DISABLED)
        btn1.place(x=350,y=175)
        btn2=Button(image=clickimage[3],text="puyopuyo",state=DISABLED)
        btn2.place(x=350,y=275)
        btn3=Button(image=clickimage[2],text="tetris",command=tetristwoExecute)
        btn3.place(x=650,y=175)
        btn4=Button(image=clickimage[3],text="puyopuyo",command=puyopuyotwoExecute)
        btn4.place(x=650,y=275)
    btn5=Button(text="決定",command=gamebefore)
    btn5.place(x=560,y=400)

def main():
    global clickimage,cv,threadclient,tetris,puyopuyo,servermsg,switchback,mainback
    master=Tk()
    master.title("puyotet_client_v3.x")
    master.resizable(0,0)
    #master.attributes("-toolwindow",1)
    master.iconbitmap('./assets/icon/puyotet.ico')
    
    cv=Canvas(master, width=1200, height=600)
    cv.pack()
    
    
    
    
    tetris=tetdraw()
    puyopuyo=puyodraw()

    for i in range(3):
        connecting[i]=PhotoImage(file=f"./assets/picture/main/connecting/connecting{i}.png")
    mainback=PhotoImage(file="./assets/picture/main/mainback.png")

    switchback=PhotoImage(file="./assets/picture/main/switchback.png")


    #player number flag 要求
    cv.create_image(600,300,image=mainback,tag="connecting")
    cv.create_image(300,300,image=connecting[0],tag="connecting")
    
    
    
    
    clickimage=[0,0,0,0,0]


    
    servermsg[0][0]=PhotoImage(file="./assets/picture/main/Connection with server established/Connection with server established main.png")
    servermsg[1][0]=PhotoImage(file="./assets/picture/main/error/no game selected error.png")
    servermsg[1][1]=PhotoImage(file="./assets/picture/main/error/failed to connect to the server error.png")
    servermsg[1][2]=PhotoImage(file="./assets/picture/main/error/opponent player disconnected error.png")
    beginimage[0]=PhotoImage(file="./assets/picture/main/leady.png")
    beginimage[1]=PhotoImage(file="./assets/picture/main/go.png")
    beginimage[2]=PhotoImage(file="./assets/picture/main/readytetris.png")
    beginimage[3]=PhotoImage(file="./assets/picture/main/readypuyopuyo.png")
    clickimage[0]=PhotoImage(file="./assets/picture/start/tetrisclick.png")
    clickimage[1]=PhotoImage(file="./assets/picture/start/puyopouyoclick.png")
    clickimage[2]=PhotoImage(file="./assets/picture/start/tetselect.png")
    clickimage[3]=PhotoImage(file="./assets/picture/start/puyoselect.png")
    ojyapuyo[0]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atk/smallpuyo.png")
    ojyapuyo[1]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atk/largepuyo.png")
    ojyapuyo[2]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atk/rockpuyo.png")
    ojyapuyo[3]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atk/starpuyo.png")
    ojyapuyo[4]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atk/moonpuyo.png")
    ojyapuyo[5]=PhotoImage(file="./assets/picture/puyopuyo/puyo/atk/crounpuyo.png")
    ojyamino[0]=PhotoImage(file="./assets/picture/tetris/mino/atk/smallmino.png")
    ojyamino[1]=PhotoImage(file="./assets/picture/tetris/mino/atk/largemino.png")
    ojyamino[2]=PhotoImage(file="./assets/picture/tetris/mino/atk/rockmino.png")
    ojyamino[3]=PhotoImage(file="./assets/picture/tetris/mino/atk/starmino.png")
    ojyamino[4]=PhotoImage(file="./assets/picture/tetris/mino/atk/moonmino.png")
    gameoverimage[0]=PhotoImage(file="./assets/picture/main/win.png")
    gameoverimage[1]=PhotoImage(file="./assets/picture/main/lose.png")
    gameoverimage[2]=PhotoImage(file="./assets/picture/main/grayback.png")
    

    master.bind('<Key-Right>',threadsright)
    master.bind('<Key-Left>',threadsleft)
    master.bind('<Key-Down>',threadsdown)
    master.bind('<Key-a>',threadsa)
    master.bind('<Key-d>',threadsd)
    master.bind('<Key-Up>',threadsup)
    master.bind('<Key-s>',threadss)
    master.mainloop()
def threadsleft(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,3]))
    threadclient.start()
def threadsdown(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,2]))
    threadclient.start()
def threadsup(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,0]))
    threadclient.start()
def threadsright(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,1]))
    threadclient.start()
def threadsa(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,4]))
    threadclient.start()
def threadss(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,5]))
    threadclient.start()
def threadsd(event):
    threadclient=threading.Thread(target=tcpsend([playerflag,6]))
    threadclient.start()


if __name__ == "__main__":
    
    mainthread=threading.Thread(target=main)
    mainthread.start()
    recevethread=threading.Thread(target=recevedata)
    recevethread.start()
    time.sleep(1)
    threadclient=threading.Thread(target=tcpsend(99))
    threadclient.start()
    