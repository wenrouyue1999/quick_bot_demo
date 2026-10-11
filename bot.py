#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午6:39
# @Author  : wenrouyue
# @File    : bot.py
import time
from urllib.parse import urlencode

from pyrogram.enums import ChatMemberStatus
from pyrogram.types.user_and_chats import chat_member_updated
from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler, ChatMemberUpdatedHandler

from mode.tg_user import TgUser
from mode.user_bot import UserBot
from service.chat_member_updated_service import ChatMemberUpdatedService
from import_utils import *


async def is_rate_limited(user_id):
    # Redis Key 设计

    cache_key = f"rate_limit:{user_id}"
    # 通过 Redis 的 INCR 命令递增请求计数
    current_count = redisUtils.incr(cache_key)
    if current_count == 1:
        # 如果是第一次请求，设置过期时间
        redisUtils.expire(cache_key, RATE_LIMIT_WINDOW)
    if current_count > RATE_LIMIT_COUNT:
        log.info(f"用户 {user_id} 超过了速率限制.")
        return False
    if current_count > 10:
        log.info(f"用户 {user_id} 已发出 {current_count} 次请求.")
    return True


# Constants
RATE_LIMIT_COUNT = config["cache"]["RATE_LIMIT_COUNT"]
RATE_LIMIT_WINDOW = config["cache"]["RATE_LIMIT_WINDOW"]
cache = {}
bots = {}
childs = {}


async def channel_message(bot: Client, message: Message):
    log.info(f"频道消息：{message.chat.id} - {message.id} - {message.text or '非文本'}")


