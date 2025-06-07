#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/27 下午4:37
# @Author  : wenrouyue
# @File    : base_mode.py
# @Description :

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from utils.mysql_utils import DatabaseManager

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    update_time = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now(),
                         comment='更新时间')
    create_time = Column(DateTime, nullable=True, default=func.now(), comment='创建时间')

    def update(self):
        dbm = DatabaseManager()
        dbm.update(self)
        return self

    def add(self):
        dbm = DatabaseManager()
        dbm.update(self)
        return self
