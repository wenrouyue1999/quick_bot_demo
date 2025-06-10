#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/27 下午4:37
# @Author  : wenrouyue
# @File    : base_mode.py
# @Description :

from import_utils import *
from sqlalchemy.ext.declarative import declarative_base

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

    @classmethod
    def paginate(
            cls,
            page: int = 1,
            page_size: int = 10,
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[Any] = None,
            desc_order: bool = True
    ) -> Dict[str, Any]:
        """
        通用分页查询方法（挂在 BaseModel 上）
        :param page: 当前页码
        :param page_size: 每页条数
        :param filters: 过滤条件 dict，例如 {"is_delete": "0"}
        :param order_by: 排序字段，例如 cls.create_time
        :param desc_order: 是否降序排列
        :return: 包含分页数据和总数的字典
        """
        dbm = DatabaseManager()
        session = dbm.session
        filters = filters or {}

        query = session.query(cls).filter_by(**filters)

        total = query.count()

        if order_by is not None:
            query = query.order_by(desc(order_by) if desc_order else order_by)

        items = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
