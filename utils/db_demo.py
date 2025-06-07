#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 下午11:21
# @Author  : wenrouyue
# @File    : db_demo.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接
DATABASE_URI = 'mysql+pymysql://username:password@localhost:3306/databasename?charset=utf8mb4'
engine = create_engine(DATABASE_URI, echo=True)

Base = declarative_base()


# 定义 User 模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"


# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 增
    new_user = User(name='Alice', age=30)
    session.add(new_user)
    session.commit()

    # 查
    users = session.query(User).all()
    for user in users:
        print(user)

    # 改
    alice = session.query(User).filter_by(name='Alice').first()
    if alice:
        alice.age = 31
        session.commit()

    # 删
    if alice:
        session.delete(alice)
        session.commit()
except Exception as e:
    session.rollback()  # 回滚事务
    print(f"发生了异常: {e}")
finally:
    session.close()  # 关闭会话
