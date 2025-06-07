#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 下午5:22
# @Author  : wenrouyue
# @File    : mysql_utils.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.config import load_config

config = load_config()

class DatabaseManager:
    def __init__(self):
        self.DATABASE_URI = config["database"]["database_uri"]
        self.engine = create_engine(
            self.DATABASE_URI,
            pool_size=100,
            max_overflow=200,  # 设置最大溢出连接数
            pool_timeout=300,  # 设置获取连接的超时时间
            pool_recycle=3600,  # 设置连接的生命周期（1小时）
            echo=True
        )
        self.SessionFactory = sessionmaker(bind=self.engine)
        self.session = self.get_session()

    def get_session(self):
        """ 获取一个新的数据库会话 """
        return self.SessionFactory()

    def __enter__(self):
        self.session = self.get_session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.session.commit()  # 提交会话
        else:
            self.session.rollback()  # 出错时回滚
        self.session.close()  # 关闭会话

    def add(self, obj):
        """ 添加对象到数据库并提交 """
        with self.get_session() as session:
            try:
                session.add(obj)
                session.commit()
                print("对象添加成功！")
                return obj
            except Exception as e:
                session.rollback()
                print(f"添加对象时出错: {e}")

    def update(self, obj):
        """ 更新对象并提交 """
        with self.get_session() as session:
            try:
                session.merge(obj)  # 使用 merge 来更新对象
                session.commit()
                print("对象更新成功！")
            except Exception as e:
                session.rollback()
                print(f"更新对象时出错: {e}")

    def delete(self, obj):
        """ 删除对象并提交 """
        with self.get_session() as session:
            try:
                session.delete(obj)
                session.commit()
                print("对象删除成功！")
            except Exception as e:
                session.rollback()
                print(f"删除对象时出错: {e}")

    def execute_sql(self, sql, params=None):
        """ 执行自定义的 SQL 语句并返回结果 """
        with self.get_session() as session:
            try:
                result = session.execute(text(sql), params or {})
                return result.fetchall()  # 返回所有结果行
            except Exception as e:
                session.rollback()  # 出错时回滚
                print(f"执行 SQL 语句时出错: {e}")

    def execute_stmt(self, stmt):
        """ 执行自定义UPDATE SQL 语句 """
        with self.get_session() as session:
            try:
                session.execute(stmt)
                session.commit()  # 提交更改（如果有）
            except Exception as e:
                session.rollback()  # 出错时回滚
                print(f"执行 SQL 语句时出错: {e}")
