#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2025/6/8 下午4:34
# @Author  : wenrouyue
# @File    : redis_keys.py
class RedisKeys:
    @staticmethod
    def groupCopyTodo(group_id):
        """
        待办的 copy 的群组 消息ID
        """
        return f"group:copy:todo:{group_id}"

    @staticmethod
    def PayCreateOrder(userId):
        return f"pay:create:order:{userId}"

    @staticmethod
    def MessageAutoDeleteZSet():
        """
        消息自动删除延迟队列 (ZSet)
        Member: token:chat_id:message_id
        Score: expiration_timestamp
        """
        return "message:auto_delete:zset"
