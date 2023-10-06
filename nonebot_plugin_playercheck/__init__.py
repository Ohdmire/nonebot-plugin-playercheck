from nonebot import on_command,require
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot,Message,MessageSegment
from nonebot.params import CommandArg
from .datasource import getallgame,deleteplayer,addplayer

import json
from pathlib import Path


require("nonebot_plugin_htmlrender")

from nonebot_plugin_htmlrender import template_to_pic


data_path=Path(".") / "data" / "playercheck"
template_path=str(Path(__file__).parent / "templates")
template_name = "main.html"

get_list = on_command("list",priority=5, block=True)
# 获取所有用户的游戏列表
@get_list.handle()
async def getlist (event: GroupMessageEvent, bot: Bot):
    data_path.mkdir(parents=True, exist_ok=True)
    if Path(str(data_path)+"/"+event.get_session_id().split("_")[1]+".json").exists()==False:
        with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","w+",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False)
    with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","r",encoding="utf-8") as f:
        jsondata=json.load(f)
    allgamelists,playerdict,gamecoverdict=getallgame(jsondata,assertpath=str(data_path)+"/"+"assert.json")
    usergroupdict={}
    for i in playerdict.keys():
        try:
            useringroupname=await bot.get_group_member_info(group_id=event.get_session_id().split("_")[1],user_id=i)
            usergroupname=useringroupname["card"]
            if usergroupname == "":
                usergroupname=useringroupname["nickname"]
            usergroupdict[i]=usergroupname
        except:
            usergroupdict[i]="None"
    templates={"allgamelists":allgamelists, "playerdict":playerdict,"usergroupdict" :usergroupdict, "gamecoverdict":gamecoverdict}
    pages={ "viewport": { "width": 1600,"height": 1000 } } 
    content = await template_to_pic(template_path=template_path,template_name=template_name,templates=templates,pages=pages)
    await get_list.send(MessageSegment.image(content))

delete_user = on_command("del",priority=5, block=True)
# 删除用户
@delete_user.handle()
async def deleteuser (event: GroupMessageEvent):
    with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","r",encoding="utf-8") as f:
        jsondata=json.load(f)
        deleteplayer(jsondata=jsondata,qq=event.get_user_id(),filepath=str(data_path)+"/"+event.get_session_id().split("_")[1]+".json")
    await delete_user.finish("删除完毕")

add_user = on_command("add",priority=5, block=True)
# 添加用户
@add_user.handle()
async def adduser (event: GroupMessageEvent, args: Message = CommandArg()):
    data_path.mkdir(parents=True, exist_ok=True)
    if Path(str(data_path)+"/"+event.get_session_id().split("_")[1]+".json").exists()==False:
        with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","w+",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False)
    with open (str(data_path)+"/"+event.get_session_id().split("_")[1]+".json","r",encoding="utf-8") as f:
        jsondata=json.load(f)
        addplayer(jsondata=jsondata,qq=event.get_user_id(),gamelists=args.extract_plain_text().split(","),filepath=str(data_path)+"/"+event.get_session_id().split("_")[1]+".json")
    await add_user.finish("添加完成")
