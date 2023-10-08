import json
import os

# 获取所有用户的游戏列表
def get_all_info(jsondata,assetspath):
    if os.path.exists(assetspath)==True:    
        with open(assetspath,"r",encoding="utf-8") as f:
            assetsdata=json.load(f)
    else:
        assetsdata=[]
        
    #对于json来说，三个变量相互关联的话，我必须至少创建出两个字典，确保数据的一致性
    gamename2aliasdict={} #游戏名与别名的对应字典
    gamename2urldict={} #游戏名与url的对应字典
    
    #读取assets.json，获取别名与url的对应字典
    for i in assetsdata: #一个i是一个字典{"name":"osu","alias":["osu","osu!"],"url":"https://osu.ppy.sh"}
        gamename2aliasdict.update({i["name"]:i["alias"]})
        gamename2urldict.update({i["name"]:i["url"]})

    #获取储存的玩家游戏列表
    gamenametemplist=[]
    for i in jsondata: #一个i是一个字典{"114514":["osu","malody"]}
        for value in i.values():
            gamenametemplist.extend(value)
            gamenametemplist=list(set(gamenametemplist)) #去重
    
    #替换别名,没有就是输入的alias当作游戏名
    allgamelists=[]
    is_convert=False #草这是什么解决方案啊，后面这个获取别名的我真的想不到其他方法能够替换别名成游戏名了
    for i in gamenametemplist: #一个i是一个alias列表的一个值
        if gamename2aliasdict=={}:
            allgamelists.append(i)
            continue
        for key,value in gamename2aliasdict.items(): #key是一个游戏名，一个value是一个别名列表(alias)
            if i in value: #如果i在values内,就把key加入allgamelists
                allgamelists.append(key)
                is_convert=True
                break
        if is_convert==False:
            allgamelists.append(i)
    allgamelists=list(set(allgamelists)) #去重
    allgamelists.sort() #排序

    return allgamelists,gamename2aliasdict,gamename2urldict
 

# 删除用户
def deleteplayer(jsondata,qq,filepath):
    newjsondata=[]
    for i in jsondata:
        for k in i.keys(): #k是字典,key是qq号,value是游戏列表
            if k != qq:
                newjsondata.append(i)
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)

# 添加用户和游戏列表
def addplayer(jsondata,qq,gamelists,filepath,gamename2aliasdict):
    #替换别名,没有就是输入的alias当作游戏名




    newgamelists=[]
    for i in gamelists: #一个i是一个alias列表的一个值
        is_convert=False #草这是什么解决方案啊，后面这个获取别名的我真的想不到其他方法能够替换别名成游戏名了
        if gamename2aliasdict=={}:
            newgamelists.append(i)
            continue
        for key,value in gamename2aliasdict.items(): #value是一个别名列表(alias)
            if i in value:
                newgamelists.append(key)
                is_convert=True
                break
        if is_convert==False:
            newgamelists.append(i)
            
    newgamelists=list(set(newgamelists)) #去重

    #修改jsondata然后写入文件
    newjsondata=[]
    if jsondata == []:
        newjsondata.append({qq:newgamelists})
    else:
        for i in jsondata: 
            if qq in i.keys():
                i.update({qq:newgamelists})
            newjsondata.append(i)

    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)