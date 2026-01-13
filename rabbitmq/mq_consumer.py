
import asyncio
import json
import aio_pika
from import_utils import log
from rabbitmq.mq_client import RabbitMQClient
from rabbitmq.mq_config import RabbitMQConfig
from rabbitmq.handlers.payment_handler import PaymentHandler


class RabbitMQConsumer:
    """RabbitMQ 消费者管理类"""

    def __init__(self):
        self.client = RabbitMQClient()

    async def _consume_queue(self, queue_name, routing_key, handler_func):
        """
        监听单个队列的内部方法 (包含 Exchange 声明与绑定)
        """
        try:
            channel = await self.client.get_channel()
            
            # 1. 声明 Exchange
            exchange = await channel.declare_exchange(
                RabbitMQConfig.EXCHANGE_NAME, 
                aio_pika.ExchangeType.TOPIC, 
                durable=True
            )
            
            # 2. 声明 Queue
            queue = await channel.declare_queue(queue_name, durable=True)
            
            # 3. 绑定 Queue 到 Exchange
            await queue.bind(exchange, routing_key=routing_key)
            log.info(f"🔗 队列 [{queue_name}] 已绑定到 Key [{routing_key}]")
            
            log.info(f"🎧 RabbitMQ 监听启动: {queue_name}")
            
            async with queue.iterator() as iterator:
                async for message in iterator:
                    async with message.process():
                        try:
                            body = message.body.decode('utf-8')
                            log.debug(f"MQ收到消息 [{queue_name}]: {body}")
                            
                            data = json.loads(body)
                            await handler_func(data)
                        except Exception as e:
                            log.error(f"MQ 消息处理异常: {e}")
        except Exception as e:
            log.error(f"队列监听异常 [{queue_name}]: {e}")
            # 可以在此添加重连/重启监听逻辑

    async def start(self):
        """启动所有消费者"""
        await self.client.connect()
        
        # 定义队列、Binding Key 与处理器的映射
        consumers = [
            (
                RabbitMQConfig.Queues.PAYMENT_CALLBACK_QUEUE, 
                RabbitMQConfig.RoutingKeys.PAYMENT_CALLBACK_KEY, 
                PaymentHandler.handle
            ),
        ]
        
        loop = asyncio.get_event_loop()
        for queue_name, routing_key, handler in consumers:
            await loop.create_task(self._consume_queue(queue_name, routing_key, handler))
        
        log.info("🚀 RabbitMQ 所有消费者任务已提交")


# 全局入口
consumer_manager = RabbitMQConsumer()


async def start_mq_consumers():
    await consumer_manager.start()
