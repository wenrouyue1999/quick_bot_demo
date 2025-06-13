#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:15
# @Author  : wenrouyue
# @File    : father_page.py
import math

from utils.bot_message import BotMessage
from import_utils import *


class BasePage:
    def __init__(self, bot_data=None, callbackQuery: Optional[Union[Message, CallbackQuery]] = None):
        self.bot_data = bot_data
        self.baseMsg: Optional[Union[Message, CallbackQuery]] = callbackQuery
        self.botMessage: Optional[BotMessage] = None
        self.botMessageByUser: Optional[BotMessage] = None
        if bot_data:
            self.bot: Optional[Client] = bot_data.get('bot', None)
            self.chatId: int = int(bot_data.get('chat_id', 0))
            self.userId: int = int(bot_data.get('user_id', 0))
            self.replyText: Optional[str] = bot_data.get('reply_text', None)
            self.replyToText: Optional[str] = bot_data.get('reply_to_text', None)
            self.replyMsgId: int = int(bot_data.get('reply_msg_id', 0))
            self.buttonReplyMsgId: int = int(bot_data.get('button_reply_msg_id', 0))
            self.userName: Optional[str] = bot_data.get('user_name', None)
            self.name: Optional[str] = bot_data.get('name', None)
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

    async def handle_send(self, send_text, flag):
        await self.botMessage.delete_msg(self.chatId, self.replyMsgId)
        await self.botMessage.delete_msg(self.chatId, self.baseMsg.id)
        if flag:
            await self.botMessage.st(f"✅️ {send_text}", 'del')
        else:
            await self.botMessage.st(f"❌️ {send_text}", 'del')

    @staticmethod
    def getDeleteButton():
        return InlineKeyboardMarkup([[InlineKeyboardButton(text="❌️ 关闭", callback_data=f"通用关闭")]])

    @staticmethod
    def getPaginationButton(page: int, page_size: int, total: int, callback_prefix: str) -> list:
        """生成分页按钮：首页、上一页、下一页、尾页"""
        total_pages = math.ceil(total / page_size)
        buttons = []

        # 首页按钮（第一页禁用）
        first_button = InlineKeyboardButton(
            "⏮ 首页",
            callback_data=f"{callback_prefix}?page=1&page_size={page_size}" if page > 1 else "分页异常?t=first_button"
        )
        # 上一页按钮（第一页禁用）
        prev_button = InlineKeyboardButton(
            "⬅️ 上一页",
            callback_data=f"{callback_prefix}?page={page - 1}&page_size={page_size}" if page > 1 else "分页异常?t=prev_button"
        )
        # 下一页按钮（最后一页禁用）
        next_button = InlineKeyboardButton(
            "下一页 ➡️",
            callback_data=f"{callback_prefix}?page={page + 1}&page_size={page_size}" if page < total_pages else "分页异常?t=next_button"
        )
        # 尾页按钮（最后一页禁用）
        last_button = InlineKeyboardButton(
            "尾页 ⏭",
            callback_data=f"{callback_prefix}?page={total_pages}&page_size={page_size}" if page < total_pages else "分页异常?t=last_button"
        )

        # 单行显示所有分页按钮
        buttons.append([first_button, prev_button, next_button, last_button])
        return buttons
