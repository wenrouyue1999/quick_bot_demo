#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/16 下午5:17
# @Author  : wenrouyue
# @File    : child_page.py

from import_utils import *
from page.base_page import BasePage

config_load = load_config()


class ChildPage(BasePage):

    def __init__(self, botData, callbackQuery):
        super().__init__(botData, callbackQuery)
        self.bot_type = "child_bot"

    async def returnLast(self, url):
        if url:
            log.info(f"ChildPage returnLast 有参数。。。 进行处理：{url}")
        param = url.get("page")
        if param == 'start':
            await self.bot.delete_messages(self.chatId, self.messageId)
            await self.botStart("returnLast")

    async def botStart(self, url):
        if url:
            log.info(f"start 有参数。。。 进行处理：{url}")
        else:
            # todo db_bot is_vip 默认True处理，仅模板测试使用
            db_bot = True
            if db_bot:
                send_text = f"💎 <b>{self.name}</b> 您好！欢迎使用子机器人！"
                button_list = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🧑‍💼 子机器人下一级", callback_data="子机器人下一级"),
                     InlineKeyboardButton(text="💰️ 子机器人回复", callback_data="回复?cbot_reply=1"), ]])
                is_vip = True
                if not is_vip:
                    return
            else:
                send_text = "此机器人为会员独享机器人，您无法使用哦！"
                button_list = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🤖 公共机器人", url="https://t.me/bot_father")]])
            await self.botMessage.send(send_text, button_list)

    async def botInput(self, url):
        """
        这里的url 则是按钮的设置的callback_data 必须设置?key=1 否则url解析不出来参数
        """
        key = next(iter(url.keys()))
        reply_messages = {
            "cbot_reply": "回复机器人TOKEN\n请点击此条消息进行回复！",
            "cbot_reply111": "回复机器人TOKEN111\n请点击此条消息进行回复！",
        }
        if key in reply_messages:
            await self.botMessage.send_reply(reply_messages[key])

    async def handleBotToken(self):
        """
        处理回复的方法，不需要接收url ，url仅针对按钮callback_data
        """
        log.info(self.baseMsg.text)
        await self.botMessage.st(f"{self.bot_type + ':' + self.baseMsg.text}", 'del')

    async def botNext(self, url):
        """
        构建测试下级页面。带返回按钮
        """
        if url:
            log.info(f"botNext 参数：{url}")
        send_text = f"<b>【🌟 {self.bot_type} 🌟】</b>\n\n"
        button_list = InlineKeyboardMarkup([[InlineKeyboardButton(text="无效按钮", callback_data="无效按钮")], ])
        await self.botMessage.returnLastByCallBackQuery(send_text, button_list, "start")
