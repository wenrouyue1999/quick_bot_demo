#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午7:40
# @Author  : wenrouyue
# @File    : main.py

from bot import FatherBot, ChildBot
from import_utils import *
from mode.user_bot import UserBot
from scheduler.bot_scheduler import schedule_jobs


async def main():
    config_load = load_config()
    api_id = config_load["key"]["api_id"]
    api_hash = config_load["key"]["api_hash"]
    # todo 无需数据库启动方式 构建UserBot对象
    dbf_bots = [
        # UserBot(tg_id='father', name='father', user_name='', bot_token='', bot_name='', bot_flag='1', bot_start_name='' ,bot_username='' , update_time='2024-11-16 08:41:44', create_time='2024-11-16 08:41:44'),
        UserBot(tg_id='father', name='father',
                user_name='toujiawbot', bot_token='7796416736:AAHcnJTbUThg86aXS17XR7GERDYn3jX5JJA',
                bot_name='偷家王', bot_flag='1', bot_start_name='toujiawbot ', bot_username='@toujiawbot',
                update_time='2024-11-16 08:37:40', create_time='2024-11-16 08:37:40')]
    dbc_bots = []
    tasks = []
    for index, bot in enumerate(dbf_bots):
        log.info(f"父机器人循环：{bot}")
        name = bot.bot_username
        token = bot.bot_token
        if str(bot.id) == '1':
            redisUtils.set("main_bot", bot.bot_start_name)
        tasks.append(FatherBot(name, api_id, api_hash, token))
    # rows = dbc_bots.fetchall()
    if len(dbc_bots) == 0:
        log.info("无子机器人需要启动")
    else:
        for bot in dbc_bots:
            log.info(f"子机器人循环：{bot}")
            tasks.append(ChildBot(f"child_{bot.tg_id}", api_id, api_hash, bot.bot_token))
        log.info(tasks)
    return tasks


async def event():
    log.info("开始挂载程序。。。")
    stop_event = asyncio.Event()
    await stop_event.wait()


async def main_task():
    tasks = await main()
    bot_tasks = [b.start() for b in tasks]
    await asyncio.gather(
        *bot_tasks,
        schedule_jobs(),
        event()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main_task())
    except RuntimeError as e:
        log.error(f"发生错误: {e}")
    except Exception as general_error:
        log.error(f"发生了一个非预期的错误: {general_error}")
