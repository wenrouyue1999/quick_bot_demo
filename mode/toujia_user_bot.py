#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/16 下午1:21
# @Author  : wenrouyue
# @File    : toujia_user_bot.py
from sqlalchemy import update
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
    is_delete = Column(String(10), default='0', comment='0未删除 1已删除')

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

    def getUserBot(self, flag=None):
        dbm = DatabaseManager()
        db_user = dbm.session.query(ToujiaUserBot).filter_by(tg_id=self.tg_id, is_delete="0").first()
        if db_user:
            log.info(f"用户存在机器人：{self}")
            return db_user
        else:
            if flag is None:
                log.info(f"用户不存在机器人，非启动，无需新增")
            else:
                log.info(f"用户不存在机器人，开始新增：{self}")
                dbm.add(self)
            return None

    def queryBotByid(self):
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserBot).filter_by(tg_id=self.tg_id, bot_username=self.bot_username,
                                                          is_delete="0").first()

    def queryBotByToken(self):
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserBot).filter_by(tg_id=self.tg_id, bot_token=self.bot_token,
                                                          is_delete="0").first()

    def update(self):
        dbm = DatabaseManager()
        dbm.update(self)
        return self

    def checkBotIsOnly(self):
        dbm = DatabaseManager()
        db_user = dbm.session.query(ToujiaUserBot).filter_by(tg_id=self.tg_id, is_delete="0").first()
        if db_user:
            log.info(f"用户存在机器人：{self} 不允许创建多个")
            return db_user
        else:
            log.info(f"用户不存在机器人，{self} 允许创建")
            return None

    @staticmethod
    def update_bot_batch(tg_ids: list):
        dbm = DatabaseManager()
        # 使用 'in_' 来筛选 tg_id
        bots_to_update = dbm.session.query(ToujiaUserBot).filter_by(is_delete="0").filter(
            ToujiaUserBot.tg_id.in_(tg_ids)).all()
        if not bots_to_update:
            log.info("No users found with provided tg_ids.")
            return []
        bots_token = []
        for bot in bots_to_update:
            bots_token.append(bot.bot_token)
        dbm.session.query(ToujiaUserBot).filter(ToujiaUserBot.tg_id.in_(tg_ids)).update({ToujiaUserBot.bot_flag: "0"})
        dbm.session.commit()
        return bots_token

    @staticmethod
    def initialize():
        dbm = DatabaseManager()
        return dbm.execute_sql(
            """SELECT tm.* FROM toujia_user_bot tm JOIN toujia_user tu ON tm.tg_id = tu.tg_id WHERE tu.vip_level > :vip_level AND tu.vip_validity_time > NOW() and tm.is_delete = :is_delete """,
            {'vip_level': 0, 'is_delete': "0"})
        # return dbm.execute_sql(
        #         """SELECT tm.* FROM toujia_user_bot tm JOIN toujia_user tu ON tm.tg_id = tu.tg_id WHERE tu.vip_level > :vip_level AND tu.vip_validity_time > NOW() and tm.is_delete = :is_delete """,
        #         {'vip_level': 0, 'is_delete': "0"}
        # )

    @staticmethod
    def initialize_father():
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserBot).filter_by(tg_id="father", is_delete="0").all()

    @staticmethod
    def get_edit_bot():
        dbm = DatabaseManager()
        return dbm.session.query(ToujiaUserBot).filter_by(tg_id="father", bot_username="edit", is_delete="0").first()
