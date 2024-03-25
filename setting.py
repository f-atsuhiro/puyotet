from tkinter import *
import json

true,false=0,1

def fileopen():
    settingfile=Tk()
    settingfile.title("現在の設定")
    settingwindow=Canvas(settingfile,width=600,height=200)
    settingwindow.pack()

    ipadlabel=Label(settingfile,text='server ip address')
    ipadlabel.place(x=30,y=30)
    iplabeltxt=Label(settingfile,text='：接続先ip(ipv4)')
    iplabeltxt.place(x=150,y=30)

    ipportlabel=Label(settingfile,text='server port address')
    ipportlabel.place(x=30,y=60)
    ipportlabeltxt=Label(settingfile,text='：接続先port　　　 (既定：25567)')
    ipportlabeltxt.place(x=150,y=60)

    Cportlabel=Label(settingfile,text='client port address')
    Cportlabel.place(x=30,y=90)
    Cportlabeltext=Label(settingfile,text='：接続に使用するport(既定：25568)')
    Cportlabeltext.place(x=150,y=90)

    accesstrylabel=Label(settingfile,text='number of access')
    accesstrylabel.place(x=30,y=120)
    accesstrylabeltext=Label(settingfile,text='：接続待ち許容回数  (既定：10)')
    accesstrylabeltext.place(x=150,y=120)

    nowsetting= open('./setting.json','r')
    nowsettingwin=json.load(nowsetting)
    Label(settingfile,text=f'{nowsettingwin["ip_address"]}').place(x=400,y=30)
    Label(settingfile,text=f'{nowsettingwin["serverport"]}').place(x=400,y=60)
    Label(settingfile,text=f'{nowsettingwin["clientport"]}').place(x=400,y=90)
    Label(settingfile,text=f'{nowsettingwin["accesstry"]}').place(x=400,y=120)


    settingfile.mainloop()

def changefile():
    global errorlabel
    try:
        errorlabel=Label(text="                                                                                          ").place(x=10,y=160)
    finally:
        if str(iptextbox.get())=="" and str(Sporttextbox.get())=="" and str(Cporttextbox.get())=="" and str(accesstextbox.get())=="":
            errorlabel=Label(text="入力されている要素がありません                                   ",fg='red')
            errorlabel.place(x=10,y=160)


        if str(accesstextbox.get())!="":
            changeaccesstry()

        if str(iptextbox.get())!="":
            changeip()

        if str(Sporttextbox.get())!="":
            changeSport()

        if str(Cporttextbox.get())!="":
            changeCport()
        

def changeaccesstry():
    global errorlabel
    try:
        newaccess=int(accesstextbox.get())
        if newaccess>10 or newaccess<=0:
            errorlabel=Label(text="number of accessに指定できる値は0~10です                      ",fg='red')
            errorlabel.place(x=10,y=160)
        else:
            with open('./setting.json','r') as changeaccess:
                changeaccessdic=json.load(changeaccess)
                changeaccessdic["accesstry"]=newaccess
            with open('./setting.json','w') as changeaccess:
                json.dump(changeaccessdic,changeaccess,indent=4)
    except:
        errorlabel=Label(text="number of accessに文字は指定できません                          ",fg='red')
        errorlabel.place(x=10,y=160)

def changeCport():
    global errorlabel
    try:
        newcport=int(Cporttextbox.get())
        if newcport>65535 or newcport<0:
            errorlabel=Label(text="client portに指定できる値は0~25565です                                      ",fg='red')
            errorlabel.place(x=10,y=160)
        else:
            with open('./setting.json','r') as chengeCportfile:
                changeCportfiledic=json.load(chengeCportfile)
                if newcport==changeCportfiledic["serverport"]:
                    errorlabel=Label(text="使用中のserver portと入力したclient portが重複しています",fg='red')
                    errorlabel.place(x=10,y=160)
                else:
                    changeCportfiledic["clientport"]=newcport
            with open('./setting.json','w') as chengeCportfile:
                json.dump(changeCportfiledic,chengeCportfile,indent=4)
    except:
        errorlabel=Label(text="client portに文字は入力できません                                      ",fg='red')
        errorlabel.place(x=10,y=160)

