import aio_pika
import asyncio
from import_utils import log
from config.config import load_config


class RabbitMQClient:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RabbitMQClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 确保只初始化一次
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.connection = None
        self.channel = None
        self._config = load_config().get("rabbitmq", {})
        self._initialized = True

    @property
    def config(self):
        return self._config

    async def connect(self):
        """建立连接 (Robust Connection)"""
        async with self._lock:
            if self.connection and not self.connection.is_closed:
                return self.connection

            try:
                host = self.config.get("host", "127.0.0.1")
                port = self.config.get("port", 5672)
                user = self.config.get("username", "guest")
                pwd = self.config.get("password", "guest")
                vhost = self.config.get("virtual_host", "/")

                self.connection = await aio_pika.connect_robust(
                    host=host,
                    port=port,
                    login=user,
                    password=pwd,
                    virtualhost=vhost
                )
                self.channel = await self.connection.channel()
                log.info(f"✅ RabbitMQ 连接成功: {host}:{port}")
                return self.connection
            except Exception as e:
                log.error(f"❌ RabbitMQ 连接失败: {e}")
                raise

    async def get_channel(self):
        if self.connection is None or self.connection.is_closed:
            await self.connect()
        # 确保 channel 可用 (aio_pika connection is robust, channel might need re-acquire?)
        # connect_robust handles reconnection, but channel might need checking.
        if self.channel is None or self.channel.is_closed:
            self.channel = await self.connection.channel()
        return self.channel

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            log.info("RabbitMQ 连接已关闭")
