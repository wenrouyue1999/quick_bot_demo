#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:15
# @Author  : wenrouyue
# @File    : father_page.py
from typing import Optional, Union

from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

from utils import common
from utils.bot_message import BotMessage


class BasePage:
    def __init__(self, bot_data=None, callbackQuery: Optional[Union[Message, CallbackQuery]] = None):
        self.bot_data = bot_data
        self.baseMsg: Optional[Union[Message, CallbackQuery]] = callbackQuery
        self.botMessage: Optional[BotMessage] = None
        self.botMessageByUser: Optional[BotMessage] = None
        if bot_data:
            self.bot: Optional[Client] = bot_data.get('bot')
            self.chatId = int(bot_data.get('chat_id'))
            self.userId = int(bot_data.get('user_id'))
            self.replyText = bot_data.get('reply_text')
            self.replyToText = bot_data.get('reply_to_text')
            self.replyMsgId = bot_data.get('reply_msg_id')
            self.buttonReplyMsgId = bot_data.get('button_reply_msg_id')
            self.userName = bot_data.get('user_name')
            self.name = bot_data.get('name')
        if isinstance(callbackQuery, Message):
            self.messageId = int(callbackQuery.id)
        elif isinstance(callbackQuery, CallbackQuery):
            self.messageId = int(callbackQuery.message.id)

    def setAttributes(self, params):
        if params:
            for key, value in params.items():
                setattr(self, key, value)

    def getBotMessage(self, args=None):
        if isinstance(self.baseMsg, Message):
            self.name = common.getName(self.baseMsg.chat.first_name, self.baseMsg.chat.last_name)
            self.userName = self.baseMsg.chat.username
        if args:
            self.botMessageByUser = BotMessage(self.bot, None, args)
            return self.botMessageByUser
        else:
            self.botMessage = BotMessage(self.bot,
                                         self.baseMsg)
            return self.botMessage
