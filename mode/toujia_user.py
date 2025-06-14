#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 下午5:42
# @Author  : wenrouyue
# @File    : toujia_user.py
from import_utils import *


class ToujiaUser(BaseModel):
    __tablename__ = 'toujia_user'  # 表名
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    tg_id = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=True, comment='tg名字')
    user_name = Column(String(100), nullable=True, comment='tg用户名')
    vip_level = Column(String(100), default='0', comment='vip级别')
    vip_validity_time = Column(DateTime, nullable=True, comment='vip过期时间')
    down_count = Column(Integer, default=0, comment='大文件下载次数')
    is_block = Column(String(10), default='0', comment='0未拉黑 1已拉黑')
    is_copy = Column(String(10), default='0', comment='0不能 1可以')

    def __init__(self, tg_id, name, user_name, vip_level='0', is_block='0', is_copy='0', **kw: Any):
        super().__init__(**kw)
        self.tg_id = tg_id
        self.name = name
        self.user_name = user_name
        self.vip_level = vip_level
        self.is_block = is_block
        self.is_copy = is_copy

    def __repr__(self):
        return (f"<ToujiaUser(tg_id='{self.tg_id}', name='{self.name}', user_name='{self.user_name}', "
                f"vip_level='{self.vip_level}', vip_validity_time='{self.vip_validity_time}', "
                f"is_block='{self.is_block}', is_delete='{self.is_delete}', is_copy='{self.is_copy}', "
                f"update_time='{self.update_time}', create_time='{self.create_time}')>")
