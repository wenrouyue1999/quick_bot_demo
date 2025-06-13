#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:15
# @Author  : wenrouyue
# @File    : father_page.py

from import_utils import *
from page.base_page import BasePage


class FatherPage(BasePage):

    def __init__(self, botData, callbackQuery):
        # 默认机器人类型
        self.bot_type = "father_bot"
        super().__init__(botData, callbackQuery)
        self.getBotMessage()

    async def returnLast(self, url):
        if url:
            log.info(f"FatherPage returnLast 有参数。。。 进行处理：{url}")
        param = url.get("page")
        if param == 'start':
            await self.bot.delete_messages(self.chatId, self.messageId)
            await self.botStart("returnLast")

    async def botStart(self, url):
        if url and url != "returnLast":
            log.info(f"start 有参数。。。 进行处理：{url}")
        else:
            send_text = f"💎 <b>{self.name}</b> 您好！欢迎使用{self.bot_type}！"
            button_list = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="🧑‍💼 父机器人下一级", callback_data="父机器人下一级"),
                 InlineKeyboardButton(text="💰️ 父机器人回复", callback_data="回复?fbot_reply=1"), ]])
            await self.botMessage.send(send_text, button_list)

    async def botInput(self, url):
        """
        这里的url 则是按钮的设置的callback_data 必须设置?key=1 否则url解析不出来参数
        """
        key = next(iter(url.keys()))
        reply_messages = {
            "fbot_reply": "回复机器人TOKEN\n请点击此条消息进行回复！",
            "fbot_reply111": "回复机器人TOKEN111\n请点击此条消息进行回复！",
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

    async def closeMessage(self, url):
        if url:
            log.info(f"closeMessage 有参数。。。 进行处理：{url}")
        await self.botMessage.delete_msg(self.chatId, self.messageId)

    async def pageError(self, url):
        if url:
            log.info(f"pageError 有参数。。。 进行处理：{url}")
            t = url.get('t', 'error')
            send_text = "分页异常"
            if t == "first_button":
                send_text = "当前为首页"
            if t == "prev_button":
                send_text = "没有上一页"
            if t == "next_button":
                send_text = "没有下一页"
            if t == "last_button":
                send_text = "当前为尾页"
            await self.baseMsg.answer(send_text,True)
