#!/bin/bash

# 项目目录
PROJECT_DIR="/www/wwwroot/GroupSendBot"
# 虚拟环境路径
VENV_DIR="$PROJECT_DIR/.venv"
# 主程序文件
MAIN_FILE="$PROJECT_DIR/main.py"

# 检查项目目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
  echo "错误：项目目录 $PROJECT_DIR 不存在"
  exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "$VENV_DIR" ]; then
  echo "错误：虚拟环境 $VENV_DIR 不存在，请先运行 uv sync 或 uv venv"
  exit 1
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 检查 main.py 是否存在
if [ ! -f "$MAIN_FILE" ]; then
  echo "错误：主程序文件 $MAIN_FILE 不存在"
  exit 1
fi

# 启动项目
nohup uv run python "$MAIN_FILE" >/dev/null 2>&1 &
echo "项目已后台启动！"