#!/bin/bash

# 项目目录
PROJECT_DIR="/www/wwwroot/GroupSendBot"
# 主程序文件
MAIN_FILE="$PROJECT_DIR/main.py"

# 查询相关进程并打印
echo "当前运行的进程："
ps aux | grep -E "[u]v run python $MAIN_FILE|[p]ython3? $MAIN_FILE" | grep -v grep || echo "无相关进程"

# 查找进程 ID
PIDS=$(ps aux | grep -E "[u]v run python $MAIN_FILE|[p]ython3? $MAIN_FILE" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
  echo "没有找到运行中的 $MAIN_FILE 进程"
  exit 0
fi

# 终止进程
for PID in $PIDS; do
  kill -9 "$PID"
  echo "已终止进程 PID: $PID"
done

echo "项目已停止！"