#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2025/6/8 下午6:29
# @Author  : wenrouyue
# @File    : long_str.py

"""
<blockquote><b>默认渠道，计算扣除费率后收益</b></blockquote>
<pre><b>默认渠道，计算扣除费率后收益</b></pre>
"""


class LongStr:
    @staticmethod
    def page_str(page):
        """
        基础分页
        Returns: 默认返回大小10条

        """
        return f"""?page={page}&page_size=10"""
