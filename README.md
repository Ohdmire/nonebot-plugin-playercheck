<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-playercheck

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-playercheck.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-playercheck">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-playercheck.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

一个查询群友音乐成分的插件


## 📖 介绍

将群友成分储存于json文件，并使用[nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)的template渲染网页


## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-playercheck

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-playercheck
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-playercheck
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-playercheck
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-playercheck
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_playercheck"]

</details>

## ⚙️ 配置

可以将本项目中的`assert`文件夹内的`assert.json`拖入你机器人目录的`/data/playercheck`文件夹内
这样可以获取游戏别名和游戏图片

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| cf.add | 主人 | 否 | 群聊 | `cf.add osu,malody` 会替换原来的游戏列表 |
| cf.del| 群员 | 否 | 群聊 | 删除用户输入的所有游戏列表 |
| cf.list| 群员 | 否 | 群聊 | 渲染图片 |
### 效果图
> 如果没有从群内获取到该玩家的信息，则会返回None

![效果](assert\效果图.PNG)