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

    async def delReplyAndSendNotice(self, send_text, flag, button_list=None):
        """
        直接删除机器人的请求回复，和用户的回复消息，并且发送通知
        @param send_text: 通知文本
        @param flag: True发送✅️ 样式，False发送❌️ 样式 (仅无按钮时生效)
        @param button_list: 按钮列表，传此参数将发送持久消息，否则发送5秒自动删除消息
        @return:
        """
        await self.botMessage.delete_msg(self.chatId, self.replyMsgId)
        await self.botMessage.delete_msg(self.chatId, self.baseMsg.id)
        if button_list:
            await self.botMessage.send_message(send_text, button_list)
        else:
            if flag:
                await self.botMessage.st(f"✅️ {send_text}", 'del')
            else:
                await self.botMessage.st(f"❌️ {send_text}", 'del')

    async def delReply(self):
        """
        直接删除机器人的请求回复，和用户的回复消息
        @return:
        """
        await self.botMessage.delete_msg(self.chatId, self.replyMsgId)
        await self.botMessage.delete_msg(self.chatId, self.baseMsg.id)

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

    async def getChatByHttps(self, link: str) -> int:
        """
        根据频道链接解析其 chat_id，支持私密和公开链接
        :param link: Telegram 链接（如 https://t.me/c/123456789 或 https://t.me/channel_username）
        :return: chat_id 字符串（私密格式为 -100xxxx）
        """
        if common.is_private_link(link):
            return int(f"-100{link.split('/')[-1]}")
        else:
            username = link.split("/")[-1]
            chat = await self.bot.get_chat(f"@{username}")
            return int(chat.id)

    @staticmethod
    def get_reply_messages():
        return {
            "fbot_reply": "回复机器人TOKEN\n请点击此条消息进行回复！",
            "fbot_reply111": "回复机器人TOKEN111\n请点击此条消息进行回复！",
            "change_password": "请输入新密码\n请直接回复此消息，输入您想设置的新密码（建议6位以上字符）"
        }

    async def inputError(self, url):
        """
        处理输入异常，重新触发回复
        @param url: {"change_password": "错误提示信息"}
        """
        key = next(iter(url.keys()))
        error_text = url.get(key)
        reply_messages = self.get_reply_messages()

        if key in reply_messages:
            base_text = reply_messages[key]
            # 组合原始提示和错误信息
            full_text = f"{base_text}\n\n{error_text}"
            await self.botMessage.send_reply(full_text)

    @staticmethod
    def check_safe_input(send_text):
        """
        验证输入是否安全（只允许大小写字母、数字及部分安全特殊字符）
        且必须包含至少一种字符（可根据需求调整复杂度，目前仅做白名单校验防止注入）
        允许的特殊字符：!@#$%^&*()_+-=[]{};':",.<>/?
        禁止的特殊字符：` (反引号), | (管道符), \ (反斜杠) 回车
        """
        # 白名单正则：字母、数字、及安全符号
        # 注意转义：\- \]
        pattern = r"^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{};':\",.<>/?]*$"
        if not re.match(pattern, send_text):
            return False
        return True
