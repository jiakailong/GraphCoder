import os
from langchain_community.agent_toolkits.file_management import FileManagementToolkit
from langchain_community.tools import ShellTool

file_tools = FileManagementToolkit(root_dir=os.getenv("WORKSPACE_ROOT", ".")).get_tools()
shell_tools = ShellTool()