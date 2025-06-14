#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/16 下午1:21
# @Author  : wenrouyue
# @File    : toujia_user_bot.py
from import_utils import *


class ToujiaUserBot(BaseModel):
    __tablename__ = 'toujia_user_bot'  # 表名
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(String(100), primary_key=True, default=lambda: str(uuid.uuid4()).replace("-", "").upper())
    tg_id = Column(String(100), nullable=False, comment='Telegram ID')
    name = Column(String(100), nullable=True, comment='用户名字')
    user_name = Column(String(100), nullable=True, comment='用户用户名')
    bot_token = Column(String(200), nullable=True, comment='机器人token')
    bot_name = Column(String(200), nullable=True, comment='机器人的名字')
    bot_start_name = Column(String(200), nullable=True, comment='机器人启动时的名字')
    bot_username = Column(String(200), nullable=True, comment='机器人用户名')
    bot_flag = Column(String(100), nullable=True, comment='机器人启动状态 0未启动 1启动')

    def __init__(self, tg_id, name, user_name, bot_token=None, bot_name=None, bot_start_name=None, bot_username=None,
                 bot_flag=None, **kw: Any):
        super().__init__(**kw)
        self.tg_id = tg_id
        self.name = name
        self.user_name = user_name
        self.bot_token = bot_token
        self.bot_name = bot_name
        self.bot_start_name = bot_start_name
        self.bot_username = bot_username
        self.bot_flag = bot_flag

    def __repr__(self):
        return (f"<ToujiaUserBot(tg_id='{self.tg_id}', name='{self.name}', user_name='{self.user_name}', "
                f"bot_token='{self.bot_token}', bot_name='{self.bot_name}', bot_flag='{self.bot_flag}', "
                f"bot_start_name='{self.bot_start_name}' ,bot_username='{self.bot_username}' , "
                f"update_time='{self.update_time}', create_time='{self.create_time}')>")

    def queryBotByToken(self):
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserBot).filter_by(tg_id=self.tg_id, bot_token=self.bot_token,
                                                          is_delete="0").first()

    @staticmethod
    def initialize():
        dbm = DatabaseManager()
        return dbm.execute_sql(
            """SELECT tm.* FROM toujia_user_bot tm JOIN toujia_user tu ON tm.tg_id = tu.tg_id WHERE tu.vip_level > :vip_level AND tu.vip_validity_time > NOW() and tm.is_delete = :is_delete """,
            {'vip_level': 0, 'is_delete': "0"})

    @staticmethod
    def initializeFather():
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserBot).filter_by(tg_id="father", is_delete="0").all()
