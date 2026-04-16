#!/bin/bash

# 获取当前脚本绝对所在目录（即项目根目录）
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 进入根目录
cd "$DIR"

echo "正在启动 Code Agent..."
# 运行时注入项目目录以保证跨操作正常导入
export PYTHONPATH="$DIR"
python app/code_agent/agent/langgraph_code_agent.py
