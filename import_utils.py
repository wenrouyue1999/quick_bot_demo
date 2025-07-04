#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 下午6:50
# @Author  : wenrouyue
# @File    : import_utils.py
from config.config import load_config
from config.long_str import LongStr
import os
import aiofiles
import re
import json
import asyncio
import time
import uuid

from log.logger import init_logger
from utils.mysql_utils import DatabaseManager
from utils.redis_utils import RedisUtil
from utils import common
from typing import Optional, Union, Dict, Any
from pyrogram.types import *
from pyrogram import Client
from pyrogram.enums import *
from pyrogram import types
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from mode.base_mode import BaseModel
from utils.mysql_utils import DatabaseManager
from config.redis_keys import RedisKeys
from urllib.parse import urlencode

log = init_logger()
config = load_config()
redisUtils = RedisUtil(config["redis"]["host"], config["redis"]["port"], config["redis"]["password"],
                       config["redis"]["db"])
redisUtilsByTask = RedisUtil(config["redis"]["host"], config["redis"]["port"], config["redis"]["password"],
                             config["redis"]["taskDb"])
db = DatabaseManager()
