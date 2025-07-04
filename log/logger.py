#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午5:58
# @Author  : wenrouyue
# @File    : logger.py


import os
import sys

import logbook
from logbook import Logger, TimedRotatingFileHandler


# 禁用 SQLAlchemy 日志（针对 logbook）
def suppress_sqlalchemy_logs():
    sqlalchemy_logger = logbook.Logger('sqlalchemy.engine')
    sqlalchemy_logger.level = logbook.ERROR


# 日志格式
def format_log(record, handler):
    return '{date} {filename}/{func}-{level}-[{lineno}]行：{msg}'.format(
        date=record.time.strftime('%Y-%m-%d %H:%M:%S'),
        level=record.level_name,
        filename=os.path.basename(record.filename),
        lineno=record.lineno,
        func=record.func_name,
        msg=record.message
    )


# 日志目录
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 文件日志处理器
# log_file_handler = TimedRotatingFileHandler(
#     filename=os.path.join(LOG_DIR, 'info.log'),
#     date_format='%Y-%m-%d',
#     encoding='utf-8',
#     bubble=True,
#     level='INFO',
#     backup_count=0  # 不保留多余旧日志
# )

# 文件日志处理器（每分钟滚动）
log_file_handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, 'info.log'),
    date_format='%Y-%m-%d',  # 包含分钟的格式
    encoding='utf-8',
    bubble=True,
    level='INFO',
    backup_count=0,  # 不保留多余旧日志
    rollover_format='{basename}-{timestamp}{ext}',
    timed_filename_for_current=False  # 当前日志文件不带时间戳
)

log_file_handler.formatter = format_log

# 控制台日志处理器
stream_handler = logbook.StreamHandler(stream=sys.stdout, level='INFO', bubble=True)
stream_handler.formatter = format_log


# 初始化 logger
def init_logger(name: str = "script_log") -> Logger:
    logbook.set_datetime_format("local")
    suppress_sqlalchemy_logs()  # 禁用 SQLAlchemy 日志
    logger = Logger(name)
    logger.handlers = []
    logger.handlers.append(log_file_handler)
    logger.handlers.append(stream_handler)
    return logger
