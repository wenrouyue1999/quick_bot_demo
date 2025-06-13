#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:13
# @Author  : wenrouyue
# @File    : callback.py

from page.father.father_page import FatherPage
from page.child.child_page import ChildPage


class Callback:
    def __init__(self):
        self.call_basks = [
            ["f|/start", FatherPage, FatherPage.botStart],
            ["f|回复", FatherPage, FatherPage.botInput],
            ["f|父机器人下一级", FatherPage, FatherPage.botNext],
            ["f|返回", FatherPage, FatherPage.returnLast],
            ["f|通用关闭", FatherPage, FatherPage.closeMessage],
            ["f|分页异常", FatherPage, FatherPage.pageError],
            ["c|/start", ChildPage, ChildPage.botStart],
            ["c|回复", ChildPage, ChildPage.botInput],
            ["c|子机器人下一级", ChildPage, ChildPage.botNext],
            ["c|返回", FatherPage, FatherPage.returnLast],
        ]

    def get_callbacks(self):
        return self.call_basks
