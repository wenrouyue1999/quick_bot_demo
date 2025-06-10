#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 下午6:50
# @Author  : wenrouyue
# @File    : import_utils.py

from config.config import load_config
import re
import asyncio
import uuid
from utils.mysql_utils import DatabaseManager
from utils.redis_utils import RedisUtil
from utils import common
from log.logger import LoggerConfig
from typing import Optional, Union, Dict, Any
from pyrogram.types import *
from pyrogram import Client
from pyrogram.enums import ChatType,MessageEntityType
from pyrogram import types
from sqlalchemy import Column, String, DateTime, func, text, update, Integer, Time,desc
from mode.base_mode import BaseModel
from utils.mysql_utils import DatabaseManager
from config.redis_keys import RedisKeys

log = LoggerConfig(__name__).get_logger()
config = load_config()
redisUtils = RedisUtil(config["redis"]["host"], config["redis"]["port"], config["redis"]["password"],
                       config["redis"]["db"])
redisUtilsByTask = RedisUtil(config["redis"]["host"], config["redis"]["port"], config["redis"]["password"],
                             config["redis"]["taskDb"])
db = DatabaseManager()
