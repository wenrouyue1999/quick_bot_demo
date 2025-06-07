#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/11/17 下午7:45
# @Author  : wenrouyue
# @File    : chat_member_updated_service.py
import copy

from pyrogram.types.user_and_chats import chat_member_updated
from mode.toujia_user_transfer_group import ToujiaUserTransferGroup
from import_utils import *

config_load = load_config()


class ChatMemberUpdatedService:

    def __init__(self, bot: Client, updated: chat_member_updated):
        self.bot = bot
        self.updated = updated
        self.db_group = ToujiaUserTransferGroup(updated.from_user.id, bot.me.id).getByGroupId(updated.chat.id)
        self.group: Optional[ToujiaUserTransferGroup] = None
        self.group_link = None
        self.group_username = None
        self.add_or_update = None

    def process_member_update(self, new_owner: str, privileges: Optional[str] = None, is_delete: Optional[str] = None):
        if self.db_group:
            log.info("存在数据库中，复制对象到group")
            self.group = copy.copy(self.db_group)
        self.group.owner = new_owner
        if privileges is not None:
            self.group.owner_dict = privileges
        if is_delete is not None:
            self.group.is_delete = is_delete
        log.info(self.group)

        if self.add_or_update == "add":
            log.info("群组/频道未记录，准备新增！")
            # self.group.add()
        else:
            # self.group.update()
            log.info("群组/频道已记录，准备修改！")

    def joinMember(self):
        if hasattr(self.updated.chat, 'username') and self.updated.chat.username is not None:
            log.info("公开的频道/群组")
            self.group_link = f"https://t.me/{self.updated.chat.username}"
            self.group_username = self.updated.chat.username
        else:
            log.info("私密的频道/群组")
            self.group_link = f"https://t.me/c/{str(self.updated.chat.id).replace('-100', '')}"
        if self.db_group:
            log.info("存在数据库中，暂不新增，等待权限变更去修改！")
            self.add_or_update = "update"
        else:
            log.info("不存在数据库中，先不新增。等待权限变更去新增！")
            self.add_or_update = "add"
            self.group = ToujiaUserTransferGroup(tg_id=self.updated.from_user.id, bot_id=self.bot.me.id,
                                                 group_id=self.updated.chat.id, group_type=self.updated.chat.type,
                                                 group_link=self.group_link, group_name=self.updated.chat.title,
                                                 group_username=self.group_username)

    def removeMember(self):
        log.info("开始处理移除的逻辑")
        self.process_member_update(new_owner="0", privileges=None, is_delete="1")

    def updateAdmin(self):
        log.info("开始处理管理员权限的逻辑")
        privileges = str(self.updated.new_chat_member.privileges) if hasattr(self.updated.new_chat_member,
                                                                             'privileges') else None
        if self.updated.chat.type == ChatType.CHANNEL:
            log.info("频道需要怼发送消息进行检测！")
            if self.updated.new_chat_member.privileges.can_post_messages and self.updated.new_chat_member.privileges.can_edit_messages:
                log.info("权限正常")
                new_owner = "1"
            else:
                log.info("无法发送消息，new_owner 设置为0")
                new_owner = "0"
        else:
            new_owner = "1"
        self.process_member_update(new_owner=new_owner, privileges=privileges)

    def unUpdateAdmin(self):
        log.info("开始处理删除权限的逻辑")
        privileges = str(self.updated.new_chat_member.privileges) if hasattr(self.updated.new_chat_member,
                                                                             'privileges') else None
        self.process_member_update(new_owner="0", privileges=privileges)
