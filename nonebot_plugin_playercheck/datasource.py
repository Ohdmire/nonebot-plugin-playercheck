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
        for k in i.keys(): #k是qq号
            if k != qq:
                newjsondata.append(i)
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)

# 添加用户和游戏列表
def addplayer(jsondata,qq,gamelists,filepath,gamename2aliasdict):
    #替换别名,没有就是输入的alias当作游戏名
    newgamelists=[] #这是一个新的列表,用来存放替换后的游戏名
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

    #这个循环结束后，newgamelists就是替换后的游戏名列表
    #newgamelists是新游戏列表，还需要合并原来的游戏列表

    newgamelists=list(set(newgamelists)) #去重
    #复制jsondata然后再新加入
    newjsondata=[] #用来存放新的jsondata
    #特殊情况第一次添加
    if len(jsondata) == 0:
        newjsondata.append({qq:newgamelists})
    else:
        qqlists=[] #用来存放jsondata里面的qq号
        qqlists.extend([list(i.keys())[0] for i in jsondata]) #这里是把jsondata里面的qq号提取出来
        #字典i只有一个所以只循环了一遍，所以这一段代码是对于第一次添加的和修改原来的代码，这里不适用于如果加入了新的qq号
        for i in jsondata: #一个i是一个字典
            for j,k in i.items(): #j是qq号,k是游戏列表。这一次循环过后，newjsondata里面储存的是一位用户的数据，格式是[{"qq号":["游戏1","游戏2"]}]
                if j != qq: #如果不是要添加的qq号,就直接加入，这样原来的数据就什么都不做
                    newjsondata.append(i) 
                    if qq not in qqlists: #新用户就应该直接添加
                        newjsondata.append({qq:newgamelists})

                else: #如果是要添加的qq号,就把游戏列表合并,再删除，再添加
                    newgamelists.extend(k) #k是原来的游戏列表
                    newgamelists=list(set(newgamelists)) #去重
                    newjsondata.append({qq:newgamelists})
 
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)
    
    result='的成分列表为：\n{}'.format(newgamelists)
    return result


# 替换别名然后保存到json
def update_alias2name(jsondata,gamename2aliasdict,filepath):
    newjsondata=[]
    for i in jsondata: #一个i是一个字典,例如{"114514":["osu","malody"]}
        templists=[] #用来存放替换后的游戏名
        for key,value in i.items(): #key是qq号,value是游戏列表
            # 循环到单个qq的游戏列表全部替换完成
            for j in value: #j单个游戏名
                is_convert=False
                if gamename2aliasdict=={}:
                    templists.append(j)
                    continue
                for key2,value2 in gamename2aliasdict.items(): #key2是游戏名,value2是别名列表
                    if j in value2:
                        templists.append(key2)
                        is_convert=True
                        break
                if is_convert==False:
                    templists.append(j)
            #这里是单个qq号的游戏列表替换完成了，已经加入templists了
            templists=list(set(templists)) #去重
            newjsondata.append({key:templists})

            
            

    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(newjsondata, f,ensure_ascii=False)

