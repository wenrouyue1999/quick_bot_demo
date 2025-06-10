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
