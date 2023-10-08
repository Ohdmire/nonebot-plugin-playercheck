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

    # 想增加个按游玩人数排序
    # 先生成一个游戏名和游玩人数的字典
    gamename2playernumdict={} 
    for i in allgamelists:
        if i not in gamename2playernumdict.keys():
            gamename2playernumdict.update({i:0}) #key是游戏名,value是游玩人数
    for i in jsondata: #一个i是一个字典{"114514":["osu","malody"]}
        for key,value in i.items(): #key是qq号,value是游戏列表
            for j in value: #j单个游戏名
                if j in gamename2playernumdict.keys():
                    gamename2playernumdict[j]+=1

    # 按照游玩人数排序
    allgamelists.sort(key=lambda x:gamename2playernumdict[x],reverse=True) #排序

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
    #复制jsondata然后再新加入
    newjsondata=[]
    if jsondata == []:
        newjsondata.append({qq:newgamelists})
    else:
        for i in jsondata: #一个i是一个字典
            for j,k in i.items(): #j是qq号,k是游戏列表
                if j != qq:
                    newjsondata.append(i)  

        newgamelists.extend(k) #k是原来的游戏列表
        newgamelists=list(set(newgamelists)) #去重
        newjsondata.append({qq:newgamelists})


    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)

# 替换别名然后保存到json
def update_alias2name(jsondata,gamename2aliasdict,filepath):
    newjsondata=[]
    for i in jsondata: #一个i是一个字典,一个key是qq号,value是游戏列表
        templists=[]
        for key,value in i.items():
            for j in value: #j单个游戏名
                if gamename2aliasdict=={}:
                    templists.append(j)
                    continue
                is_convert=False
                for key2,value2 in gamename2aliasdict.items(): #key2是游戏名,value2是别名列表
                    if j in value2:
                        templists.append(key2)
                        is_convert=True
                        break
                if is_convert==False:
                    templists.append(j)
        templists=list(set(templists)) #去重
        newjsondata.append({key:templists})
            
            

    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)

