# quick_bot_demo快速开发框架规范（给 Codex / AI）

你在这个仓库内开发时，必须遵守以下规则。

## 1. 回复语言
- 始终使用中文。

## 2. 目标与风格
- 这是一个快速开发 Telegram Bot 的技术框架。
- 新功能优先复用现有基础设施，不要重复造轮子。
- 保持“小步快改、可运行、可维护”的风格。

## 3. 统一导入与基类约定
- 新页面文件优先使用：
  - `from import_utils import *`
  - `from page.base_page import BasePage`
  - `from utils.bot_message import BotMessage`
  - ```
    class XxxxrPage(BasePage):

    def __init__(self, botData, callbackQuery):
        super().__init__(botData, callbackQuery)
        self.getBotMessage()
    async def xxxx(self, url):
        if url:
            log.info(f"DemoPage xxxx 参数: {url}")```
- 页面类优先继承：
  - `BasePage`
- 交互发送优先使用：
  - `self.getBotMessage()`
  - `self.botMessage.send(...) / send_reply(...) / st(...)`

## 4. 回调与路由约定
- callback_data 保持现有风格：`中文动作?key=value&...`
- 有参数时按既有模式解析，不改动整体路由机制。

## 5. 代码复用优先级
- 优先复用：
  - `import_utils.py`
  - `page/base_page.py`
  - `utils/bot_message.py`
  - `utils/common.py`
- 已有能力（分页、删除消息、输入校验、频道链接解析）优先直接调用，不重复实现。

## 6. 日志与异常处理
- 使用 `log.info / log.error` 保持关键路径可追踪。
- 出错优先给出用户可理解提示，不要静默失败。
- 涉及用户输入时，优先走 `check_safe_input` 或同等级白名单校验。

## 7. 数据与配置
- 配置读取沿用 `load_config()`。
- Redis/MySQL 沿用现有封装（`RedisUtil`、`DatabaseManager`）。
- 不随意新增全局单例；如需新增，遵循 `import_utils.py` 现有组织方式。

## 8. 改动原则
- 非必要不重构大面积代码。
- 不破坏已有接口命名和调用方式。
- 新增功能时，同时给出最小可用示例（入口方法 + 按钮 + 回调处理）。

## 9. 输出要求（给 AI）
- 先给可运行方案，再解释原因。
- 涉及多文件改动时，明确每个文件改了什么。
- 如果环境限制导致无法直接写文件，要明确说明并给出完整可复制内容。
