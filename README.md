# Telegram Bot 快速开发框架

本项目用于快速开发 **Telegram Bot**，内置了机器人交互的基础能力，支持灵活扩展，适用于多种业务场景。

---

## 📦 功能介绍

- 修改 `config_dev.yaml` 配置文件即可快速接入
- 执行 `ddl.sql` 初始化数据库表结构
- 根据 `ToujiaUserBot` 中的 `initialize()` 方法中的 SQL，初始化子机器人数据
- 本框架已构建以下基础功能：
  ```
  - `/start` 命令处理
  - 消息回复
  - 多级菜单（下一级）逻辑封装
  - 通用返回操作支持
  - 机器人在群组 / 频道中管理员权限变动检测
  - 定时任务支持
  - 支持通用分页
  ```

---

## 🚀 快速开始

```
1. 修改配置文件：
   vi config_dev.yaml
2. 初始化数据库结构：
   mysql -u root -p < ddl.sql
3. 初始化子机器人数据：
   根据 ToujiaUserBot 中的 initialize() 方法中的 SQL，执行相关语句初始化。
4. 启动主程序：
   python main.py
```

---

## 注意事项
- 开发环境已使用代理

- ```text
    proxy = {
    "scheme": "socks5",
    "hostname": "127.0.0.1",
    "port": 10808
    }
    ```
