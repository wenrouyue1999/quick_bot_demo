#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:45
# @Author  : wenrouyue
# @File    : reply.py
from page.child.child_page import ChildPage
from page.father.father_page import FatherPage


class Reply:
    def __init__(self):
        self.reply = [
            ["f|回复机器人TOKEN", FatherPage, FatherPage.handleBotToken],
            ["c|回复机器人TOKEN", ChildPage, ChildPage.handleBotToken]
        ]

    def get_reply(self):
        return self.reply
