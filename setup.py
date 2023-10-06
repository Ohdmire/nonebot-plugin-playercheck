# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r",encoding="UTF-8") as f:
    long_description = f.read()

setuptools.setup(
    name="nonebot-plugin-playercheck",
    version="1.0.0",
    author="ohdmire",
    author_email="1750011571@qq.com",
    description="Nonebot2 群友音游成分查询",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ohdmire/nonebot-plugin-playercheck",
    project_urls={
        "Bug Tracker": "https://github.com/ohdmire/nonebot-plugin-playercheck/issues",
    },
    packages=["nonebot_plugin_playercheck"],
    python_requires=">=3.8,<4.0",
    install_requires=[
        "nonebot2>=2.0.0a16",
        "nonebot-adapter-onebot>=2.0.0b1",
        "nonebot_plugin_htmlrender"
    ],
)