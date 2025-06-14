#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/27 下午4:37
# @Author  : wenrouyue
# @File    : base_mode.py
# @Description :

from import_utils import *

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    is_delete = Column(String(10), default="0", nullable=True)
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
        调用实例：
        def adPaginate(self, page: int = 1, page_size: int = 10):
            return self.paginate(
                page=page,
                page_size=page_size,
                filters={"is_delete": "0"},
                order_by=Advertisement.create_time,
                desc_order=True
            )
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

    @classmethod
    def rawPaginate(
            cls,
            base_sql: str,
            page: int = 1,
            page_size: int = 10,
            filters: Optional[dict] = None,
            model_class: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        原生 SQL 分页查询通用方法
        @param base_sql: 原始 SQL（不含 LIMIT 和 OFFSET）
        @param page: 当前页码
        @param page_size: 每页大小
        @param filters: 绑定参数
        @param model_class: 绑定实体类可为Dto
        :return: dict 包含 total, items, page, page_size
        调用实例：
        def adPaginateBySql(self, page: int = 1, page_size: int = 10):
            return self.rawPaginate(""
            SELECT
           t1.id,t1.tg_id,t1.ad_name,t1.caption,t1.media,t1.button,t1.entity,t1.is_delete,t1.update_time,t1.create_time
           FROM advertisement t1
           left join advertisement_task_gx t2 on t1.id = t2.ad_id and t2.is_delete = '0'
           WHERE t1.is_delete = '0' and t2.task_id = :task_id
           ORDER BY t1.create_time DESC
            "", page=page, page_size=page_size, {"task_id":"123123"},model_class=Advertisement)
        """
        dbm = DatabaseManager()
        session = dbm.session
        filters = filters or {}
        model_class = model_class or cls

        # 查询总数
        count_sql = f"SELECT COUNT(1) FROM ({base_sql}) AS total_sub"
        total = session.execute(text(count_sql), filters).scalar()

        # 加入分页
        paginated_sql = base_sql + " LIMIT :limit OFFSET :offset"
        filters.update({
            "limit": page_size,
            "offset": (page - 1) * page_size
        })

        result = session.execute(text(paginated_sql), filters).mappings().all()
        # 映射为类实例（构造函数接收字典）
        items = [model_class(**dict(row)) for row in result]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
