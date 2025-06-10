#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:13
# @Author  : wenrouyue
# @File    : router.py
from urllib.parse import urlparse, parse_qs

from bot_router.callback import Callback
from bot_router.reply import Reply
from import_utils import *
from utils import common


class Router:
    def __init__(self):
        self.routes = {}
        call_backs = Callback().get_callbacks()
        for callback in call_backs:
            self.addRoute(callback[0], callback[1], callback[2])

    def addRoute(self, path_pattern, handler_class, handler_function):
        self.routes[path_pattern] = (handler_class, handler_function)

    async def route(self, path_pattern, bot: Optional[Client], msg, msg_type):
        if msg_type == "msg":
            chat_id = msg.chat.id
            user_id = msg.from_user.id
            name = common.getName(msg.from_user.first_name, msg.from_user.last_name)
            user_name = msg.from_user.username
            log.info(f'非按钮回调，用户：{user_id} 触发path：{path_pattern}')
            if 'child' not in bot.name:
                path_pattern = '' + path_pattern
        else:
            chat_id = msg.message.chat.id
            user_id = msg.from_user.id
            name = common.getName(msg.message.chat.first_name, msg.message.chat.last_name)
            user_name = msg.message.chat.username
            log.info(f'用户：{chat_id} 点击按钮回调：{path_pattern}')
        # 父机器人于子机器人权限判断
        if 'child' in bot.name:
            path_pattern = "c|" + path_pattern
        else:
            path_pattern = "f|" + path_pattern
        parsed_url = urlparse(path_pattern)

        query = {key: values[0] for key, values in parse_qs(parsed_url.query).items()}
        path = parsed_url.path
        route_info = self.routes.get(path)

        bot_data = {
            'bot': bot,
            'chat_id': chat_id,
            'user_id': user_id,
            'name': name,
            'user_name': user_name,
        }

        if route_info:
            handler_class, handler_function = route_info
            handler = handler_class(bot_data, msg)
            await handler_function(handler, query)
        else:
            log.info(f'未匹配路径 {path}')


class ReplyInput:
    def __init__(self):
        self.routes = {}
        reply_list = Reply().get_reply()
        for reply in reply_list:
            self.addInput(reply[0], reply[1], reply[2])

    def addInput(self, path_pattern, handler_class, handler_function):
        self.routes[path_pattern] = (handler_class, handler_function)

    async def replyInput(self, bot, msg):
        url = msg.reply_to_message.text.split("\n")
        reply_text = msg.text
        reply_msg_id = msg.reply_to_message_id
        chat_id = msg.chat.id
        user_id = msg.from_user.id
        button_reply_msg_id = str(url[-1]).split("：")[-1]
        log.info(f'用户：{user_id} 回复消息：{url[0]}')
        # 父机器人于子机器人权限判断
        if 'child' in bot.name:
            url[0] = "c|" + url[0]
        else:
            url[0] = "f|" + url[0]
        route_info = self.routes.get(url[0])

        bot_data = {
            'bot': bot,
            'chat_id': chat_id,
            'user_id': user_id,
            'reply_text': reply_text,
            'reply_to_text': msg.reply_to_message.text,
            'reply_msg_id': reply_msg_id,
            'button_reply_msg_id': button_reply_msg_id
        }

        if "编辑" in url[0]:
            bot_data['mode'] = "edit"

        if route_info:
            handler_class, handler_function = route_info
            handler = handler_class(bot_data, msg)
            await handler_function(handler)
        else:
            log.info(f'未匹配路径 回复 {url[0]}')


class Input:
    def __init__(self):
        self.routes = {}
        # reply_list = Reply().get_reply()
        # for reply in reply_list:
        #     self.add_input(reply[0], reply[1], reply[2])
        call_backs = Callback().get_callbacks()
        for callback in call_backs:
            self.addInput(callback[0], callback[1], callback[2])

    def addInput(self, path_pattern, handler_class, handler_function):
        self.routes[path_pattern] = (handler_class, handler_function)

    async def input(self, bot, msg):
        url = msg.text.split("\n")
        chat_id = msg.chat.id
        user_id = msg.from_user.id
        name = common.getName(msg.from_user.first_name, msg.from_user.last_name)
        user_name = msg.from_user.username

        log.info(f'用户：{user_id} 发送消息：{url[0]}')
        # 父机器人于子机器人权限判断
        if 'child' in bot.name:
            url[0] = "c|" + url[0]
        else:
            url[0] = "f|" + url[0]
        route_info = self.routes.get(url[0])

        bot_data = {
            'bot': bot,
            'chat_id': chat_id,
            'user_id': user_id,
            'name': name,
            'user_name': user_name,
        }

        if route_info:
            handler_class, handler_function = route_info
            handler = handler_class(bot_data, msg)
            await handler_function(handler, url[0])
        else:
            log.info(f'未匹配路径 回复 {url[0]}')


class Query:
    def __init__(self):
        pass

    async def query(self, bot, query):
        split = query.data.split("_")
        if split[0] == "b":
            # 处理相关逻辑，可以实现具体处理
            pass

    async def callback(self, data, bot, query):
        parsed_url = urlparse(data)
        path = parsed_url.path
        route_info = Router().routes.get(path)

        bot_data = {
            "bot": bot,
            path: path
        }

        if route_info:
            handler_class, handler_function = route_info
            handler = handler_class(bot_data, query)
            await handler_function(handler, query)
            # await getattr(handler, handler_function)(bot, query)
        else:
            log.info(f'未匹配路径 {path}')
