#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2025/10/24 下午5:40
# @Author  : wenrouyue
# @File    : tg_user.py

from import_utils import *


class TgUser(BaseModel):
    __tablename__ = 'tg_user'  # 表名
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    tg_id = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=True, comment='tg名字')
    user_name = Column(String(100), nullable=True, comment='tg用户名')

    def __init__(self, tg_id, name, user_name, **kw: Any):
        super().__init__(**kw)
        self.tg_id = tg_id
        self.name = name
        self.user_name = user_name

    def __repr__(self):
        return (f"<TgUser(tg_id='{self.tg_id}', name='{self.name}', user_name='{self.user_name}'"
                f", is_delete='{self.is_delete}', "
                f"update_time='{self.update_time}', create_time='{self.create_time}')>")
