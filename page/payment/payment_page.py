#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2025/12/7 下午10:52
# @Author  : wenrouyue
# @File    : payment_page.py

from page.base_page import BasePage
from import_utils import *
from api.payment_api import PaymentApi
from api.local_api import LocalApi


class PaymentPage(BasePage):
    def __init__(self, botData, callbackQuery):
        super().__init__(botData, callbackQuery)
        self.getBotMessage()

    PRODUCT_MAP = {
        "vip66": {
            "name": "vip1",
            "price": "66",
            "icon": "👑",
            "desc": "加入私密频道，每日更新，独家资源优先看。\n   防封保险：私密频道更安全，防止失联。"
        },
        "vip199": {
            "name": "vip2",
            "price": "199",
            "icon": "🔥",
            "desc": "<b>包含权益一</b>，额外赠送 <b>10T 全站精品资源包</b>。\n   PikPak转存：一键保存到自己网盘，永久收藏，无需担心失效。"
        }
    }

    async def callBuyResource(self, url):
        """
        购买资源介绍页
        """
        if url:
            log.info(f"callBuyResource 参数：{url}")

        # 动态构建介绍文本
        intro_lines = []
        for code, info in self.PRODUCT_MAP.items():
            intro_lines.append(
                f"{info['icon']} <b>{info['name']} ({info['price']}元/永久)：</b>\n"
                f"   {info['desc']}\n"
            )

        send_text = (
            "💎 <b>玩物视频站VIP会员权益说明</b>\n\n"
            f"{chr(10).join(intro_lines)}\n"
            "💳 <b>支持支付方式：</b> 支付宝、微信\n"
        )

        button_list = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text=f"{info['icon']} 购买{info['name']} (￥{info['price']})",
                callback_data=f"支付选择?p={code}"
            )] for code, info in self.PRODUCT_MAP.items()
        ])

        await self.botMessage.editByMsgId(send_text, self.messageId, button_list, "start")

    async def callPaymentSelect(self, url):
        """
        选择支付方式
        """
        product_code = url.get("p")
        product_info = self.PRODUCT_MAP.get(product_code)

        if not product_info:
            await self.baseMsg.answer("❌ 商品不存在", True)
            return

        name = product_info['name']
        price = product_info['price']
        descs = product_info['desc']

        send_text = (
            f"💰 <b>收银台</b>\n\n"
            f"商品：<b>{name}</b>\n"
            f"包含权益：\n{descs}\n\n"
            f"无需付费，直接点击下方按钮模拟支付成功！\n"
            f"金额：<b>￥{price}</b>\n\n"
            f"请选择支付方式："
        )

        button_list = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="💰 支付宝支付", callback_data=f"模拟支付?p={product_code}&w=alipay")],
            [InlineKeyboardButton(text="💰 微信支付", callback_data=f"模拟支付?p={product_code}&w=wxpay")]
        ])
        await self.botMessage.editByMsgId(send_text, self.messageId, button_list, "buy_resource")

    async def callPaymentCreate(self, url):
        """
        创建支付订单
        """
        # import_utils 已经导入了 redisUtils 和 RedisKeys
        # from utils.redis_utils import RedisUtil
        # from config.redis_keys import RedisKeys
        from api.payment_api import PaymentApi
        from img.qr_code import get_qr_code
        import os

        product_code = url.get("p")
        way = url.get("w")

        # 频率限制
        limit_key = RedisKeys.PayCreateOrder(self.userId)
        if redisUtils.get(limit_key):
            await self.baseMsg.answer("⚠️ 您下单太频繁了，请稍后再试", True)
            return

        product_info = self.PRODUCT_MAP.get(product_code)
        if not product_info:
            await self.baseMsg.answer("❌ 商品不存在", True)
            return

        # 提示正在刷新
        await self.botMessage.editByMsgId("⌛️ 正在创建/刷新订单，请稍候...", self.messageId, None, "buy_resource")

        # 构造订单参数
        import time
        from config.config import load_config

        out_trade_no = f"{int(time.time())}{self.userId}"
        log.info(f"正在创建订单, out_trade_no: {out_trade_no}")

        # 读取支付配置模式
        conf = load_config()
        payment_mode = conf.get('payment', {}).get('mode', 'post')
        payment_version = conf.get('payment', {}).get('version', 'v2')

        try:
            sdk = PaymentApi()
            pay_url = None
            platform_trade_no = None  # 支付平台返回的订单号
            
            # 模式一: POST API 请求 (适用于 V2/V1 API)
            if payment_mode == 'post':
                # 使用 API 发起支付
                res = await sdk.api_pay(
                    name=product_info['name'],
                    money=product_info['price'],
                    pay_type=way,
                    out_trade_no=out_trade_no
                )
                
                # 兼容处理：如果是字符串则解析为JSON (防止 double encoded)
                if isinstance(res, str):
                    try:
                        res = json.loads(res)
                    except Exception as e:
                        log.info(f"json.loads异常:{e}")
                
                # 状态码判断: 从配置中读取期望的成功状态码
                version_conf = conf.get('payment', {}).get(payment_version, {})
                success_code = version_conf.get('success_code', 0)

                log.info(f"当前支付版本: {payment_version}, 期望成功状态码: {success_code}, 实际返回: {res.get('code')}")

                if isinstance(res, dict) and res.get('code') == success_code:
                    pay_url = res.get('pay_info') or res.get('pay_url') or res.get('payurl')
                    platform_trade_no = res.get('trade_no') # 获取平台订单号
                    
                    # 补救措施：如果 JSON 中没有 trade_no，尝试从 pay_url 中提取
                    # 参考 URL: https://baiweipay.com/pay/submit/2026011216503435353/
                    if not platform_trade_no and pay_url:
                        import re
                        match = re.search(r'/pay/submit/(\d+)/?', str(pay_url))
                        if match:
                            platform_trade_no = match.group(1)
                            log.info(f"从URL解析到平台订单号: {platform_trade_no}")
                else:
                    log.error(f"API创建订单失败: {res}")
                    await self.baseMsg.answer("⚠️ 创建订单失败，请稍后再试", True)
                    return
            else:
                # 模式二: URL 拼接 (仅适用于 GET 跳转)
                pay_url = sdk.create_order(
                    name=product_info['name'],
                    money=product_info['price'],
                    pay_type=way,
                    out_trade_no=out_trade_no
                )

            # 设置频率限制 (成功下单后 60秒)
            redisUtils.set_by_time(limit_key, "1", 60)

            # 保存订单到本地数据库 (Java API)
            try:
                from api.local_api import LocalApi
                local_api = LocalApi()
                
                await local_api.create_order(
                    order_no=out_trade_no,
                    pay_order_no=platform_trade_no,
                    user_id=self.userId,
                    product_name=product_info['name'],
                    amount=product_info['price'],
                    payment_method=way,
                    pay_url=pay_url
                )
                log.info(f"订单已保存至本地数据库: {out_trade_no}")
            except Exception as save_err:
                log.error(f"保存订单至本地数据库失败: {save_err}")

            way_name = "支付宝" if way == "alipay" else "微信"
            create_time = time.strftime("%Y-%m-%d %H:%M:%S")

            # 美化 UI
            send_text = (
                f"🌟<b>付款信息</b>🌟\n"
                f"订单号：<code>{out_trade_no}</code>\n"
                f"付款金额：<b>￥{product_info['price']}</b>\n"
                f"付款方式：{way_name}\n"
                f"商品名称：{product_info['name']}\n"
                f"创建时间：{create_time}\n\n"
                f"💠 使用{way_name}扫码或点击立即支付跳转浏览器\n"
                f"💠 付款请不要更改金额备注等信息\n"
                f"💠 支付已设置 10分钟 超时，超时后二维码将自动销毁\n"
            )

            button_list = InlineKeyboardMarkup([
                [InlineKeyboardButton(text=f"💸 立即支付", url=pay_url)],
                [InlineKeyboardButton(text="🔄 无法支付，刷新二维码", callback_data=f"模拟支付?p={product_code}&w={way}")],
                [InlineKeyboardButton(text="✅ 我已支付", callback_data=f"支付查询?t={out_trade_no}")],
            ])

            # --- QR Code 集成 ---
            # 确保目录存在
            if not os.path.exists('./img/order/'):
                os.makedirs('./img/order/')

            # 生成二维码图片路径
            log.info(f"准备生成二维码: pay_url={pay_url}, out_trade_no={out_trade_no}")
            if not pay_url:
                log.error("严重错误: pay_url 为空，无法生成支付信息")
                await self.baseMsg.answer("⚠️ 生成支付链接失败，请重试", True)
                return

            qr_path = get_qr_code(pay_url, way, out_trade_no)
            log.info(f"二维码已生成路径: {qr_path}, 是否存在: {os.path.exists(qr_path)}")

            # 删除旧文本消息
            await self.botMessage.delete_msg(self.chatId, self.messageId)

            # 发送带图片的详情消息
            sent_msg = await self.botMessage.send_order_photo(send_text, qr_path, button_list)

            if sent_msg:
                # 更新当前上下文的消息ID
                self.messageId = sent_msg.id

                # 开启 10分钟 (600秒) 后自动删除任务 (改为 Redis ZSet 持久化方案)
                # Redis Member 格式: token:chat_id:message_id
                delay_seconds = 600
                expire_time = int(time.time()) + delay_seconds
                zset_key = RedisKeys.MessageAutoDeleteZSet()
                # Member 格式: token:chat_id:message_id:trade_no
                member = f"{self.bot.bot_token}:{self.chatId}:{sent_msg.id}:{out_trade_no}"

                redisUtils.zadd(zset_key, {member: expire_time})
                log.info(f"已添加自动删除任务至 Redis: {member}, expire: {expire_time}")

        except Exception as e:
            log.error(f"创建支付订单失败: {e}")
            await self.baseMsg.answer("⚠️ 支付系统繁忙，请稍后再试", True)

    async def callPaymentQuery(self, url):
        """
        查询支付状态
        """
        from api.payment_api import PaymentApi
        trade_no = url.get("t")

        try:
            sdk = PaymentApi()
            # 查单
            res = await sdk.query_order(out_trade_no=trade_no)
            log.info(f"查单结果: {res}")

            if res and res.get('code') == 0 and res.get('status') == 1:
                # 支付成功
                await self.botMessage.delete_msg(self.chatId, self.messageId)
                send_text = (
                    "✅ <b>支付成功！</b>\n\n"
                    "🎉 感谢您的支持！会员权益已生效。\n"
                    "👉 私密频道链接及资源提取码已发送至您的私聊，请查收。\n"
                )
                await self.botMessage.send_message(send_text, self.getDeleteButton())
            else:
                await self.baseMsg.answer("⚠️ 订单未支付或支付处理中，请稍后再试", True)

        except Exception as e:
            log.error(f"查询订单失败: {e}")
            await self.baseMsg.answer("⚠️ 支付查询失败", True)
