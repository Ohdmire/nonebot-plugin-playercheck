import json
import os
import operator


# 获取所有用户的游戏列表
def getallgame(jsondata,assetspath):
    def getgamename(gamename):
        if os.path.exists(assetspath)==True:
            with open(assetspath,"r",encoding="utf-8") as f:
                jsondata=json.load(f)
            for i in jsondata:
                if gamename in i["alias"]:
                    return i["name"]
            return gamename
        else:
            return gamename
    
    def getpicurl(gamename):
        if os.path.exists(assetspath)==True:
            with open(assetspath,"r",encoding="utf-8") as f:
                jsondata=json.load(f)
            for i in jsondata:
                if gamename in i["name"]:
                    return i["url"]
                pass
        else:
            pass

    allgamelists=[]
    playerdict={} #玩家字典，key是qq，value是游戏列表
    gamecoverdict={} #游戏封面字典，key是游戏名，value是封面url
    for i in jsondata: #每一个i是一个用户
        allgame=i["gamelists"]
        nametemplist=[]
        for j in allgame:
            j=getgamename(j)
            nametemplist.append(j) #替换别名
            playerdict[i["qq"]]=nametemplist
            if j not in allgamelists:
                allgamelists.append(j)
    
    for i in allgamelists: #获取游戏封面
        gamecoverdict[i]=getpicurl(i)

    allgamelists.sort()
    sort_key_dic_instance = dict(sorted(playerdict.items(), key=operator.itemgetter(0)))  #按照key值升序


    return allgamelists,sort_key_dic_instance,gamecoverdict

# 删除用户
def deleteplayer(jsondata,qq,filepath):
    newjsondata=[]
    for i in jsondata:
        if i["qq"]==qq:
            pass
        else:
            newjsondata.append(i)
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata,f,ensure_ascii=False)

# 添加用户和游戏列表
def addplayer(jsondata,qq,gamelists,filepath):
    newjsondata=[]
    for i in jsondata:
        if i["qq"]==qq:
            pass
        else:
            newjsondata.append(i)
    newjsondata.append({"qq":qq,"gamelists":gamelists})
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)
