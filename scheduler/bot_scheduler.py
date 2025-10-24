#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/12/9 下午10:05
# @Author  : wenrouyue
# @File    : bot_scheduler.py
import time
from concurrent.futures import ThreadPoolExecutor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from bot import bots, childs
from import_utils import *
from mode.user_bot import UserBot
from typing import Union, List, Optional
scheduler = AsyncIOScheduler()


def get_time(fun, t):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 取微秒的前3位以获得毫秒
    return f"执行定时 {fun} {t}：{formatted_datetime}"


# 每分钟执行用户定时转发任务
# async def check_task():
#     log.info(get_time("用户定时转发任务", "开始"))
#     db_tasks = ToujiaUserTransferTask.get_task()
#     ids = []
#     if db_tasks:
#         executor = ThreadPoolExecutor(max_workers=10)
#         for task in db_tasks:
#             log.info(f"任务: {task}")
#             ids.append(task.id)
#             executor.submit(run_async_task_in_thread, task)
#         # 调用shutdown，确保不等待任务完成
#         executor.shutdown(wait=False)
#         log.info(f"需要执行的ids：{ids}")
#         # 测试代码 完事打开
#         # if len(ids) > 0:
#         #     # 任务状态 0未执行 1已执行 2执行中
#         #     ToujiaUserTransferTask.update_status_batch(ids, "1")
#     log.info(get_time("用户定时转发任务", "结束"))

# def run_async_task_in_thread(task):
#     log.info(f"异步:{task.id}任务开始执行...")
#     asyncio.run(transfer_message1(task))  # 直接调用新的异步函数
#     log.info(f"异步:{task.id}任务执行完毕")


async def log_scheduler():
    try:
        log.info(f"log_scheduler 定时打印：{time.time()}")
    except Exception as e:
        log.error(f"发送消息失败: {str(e)}")


# @File    : child_task_page.py
async def schedule_jobs():
    log.info("启动定时任务")
    # 启动定时任务
    scheduler.add_job(log_scheduler, 'interval', minutes=1)

    # scheduler.add_job(check_inactivity, 'interval', seconds=600)
    # 启动调度器
    # scheduler.add_job(edit_message, 'interval', seconds=10)
    # scheduler.add_job(test_add, 'interval', seconds=10)

    # scheduler.add_job(check_report, 'interval', seconds=10)
    # scheduler.add_job(check_vip_user, 'interval', seconds=60)

    # for token in bots:
    #     scheduler.add_job(check_inactivity, 'interval', args=[str(token).split(":")[0]], seconds=600)
    scheduler.start()
#

# def check_vip_user():
# log.info(get_time("检测举报用户", "开始"))
# log.info(get_time("检测举报用户", "结束"))

# def edit_message():
#     log.info(get_time("每分钟编辑举报按钮", "开始"))
#     db_bots = ToujiaUserBot(tg_id="1", name="1", user_name="1").initialize_father()
#     father_dict = {}
#     for db_bot in db_bots:
#         # bot: Optional[Client] = db_bot.bot_token
#         # 以bot id 为key token 为value 存入字典
#         db_bot_id = str(db_bot.bot_token).split(":")[0]
#         father_dict[db_bot_id] = db_bot.bot_token
#     queue_len = redisUtils.llen('report:await:edit')
#     # for count in range(queue_len):
#     item = redisUtils.lpop("report:await:edit")
#     # 入队存入的 发送的机器人id，链接
#     redis_bot_id = item.split("_")[0]
#     redis_link = item.split("_")[1]
#     toujiawang_id, toujiawang_msg_id = common.checkTgToujiaLink(redis_link)
#     log.info(toujiawang_id)
#     log.info(toujiawang_msg_id)
#     # 根据token 从bots获取机器人实例
#     bot: Optional[Client] = bots.get(father_dict.get(redis_bot_id))
#     message = bot.get_messages(int(toujiawang_id),int(toujiawang_msg_id))
#         # todo 确认是否本机器人发的能够修改
#     bot.edit_message_caption()
#     log.info(get_time("每分钟编辑举报按钮", '结束'))


# def test_add():
#     log.info(get_time("每分新增例子", "开始"))
#     redisUtils.rpush('report:await:edit', "7120198617_https://t.me/c/2298147455/75")
#     redisUtils.rpush('report:await:edit', "7181252283_https://t.me/c/2298147455/76")
#     redisUtils.rpush('report:await:edit', "8144377512_https://t.me/c/2298147455/82")
#     log.info(get_time("每分新增例子", '结束'))
