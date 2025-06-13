#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:24
# @Author  : wenrouyue
# @File    : bot_message.py

from pyrogram.enums import ParseMode
from import_utils import *


class BotMessage:
    def __init__(self, bot, msg, *args):
        self.bot: Optional[Client] = bot
        self.msg: Optional[Union[Message, CallbackQuery]] = msg
        if isinstance(self.msg, CallbackQuery):
            # callback消息
            self.chat_id = self.msg.message.chat.id
            self.msg_id = self.msg.message.id
        elif isinstance(self.msg, Message):
            self.chat_id = self.msg.chat.id
            self.msg_id = self.msg.id
        else:
            self.chat_id = args[0]

    async def send_again_reply(self, send_text, msg_id):
        try:
            send_text += f"\n\n消息id：{msg_id}"
            await self.bot.send_message(self.chat_id, send_text, reply_markup=ForceReply(selective=True),
                                        parse_mode=ParseMode.HTML)
        except Exception as e:
            log.info(e)
            log.info(f"BotMessage.send_again_reply 发送消息失败！text：{send_text}\nmsgId：{msg_id}")

    async def send_reply(self, send_text, msg_id=None):
        try:
            if msg_id:
                send_text += f"\n\n消息id：{msg_id}"
            else:
                send_text += f"\n\n消息id：{self.msg_id}"

            await self.bot.send_message(self.chat_id, send_text, reply_markup=ForceReply(selective=True),
                                        parse_mode=ParseMode.HTML)
        except Exception as e:
            log.info(e)
            log.info(f"BotMessage.send_reply 发送消息失败！text：{send_text}\nid：{msg_id}")

    async def st(self, send_text, del_flag=None, *args):
        try:
            send = self.chat_id
            if args:
                send = args[0]
            if del_flag != "del":
                sent_message = await self.bot.send_message(send, send_text, parse_mode=ParseMode.HTML)
            else:
                sent_message = await self.bot.send_message(send, send_text, parse_mode=ParseMode.HTML)
                await self.delete_timeout(send, sent_message.id)
            return sent_message
        except Exception as e:
            log.info(e)
            log.info(f"BotMessage.st 发送消息失败！text：{send_text}\ndel：{del_flag}\nargs：{args}")

    async def send(self, send_text, button_list):
        try:
            send = self.chat_id
            await self.bot.send_message(send, send_text, reply_markup=button_list, parse_mode=ParseMode.HTML,
                                        disable_web_page_preview=True)
        except Exception as e:
            log.info(e)
            log.info(f"BotMessage.send 发送消息失败！send_text：{send_text}\nbuttonList：{button_list}")

    async def send_message(self, send_text, button_list, **kwargs):
        """
        发送消息，text 为必传字段，其他参数透传给 pyrogram.send_message
        Args:
            send_text (str): 消息文本
            **kwargs: 其他参数，如 reply_markup, parse_mode, entities 等
        Returns:
            types.Message: 发送的消息对象
            @param send_text: 发送文本
            @param button_list: 按钮
        """
        try:
            sent_message = await self.bot.send_message(
                chat_id=self.chat_id,
                text=send_text,
                parse_mode=ParseMode.HTML,  # 默认 HTML 解析
                disable_web_page_preview=True,  # 默认禁用网页预览
                reply_markup=button_list,
                **kwargs  # 透传其他参数
            )
            return sent_message
        except Exception as e:
            log.info(f"BotMessage.send_message 发送消息失败！send_text: {send_text},buttonList：{button_list} kwargs: {kwargs}, error: {e}")
            raise

    async def delete_timeout(self, chat_id, message_id):
        await asyncio.sleep(5)
        try:
            await self.bot.delete_messages(chat_id, message_id)
        except Exception as e:
            log.info(e)

    async def send_order_photo(self, send_text, qrcode_name, button_list=None):
        try:
            await self.bot.send_photo(self.chat_id, qrcode_name, caption=send_text,
                                      reply_markup=button_list, parse_mode=ParseMode.HTML)
            log.info("这里创建订单后，需要10分钟后删除消息！")
        except Exception as e:
            log.info(e)

    async def delete_msg(self, chat_id, message_id):
        await self.bot.delete_messages(chat_id, message_id)

    async def answer(self, callback_query_id, send_text):
        try:
            await self.bot.answer_callback_query(callback_query_id, show_alert=True, text=send_text)
        except Exception as e:
            log.info(e)

    async def returnLastByCallBackQuery(self, send_text, button_list: Optional[Union[InlineKeyboardMarkup, None]],
                                        param):
        await self.bot.edit_message_text(chat_id=self.chat_id,
                                         message_id=self.msg_id,
                                         text=send_text,
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=common.getButtonList(button_list, param),
                                         disable_web_page_preview=True)

    async def returnLastByThisMsg(self, send_text, button_list: Optional[Union[InlineKeyboardMarkup, None]], param):
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=send_text, parse_mode=ParseMode.HTML,
            reply_markup=common.getButtonList(button_list, param),
            disable_web_page_preview=True)

    async def returnLastByCallBackQueryByEntities(self, send_text,
                                                  button_list: Optional[Union[InlineKeyboardMarkup, None]],
                                                  param, entities):
        await self.bot.edit_message_text(chat_id=self.chat_id,
                                         message_id=self.msg_id,
                                         text=send_text,
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=common.getButtonList(button_list, param),
                                         disable_web_page_preview=True,
                                         entities=entities)

    async def editByMsgId(self, send_text, msg_id, button_list, param):
        """
        专用于指定消息id的修改（多用于回复后修改）
        @param send_text: 文本
        @param msg_id: 消息id self.buttonReplyMsgId
        @param button_list: 按钮
        @param param: 返回的指定场景
        @return:
        """
        await self.bot.edit_message_text(chat_id=int(self.chat_id),
                                         message_id=int(msg_id),
                                         text=send_text,
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=common.getButtonList(button_list, param),
                                         disable_web_page_preview=True,
                                         )
