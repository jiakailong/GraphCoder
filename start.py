#!/usr/bin/env python3
import os
import sys
import asyncio

# 获取当前脚本所在目录（即项目根目录）绝对路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 动态添加 PYTHONPATH，避免手动设置的环境变量遗漏，也确保子进程（MCP Tools等可以正常找到代码库）
sys.path.insert(0, project_root)
os.environ["PYTHONPATH"] = project_root
os.environ["WORKSPACE_ROOT"] = project_root

# 避免导入 Langchain 核心警告
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")

try:
    from app.code_agent.agent.langgraph_code_agent import run_agent
except ImportError as e:
    print(f"导入项目模块失败，请确保您在包含项目的 Python/Conda 虚拟环境中执行该脚本: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("====================================")
    print("🚀 正在启动 Code Agent ...")
    print(f"📂 工作空间: {project_root}")
    print("====================================")
    
    try:
        # 直接运行工作流
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\n用户手动终止，Agent 已安全退出。")
    except Exception as e:
        print(f"\n运行时遇到致命错误: {e}")
        import traceback
        traceback.print_exc()