class FatherBot:
    def __init__(self, name=None, api_id=None, api_hash=None, token=None):
        from bot_router.router import Router, Input, Query, ReplyInput
        self.token = token
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.router = Router()
        self.Input = Input()
        self.ReplyInput = ReplyInput()
        self.query = Query()
        self.config = load_config()
        if self.config["environment"] == "dev":
            log.info("开发环境，代理启动机器人")
            proxy = {
                "scheme": "socks5",
                "hostname": "127.0.0.1",
                "port": 10808
            }
            self.bot = Client(name=self.name,
                              api_id=self.api_id,
                              api_hash=self.api_hash,
                              bot_token=self.token,
                              proxy=proxy)
            self.add_handler(self.bot)
        else:
            log.info("服务器环境，无需代理启动机器人")
            self.bot = Client(name=self.name,
                              api_id=self.api_id,
                              api_hash=self.api_hash,
                              bot_token=self.token)
            self.add_handler(self.bot)
        # bots[self.bot.bot_token] = self.bot

    async def start(self):
        """ 创建并启动父机器人 """
        try:
            # 启动父机器人
            await self.bot.start()
            bots[self.bot.bot_token] = self
            commands = [
                BotCommand(command="start", description="启动机器人")
            ]
            # 父机器人启动成功
            log.info(f"父机器人 {self.bot.bot_token} 启动成功！")
            log.info(f"机器人队列有：{len(bots)} 个 {bots}")
            await self.bot.set_bot_commands(commands)
            return self.bot
        except Exception as e:
            log.error(f"启动父机器人 {self.bot.bot_token} 失败: {e}")
            return None

    def add_handler(self, bot: Client):
        # 监听私聊中 /start 和 /help 指令；
        bot.add_handler(MessageHandler(self.commod, filters.command(["start", "help"]) & filters.private))
        # 处理所有按钮点击事件（即 callback_data）
        bot.add_handler(CallbackQueryHandler(callback=self.callback_query))
        # 用户回复机器人消息
        bot.add_handler(MessageHandler(filters=filters.private & filters.reply, callback=self.reply_message_private))
        # 私聊中发送普通消息（非指令、非回复）
        bot.add_handler(MessageHandler(filters=filters.private, callback=self.message_private))
        # 处理机器人加入/退出群组/频道的通知
        bot.add_handler(ChatMemberUpdatedHandler(callback=self.chat_member_update))
        # 监听 bot 所在频道的所有新消息
        bot.add_handler(MessageHandler(filters=filters.channel | filters.group, callback=channel_message))

    @staticmethod
    def chat_member_update(bot: Client, updated: chat_member_updated):
        # 检查更新的成员是否是你的机器人
        # log.info(updated)
        new_chat_member = updated.new_chat_member
        chat = updated.chat
        # chat_service = ChatMemberUpdatedService(bot, updated)
        # 保证 new_chat_member 不为 None
        if new_chat_member is not None and new_chat_member.user.is_bot:
            new_status = new_chat_member.status
            log.info(new_status)
            if new_status == ChatMemberStatus.ADMINISTRATOR:
                # chat_service.joinMember()
                # chat_service.updateAdmin()
                log.info(f"机器人具有管理员权限 🎉 : {chat.title} (ID: {chat.id})")
            elif new_status == ChatMemberStatus.MEMBER:
                log.info(f"机器人已被作为成员加入: {chat.title} (ID: {chat.id})")
                # chat_service.joinMember()
                # chat_service.unUpdateAdmin()
                log.info("机器人没有管理员权限 🚫")
            # 处理被禁用的情况
            elif new_status == ChatMemberStatus.BANNED:
                log.info(f"机器人被禁止进入群组: {chat.title} (ID: {chat.id})")
                # chat_service.removeMember()

        elif new_chat_member is None:
            # 处理机器人被移除的情况
            # chat_service.removeMember()
            log.info(f"机器人已被移除群组: {chat.title} (ID: {chat.id})")

        # 提取关键信息
        chat_title = getattr(updated.chat, 'title', '') or ''
        chat_username = f"@{updated.chat.username}" if getattr(updated.chat, 'username', None) else ""
        from_u = getattr(updated, 'from_user', None)
        f_name = getattr(from_u, 'first_name', '') or ''
        l_name = getattr(from_u, 'last_name', '') or ''
        u_name = f"@{from_u.username}" if getattr(from_u, 'username', None) else ''
        user_name = f"{f_name} {l_name} {u_name}".strip()
        user_id = getattr(from_u, 'id', 0)
        date = getattr(updated, 'date', None)
        # 判断加入或退出
        try:
            action = "加入" if (updated.new_chat_member and
                                updated.new_chat_member.status.value == "member"
                                or updated.new_chat_member.status.value == "administrator") else "退出"
        except Exception as e:
            action = "移除"
            log.info(e)
        # 打印日志
        log.info(f"{date} 用户 {user_name} (ID: {user_id}) {action} {chat_type} {chat_title} {chat_username}")

    async def reply_message_private(self, bot: Client, msg: Message):
        flag = await self.checkUser(msg.from_user.id)
        log.info("reply_message_private 接收消息了（用户回复机器人消息）")
        # log.info(msg)
        if flag and msg.reply_to_message:
            if msg.text is not None:
                await self.ReplyInput.replyInput(bot, msg)
            if msg.photo is not None:
                await self.ReplyInput.replyInput(bot, msg)
            if msg.media is not None:
                await self.ReplyInput.replyInput(bot, msg)

    async def message_private(self, bot: Client, msg: Message):
        log.info("message_private 接收消息了")
        if "child" in bot.name:
            db_bot = UserBot(tg_id=msg.from_user.id, name=self.name, user_name=msg.from_user.username,
                             bot_token=self.bot.bot_token).queryBotByToken()
            if not db_bot:
                text = "此机器人为会员独享机器人，您无法使用哦！"
                button_list = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🤖 公共机器人", url="https://t.me/cuilon_bot"),
                     InlineKeyboardButton(text="🤖 创建同款", url="https://t.me/cuilon_bot")],
                    [InlineKeyboardButton(text="🥱 聊天交友", url="https://t.me/cuilon_bot"),
                     InlineKeyboardButton(text="👩‍💻 联系客服", url="https://t.me/cuilon_bot"), ],
                ])
                await self.bot.send_message(msg.chat.id, text, reply_markup=button_list)
                return
        flag = await self.checkUser(msg.from_user.id)
        if flag and msg.text:
            if len(msg.text.split(" ")) == 2:
                msg.text = msg.text.split(" ")[1]
            if msg.text.startswith("https://"):
                # 校验用户发送的是否为公开链接
                lst = common.checkTgLink(msg.text)
                if len(lst) != 0:
                    # 用户发送的链接有效
                    msg.text = "转发消息\n" + msg.text
                else:
                    if msg.text.startswith("https://t.me/c"):
                        log.info(f'用户：{msg.from_user.id} 发送消息：{msg.text} ，私密链接')
                        msg.text = "转发消息\n" + msg.text
                    else:
                        log.info(f'用户：{msg.from_user.id} 发送消息：{msg.text} ，链接无效，直接返回')
                    # await self.bot.send_message(msg.from_user.id, f"{msg.text}\n\n不是Telegram的消息链接！")
                    # return
            await self.Input.input(bot, msg)

    async def callback_query(self, bot: Client, call_back: CallbackQuery):
        if call_back.inline_message_id:
            flag = await self.checkUser(call_back.from_user.id)
            flag and await self.query.callback(call_back.data, bot, call_back)
        else:
            skip = False
            if (call_back.data == '会员解封'
                    or '支付' in call_back.data
                    or '订单' in call_back.data):
                skip = True
            flag = await self.checkUser(call_back.message.chat.id, skip=skip)
            flag and await self.router.route(call_back.data, bot, call_back, "call_back")

    async def commod(self, bot: Client, msg: Message):
        flag = await self.checkUser(msg.from_user.id)
        if not flag:
            return
            # 原始 message.text 可能是 "/start a_6465491111"
        parts = msg.text.split(maxsplit=1)
        command = parts[0]
        params = parts[1] if len(parts) > 1 else ""
        if params:
            query_params = urlencode({"param": params})
            formatted_msg = f"{command}?{query_params}"
        else:
            formatted_msg = f"{command}"
        user_id = msg.from_user.id
        name = common.getName(msg.chat.first_name, msg.chat.last_name)
        user_name = "https://t.me/" + msg.chat.username
        log.info(f"用户user_id：{user_id}，name:{name} ，user_name: https://t.me/{user_name}")
        TgUser(user_id, name, user_name).init_user()
        await self.router.route(formatted_msg, bot, msg, "msg")

    async def checkUser(self, userId, **args):
        is_ban = self.user_is_ban(userId)
        if is_ban:
            if await is_rate_limited(userId):
                return True
            else:
                await self.bot.send_message(userId, "操作频率太快了！请等待1分钟")
                return False
        else:
            if args.get("skip"):
                return True
            await self.bot.send_message(userId, text="您已经被拉黑，如有疑问联系管理员！",
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text="💠 会员点我直接解封",
                                                                  callback_data="会员解封")]]))
            return False

    @staticmethod
    def user_is_ban(userId):
        # bot_id = common.botGetId(self.bot)
        res = redisUtils.sismember(config["redisKey"]["userBlank"], userId)
        if res == 1:
            log.info(f"{userId}, is banned")
            return False
        return True


class ChildBot(FatherBot):
    def __init__(self, name=None, api_id=None, api_hash=None, token=None):
        super().__init__(name, api_id, api_hash, token)

    # 子机器人的创建函数
    async def start(self, **args):
        """ 创建并启动子机器人 """
        try:
            # 启动子机器人
            await self.bot.start()
            childs[self.bot.bot_token] = self
            # 子机器人启动成功
            log.info(f"子机器人 {self.bot.bot_token} 启动成功！")
            log.info(f"子机器人对象有：{len(childs)} 个 {childs}")
            commands = [
                BotCommand(command="start", description="启动机器人")
            ]
            await self.bot.set_bot_commands(commands)
            return self.bot
        except Exception as e:
            log.error(f"启动子机器人 {self.bot.bot_token} 失败: {e}")
            return None

    async def stop(self):
        try:
            log.info(f"开始停止：{self}")
            log.info("移除childs 和 bots 数据")
            childs.pop(self.bot.bot_token, None)
            bots.pop(self.bot.bot_token, None)
            await self.bot.stop()
        except Exception as e:
            log.error(f"启动子机器人 {self.bot.bot_token} 失败: {e}")
            return None
