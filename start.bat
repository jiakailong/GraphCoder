@echo off
setlocal

:: 获取当前批处理脚本所在路径（项目根目录）并切换工作目录
cd /d "%~dp0"

echo 正在启动 Code Agent...
:: 统一设置 PYTHONPATH 至项目目录，方便 MCP 等组件导入包
set "PYTHONPATH=%cd%"

:: 调用底层 agent 入口
python app\code_agent\agent\langgraph_code_agent.py

endlocal
