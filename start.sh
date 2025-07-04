#!/bin/bash

VENV_DIR_BUG=".venv"
PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
SITE_PACKAGES="$VENV_DIR_BUG/lib/python$PYTHON_VERSION/site-packages/pyrogram/utils.py"
MODIFIED_FILE="./pyrogram_bug/utils.py"

# 检查文件和目录
[ ! -d "$VENV_DIR_BUG" ] && { echo "Error: .venv not found"; exit 1; }
[ ! -f "$MODIFIED_FILE" ] && { echo "Error: $MODIFIED_FILE not found"; exit 1; }
[ ! -f "$SITE_PACKAGES" ] && { echo "Error: $SITE_PACKAGES not found"; exit 1; }

# 备份并替换
cp "$SITE_PACKAGES" "$SITE_PACKAGES.bak" && echo "Backed up utils.py"
cp "$MODIFIED_FILE" "$SITE_PACKAGES" && echo "Replaced utils.py"


# 项目目录
PROJECT_DIR="$(pwd)"
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