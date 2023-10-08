from nonebot import on_command,require
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot,Message,MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from .datasource import get_all_info,deleteplayer,addplayer

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-playercheck",
    description="一个查询群友音游成分的插件",
    usage="cf.add [游戏名1,游戏名2...] 添加游戏\n"
          "cf.del 删除游戏\n"   
          "cf.list 查询游戏列表\n",

    type="application",
    homepage="https://github.com/ohdmire/nonebot-plugin-playercheck",
    supported_adapters={"~onebot.v11"},
)


import json
from pathlib import Path
import operator

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic

data_path=Path(".") / "data" / "playercheck"
template_path=str(Path(__file__).parent / "templates")
template_name = "main.html"

# 获取所有用户的游戏列表
get_list = on_command("cf.list",priority=5, block=True)
@get_list.handle()
async def getlist (event: GroupMessageEvent, bot: Bot):
    #读取数据部分
    data_path.mkdir(parents=True, exist_ok=True)
    if Path(str(data_path)+"/"+event.get_session_id().split("_")[1]+".json").exists()==False:
        with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","w+",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False)
    with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","r",encoding="utf-8") as f:
        jsondata=json.load(f)

    allgamelists,gamename2aliasdict,gamename2urldict=get_all_info(jsondata,assetspath=str(data_path)+"/"+"assets.json")

    #这里处理一下群友列表，把qq号和群名片对应起来，没有就用昵称
    groupmemberlists=await bot.get_group_member_list(group_id=event.get_session_id().split("_")[1])
    user2cardname={}
    for i in groupmemberlists: #i是一个字典，包含qq，群名片，昵称等信息
        userqq=i["user_id"]
        usercardname=i["card"]
        if usercardname == "":
            usercardname=i["nickname"]
        user2cardname.update({str(userqq):str(usercardname)})

    #按照群名片排序
    user2cardname = dict(sorted(user2cardname.items(), key=operator.itemgetter(1)))

    #playerdict就是jsondata
    templates={"allgamelists":allgamelists, "jsondata":jsondata,"user2cardname" :user2cardname, "gamename2urldict":gamename2urldict}
    pages={ "viewport": { "width": 1600,"height": 1000 } } 
    content = await template_to_pic(template_path=template_path,template_name=template_name,templates=templates,pages=pages)
    await get_list.send(MessageSegment.image(content))

# 删除用户
delete_user = on_command("cf.del",priority=5, block=True)
@delete_user.handle()
async def deleteuser (event: GroupMessageEvent):
    with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","r",encoding="utf-8") as f:
        jsondata=json.load(f)
    deleteplayer(jsondata=jsondata,qq=event.get_user_id(),filepath=str(data_path)+"/"+event.get_session_id().split("_")[1]+".json")
    await delete_user.finish("删除完毕")

# 添加用户
add_user = on_command("cf.add",priority=5, block=True)
@add_user.handle()
async def adduser (event: GroupMessageEvent, args: Message = CommandArg()):
    #这里多了个判断，第一次用应该没有创建群号.json，所以要创建
    data_path.mkdir(parents=True, exist_ok=True)
    if Path(str(data_path)+"/"+event.get_session_id().split("_")[1]+".json").exists()==False:
        with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","w+",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False)
    #这里和删除用户的部分一样
    with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","r",encoding="utf-8") as f:
        jsondata=json.load(f)
    gamename2aliasdict=get_all_info(jsondata,assetspath=str(data_path)+"/"+"assets.json")[1]
    addplayer(jsondata=jsondata,qq=event.get_user_id(),gamelists=args.extract_plain_text().split(","),gamename2aliasdict=gamename2aliasdict,filepath=str(data_path)+"/"+event.get_session_id().split("_")[1]+".json")
    await add_user.finish("添加完成")

#TO DO私聊部分