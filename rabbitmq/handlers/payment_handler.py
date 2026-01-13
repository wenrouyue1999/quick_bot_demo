import json
from import_utils import log
from bot import bots
from api.local_api import LocalApi


class PaymentHandler:
    @staticmethod
    async def handle(data: dict):
        """
        处理支付回调业务逻辑
        """
        try:
            status = str(data.get("status"))
            tg_id = data.get("tgId")
            order_no = data.get("orderNo")
            product_name = data.get("productName")
            amount = data.get("amount")

            log.info(f"💰 处理支付回调 - 订单号: {order_no}, 状态: {status}")

            if status == "1":
                await PaymentHandler._process_success(tg_id, order_no, product_name, amount)
            elif status == "2":
                log.info(f"订单 {order_no} 确认已超时取消")
            else:
                log.info(f"订单 {order_no} 状态变更: {status}")

        except Exception as e:
            log.error(f"PaymentHandler 业务处理异常: {e}")

    @staticmethod
    async def _process_success(tg_id, order_no, product_name, amount):
        if not tg_id:
            log.warning("订单缺少 tgId，无法通知用户")
            return

        send_text = (
            f"✅ <b>支付成功！</b>\n\n"
            f"商品：{product_name}\n"
            f"金额：￥{amount}\n"
            f"订单号：<code>{order_no}</code>\n\n"
            f"🎉 感谢您的支持！会员权益已自动生效。\n"
            f"👉 资源提取码及专属链接已发送至下方按钮，请查收。"
        )

        sent = False
        # 遍历 Bot 实例尝试通知
        for token, bot_wrapper in bots.items():
            try:
                if hasattr(bot_wrapper, 'bot'):
                    await bot_wrapper.bot.send_message(
                        chat_id=int(tg_id),
                        text=send_text
                    )
                    log.info(f"Bot Notification Sent to {tg_id}")
                    sent = True
                    break
            except Exception as e:
                pass  # Try next bot

        if not sent:
            log.error(f"⚠️ 无法通知用户 {tg_id} (未找到活跃Bot会话)")
