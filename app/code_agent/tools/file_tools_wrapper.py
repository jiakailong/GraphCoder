import os
from langchain_community.agent_toolkits import FileManagementToolkit
from app.core.config import settings

# 从原本的 app.bailian.common 中抽离，并改用安全的工作区相对路径而非硬编码 Mac 路径
WORKSPACE_ROOT = os.getenv("WORKSPACE_ROOT", settings.WORKSPACE_ROOT)
os.makedirs(WORKSPACE_ROOT, exist_ok=True)

# 默认情况下使用项目根目录作为文件操作沙箱，允许 Agent 跨目录操作
file_toolkit = FileManagementToolkit(root_dir=WORKSPACE_ROOT)
file_tools = file_toolkit.get_tools()
