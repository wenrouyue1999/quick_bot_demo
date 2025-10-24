#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/16 下午10:50
# @Author  : wenrouyue
# @File    : user_transfer_group.py

from import_utils import *


class UserTransferGroup(BaseModel):
    __tablename__ = 'user_transfer_group'  # 表名
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(String(100), primary_key=True, default=lambda: str(uuid.uuid4()).replace("-", "").upper())
    tg_id = Column(String(100), nullable=True, comment='Telegram ID')
    bot_id = Column(String(100), nullable=True, comment='Bot ID')
    group_id = Column(String(100), nullable=True, comment='群组id')
    group_type = Column(String(100), nullable=True, comment='1群组 2频道')
    group_link = Column(String(100), nullable=True, comment='群组/频道 链接')
    group_name = Column(String(100), nullable=True, comment='群组/频道 名字')
    group_username = Column(String(100), nullable=True, comment='群组/频道 用户名')
    owner = Column(String(100), nullable=True, comment='0无权限发送 1有权限发送')
    owner_dict = Column(String(100), nullable=True, comment='所有权限字典')

    def __init__(self, tg_id, bot_id, group_id=None, group_type=None,
                 group_link=None, group_name=None, group_username=None,
                 owner=None, owner_dict=None, **kw: Any):
        super().__init__(**kw)
        self.tg_id = tg_id
        self.bot_id = bot_id
        self.group_id = group_id
        self.group_type = group_type
        self.group_link = group_link
        self.group_name = group_name
        self.group_username = group_username
        self.owner = owner
        self.owner_dict = owner_dict

    def __repr__(self):
        return (f"<ToujiaUserTransferGroup(id='{self.id}', tg_id='{self.tg_id}', bot_id='{self.bot_id}', "
                f"group_id='{self.group_id}', group_type='{self.group_type}', group_link='{self.group_link}', "
                f"group_name='{self.group_name}', group_username='{self.group_username}', "
                f"owner='{self.owner}',owner_dict='{self.owner_dict}', is_delete='{self.is_delete}', "
                f"update_time='{self.update_time}', create_time='{self.create_time}')>")

    def getAll(self):
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserTransferGroup).filter_by(tg_id=self.tg_id, bot_id=self.bot_id,
                                                                    is_delete=self.is_delete).all()

    def getByGroupId(self, group_id):
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserTransferGroup).filter_by(tg_id=self.tg_id, bot_id=self.bot_id,
                                                                    group_id=group_id,
                                                                    is_delete=self.is_delete).first()

    def getCanSendChat(self):
        dbm = DatabaseManager()
        return (
            dbm.session.query(ToujiaUserTransferGroup)
            .filter_by(tg_id=self.tg_id, bot_id=self.bot_id, is_delete=self.is_delete, owner="1")
            .order_by(ToujiaUserTransferGroup.update_time.desc())
            .all()
        )