def changeSport():
    global errorlabel
    try:
        newsport=int(Sporttextbox.get())
        if newsport>65535 or newsport<0:
            errorlabel=Label(text="server portに指定できる値は0~25565です                                      ",fg='red')
            errorlabel.place(x=10,y=160)
        else:
            with open('./setting.json','r') as chengeSportfile:
                changeSportfiledic=json.load(chengeSportfile)
                if newsport==changeSportfiledic["clientport"]:
                    errorlabel=Label(text="使用中のclient portと入力したserver portが重複しています",fg='red')
                    errorlabel.place(x=10,y=160)
                else:
                    changeSportfiledic["serverport"]=newsport
        with open('./setting.json','w') as chengeSportfile:
            json.dump(changeSportfiledic,chengeSportfile,indent=4)
    except:
        errorlabel=Label(text="server portに文字は入力できません                                      ",fg='red')
        errorlabel.place(x=10,y=160)
    

def changeip():
    global errorlabel,write
    write=true
    commacount=0
    newip = str(iptextbox.get())
    for i in range(len(newip)):
        try:
            if newip[i]=="." and newip[i+1]==".":
                errorlabel=Label(text="ipに連続したコンマ入力が存在します                                      ",fg='red')
                errorlabel.place(x=10,y=160)
                write=false
        finally:
            if newip[i]==".":
                print("run")
                commacount+=1
    if commacount==3 or write==false:
        for i in range(len(newip)):
            if newip[i].isdecimal()==False and newip[i]!='.':
                print('通過')
                errorlabel=Label(text="server ipに文字は入力できません                                      ",fg='red')
                errorlabel.place(x=10,y=160)
                write=false
        if write==true:
            with open('./setting.json','r') as chengeipfile:
                changeipfiledic=json.load(chengeipfile)
                changeipfiledic["ip_address"]=f"{newip}"
            with open('./setting.json','w') as chengeipfile:
                json.dump(changeipfiledic,chengeipfile,indent=4)
    else:
        errorlabel=Label(text="ipのコンマ数が不足しています                                      ",fg='red')
        errorlabel.place(x=10,y=160)


def main():
    global iptextbox,Sporttextbox,Cporttextbox,accesstextbox
    root=Tk()
    root.title("setting")
    root.resizable(0,0)

    window=Canvas(root,width=500,height=200)
    window.pack()
#------------------<label>
    ipadlabel=Label(text='server ip address')
    ipadlabel.place(x=30,y=30)
    iplabeltxt=Label(text='：接続先ip(ipv4：xxx.xxx.xxx.xxx)')
    iplabeltxt.place(x=150,y=30)

    ipportlabel=Label(text='server port address')
    ipportlabel.place(x=30,y=60)
    ipportlabeltxt=Label(text='：接続先port　　　 (既定：25567)')
    ipportlabeltxt.place(x=150,y=60)

    Cportlabel=Label(text='client port address')
    Cportlabel.place(x=30,y=90)
    Cportlabeltext=Label(text='：接続に使用するport(既定：25568)')
    Cportlabeltext.place(x=150,y=90)

    accesstrylabel=Label(text='number of access')
    accesstrylabel.place(x=30,y=120)
    accesstrylabeltext=Label(text='：接続待ち許容回数  (既定：10)')
    accesstrylabeltext.place(x=150,y=120)
#------------------</label>
    
#------------------<textbox>
    iptextbox=Entry(width=20)
    iptextbox.place(x=350,y=30)
    Sporttextbox=Entry(width=20)
    Sporttextbox.place(x=350,y=60)
    Cporttextbox=Entry(width=20)
    Cporttextbox.place(x=350,y=90)
    accesstextbox=Entry(width=20)
    accesstextbox.place(x=350,y=120)
#-------------------</textbox>

#-------------------<button>
    Adaptationbutton=Button(text="適用",width=7,command=changefile)
    Adaptationbutton.place(x=440,y=160)
    Cancelbutton=Button(text="閉じる",width=7,command=exit)
    Cancelbutton.place(x=370,y=160)
    Wsettingbutton=Button(text="現在の設定",width=7,command=fileopen)
    Wsettingbutton.place(x=300,y=160)
#-------------------</button>

    root.mainloop()

if __name__ =="__main__":
    main()