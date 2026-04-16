import os
from app.code_agent.utils.mcp import create_mcp_stdio_client

async def get_stdio_powershell_tools():  # Renamed from get_stdio_terminal_tools to match filename
    params = {
        "command": "python",
        "args": [
            os.path.join(os.getenv("WORKSPACE_ROOT", "."), "app/code_agent/mcp/powershell_tools.py")
        ]
    }
    client, tools = await create_mcp_stdio_client("powershell_tools", params)
    return tools
