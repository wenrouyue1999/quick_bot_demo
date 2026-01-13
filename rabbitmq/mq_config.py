
class RabbitMQConfig:
    # 交换机名称
    EXCHANGE_NAME = "pikpak.payment.exchange"
    
    # 队列配置
    class Queues:
        PAYMENT_CALLBACK_QUEUE = "pikpak.payment.callback"
        # 可以在此添加更多队列
        # ORDER_TIMEOUT_QUEUE = "pikpak.order.timeout"

    # Routing Keys
    class RoutingKeys:
        PAYMENT_CALLBACK_KEY = "payment.callback"
        
    # 连接配置 (从 config_dev.yaml 读取，这里仅作为 Key 引用)
