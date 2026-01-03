#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2026/01/01
# @Author  : wenrouyue
# @File    : local_api.py
from api.http_utils import HttpUtils
from import_utils import *


class LocalApi:
    """管理所有本地接口调用 (异步)"""

    def __init__(self):
        config_load = load_config()
        """
        # HttpUtils 默认使用 config["request"]["base_url"]
        # 需要其他前缀，创建其他api文件即可
        # self.http = HttpUtils(base_url=config_load["request"]["alist_base_url"])
        # 使用方法 reg_res = await LocalApi().register_alist_user(tg_id, username, password)
        """
        self.http = HttpUtils()
        self.prefix = ""

    async def register_alist_user(self, tg_id, alist_username, alist_password):
        """
        注册Alist用户并绑定关联
        :param tg_id: Telegram ID
        :param alist_username: Alist 用户名
        :param alist_password: Alist 密码
        :return:
        """
        url = "/alist/register"
        json_data = {
            "tgId": str(tg_id),
            "alistUsername": alist_username,
            "alistPassword": alist_password
        }
        return await self.http.post(url, json_data=json_data)

    async def get_alist_user_by_tg_id(self, tg_id):
        """
        根据tg_id 查询alist注册用户
        :param tg_id: Telegram ID
        :return:
        """
        url = "/alist/queryByTgId"
        params = {
            "tgId": str(tg_id)
        }
        return await self.http.get(url, params=params)
