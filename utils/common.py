#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:40
# @Author  : wenrouyue
# @File    : common.py
import re
from datetime import datetime, date
from typing import Optional, Union
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def getName(first_name, last_name):
    t = ""
    if first_name:
        t += first_name
    if last_name:
        t += last_name
    return t


# 机器人获取自己id
def botGetId(bot):
    return bot.bot_token.split(":")[0]


# 格式化时间字符串
def parseDatetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(dt, date):
        return dt.strftime('%Y-%m-%d')
    return None


def getButtonList(button_list: Optional[Union[InlineKeyboardMarkup, None]], param):
    if button_list:
        existing_buttons = button_list.inline_keyboard
        existing_buttons.append(
            [InlineKeyboardButton(text=getRButton().get("key"), callback_data=f"返回?page={param}")]
        )
        button_list = InlineKeyboardMarkup(existing_buttons)
    else:
        button_list = InlineKeyboardMarkup([
            [InlineKeyboardButton(text=getRButton().get("key"), callback_data=f"返回?page={param}"), ],
        ])
    return button_list


def getRButton():
    return {"key": "↩️ 返回"}


def getRClose():
    return {"key": "❌️ 关闭", "value": "通用关闭"}


"""
['goudan', '1126', '?comment=24901']
免费校验的方法，发送多条也只取第一条
index 0 用户名
index 1 消息id
index 2 其他参数 包含 comment就是评论
"""


def checkTgLink(text):
    pattern2 = r"https://t.me/(?!c/)(.*?)/([1-9]\d*)(.*)"
    match = re.search(pattern2, text)
    if match:
        return list(match.groups())
    else:
        return []


def checkTgToujiaLink(text):
    pattern2 = r"https://t.me/c/(.*?)/([1-9]\d*)(.*)"
    match = re.search(pattern2, text)

    if match:
        return [f"-100{match.groups()[0]}", match.groups()[1]]
    else:
        return []


def getVipLvToStr(level):
    text = ""
    if level == "0":
        text = "⚪️ 非会员"
    if level == "1":
        text = "🔵 转发会员"
    if level == "2":
        text = "🟣 下载会员"
    return text


def getChoicePayToStr(dist):
    text = "您正在充值\n\n"
    money = getPayMoneyToStr(dist)
    t = "月付" if dist["t"] == "m" else "试用版"
    if dist["v"] == "1":
        text += f"🔵 转发会员-{t} {money}￥"
    if dist["v"] == "2":
        text += f"🟣 下载会员-{t} {money}￥"
    text += "\n\n请点击按钮选择您的支付方式！"
    return text


def getPayMoneyToStr(dist):
    text = "30"
    if dist["v"] == "1":
        text = "30" if dist["t"] == "m" else "10"
    if dist["v"] == "2":
        text = "200" if dist["t"] == "m" else "30"
    return text


def replace_links(text):
    """
    替换文本中的所有 URL、Telegram 链接和以 @ 开头的用户名为 'hello world'。

    参数：
    text (str): 输入文本。

    返回：
    str: 替换后的文本。
    """
    # 正则表达式匹配各种 URL、Telegram 链接和以 @ 开头的用户名
    new_text = None
    if text:
        new_text = re.sub(
            r'https?://\S+|.\.\S+|@\w+|[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+',
            '',
            text
        )
    return new_text


def get_today():
    now = datetime.now()
    year = now.year
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    return f'{year}{month}{day}'

def parse_input(text: str) -> dict:
    """
    解析用户输入
    Args:
        text:

    Returns:

    """
    task_info = {}
    for line in text.strip().splitlines():
        if "：" in line:  # 使用中文全角冒号分割
            key, _, value = line.partition("：")
            task_info[key.strip()] = value.strip()
    return task_info

if __name__ == '__main__':
    print(checkTgLink("https://t.me/c/1886369298/9369"))
    print(checkTgLink("https://t.me/ccbbaaw1/4381"
                      "https://t.me/jk45670/4381?single"))
    print(checkTgLink("https://t.me/jk45670/4381?single"))
    print(checkTgLink("https://t.me/goudan/1126?comment=24901"))
    print(checkTgToujiaLink("https://t.me/c/2298147455/67"))
    # 示例用法
    input_text = (
        "加入我们的 Telegram 群组 https://t.me/example_group，"
        "访问我们的网站 www.example.com，"
        "或者联系 @username，"
        "还有其他链接 like example/path 或 example/anotherPath。"
        "哈哈 xxx.xxx.xx xxx.xx"
    )
    output_text = replace_links(input_text)

    print(output_text)
