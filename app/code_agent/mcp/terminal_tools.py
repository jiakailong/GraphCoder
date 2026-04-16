import subprocess
from typing import Annotated, List
import os

from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP()

DOCKER_CONTAINER_NAME = "code_agent_persistent_terminal"

def _ensure_container_running():
    res = subprocess.run(["docker", "ps", "-q", "-f", f"name={DOCKER_CONTAINER_NAME}"], capture_output=True, text=True)
    if not res.stdout.strip():
        workspace = os.getenv("WORKSPACE_ROOT", os.getcwd())
        # Start a background container that stays alive
        subprocess.run([
            "docker", "run", "-d", "--rm", "--name", DOCKER_CONTAINER_NAME,
            "-v", f"{workspace}:/workspace", "-w", "/workspace",
            "python:3.12-slim", "tail", "-f", "/dev/null"
        ])

@mcp.tool(name="open_terminal", description="打开或重置后台沙盒终端")
def open_new_terminal(window_id: Annotated[str, Field(description="可选的窗口ID", examples="12345")] = "") -> str:
    _ensure_container_running()
    return f"安全的沙盒终端已启动，容器名称: {DOCKER_CONTAINER_NAME}"

@mcp.tool(name="run_terminal_script", description="在沙盒终端中运行脚本命令")
def run_script_in_terminal(script: Annotated[str, Field(description="在终端中执行的脚本命令", examples="ls -al")]) -> str:
    _ensure_container_running()
    res = subprocess.run(["docker", "exec", DOCKER_CONTAINER_NAME, "bash", "-c", script], capture_output=True, text=True)
    if res.returncode != 0:
        return f"执行失败: \n{res.stderr}"
    return res.stdout

@mcp.tool(name="close_terminal", description="关闭沙盒终端")
def close_terminal_if_open() -> str:
    subprocess.run(["docker", "stop", DOCKER_CONTAINER_NAME], capture_output=True)
    return "沙盒终端已成功关闭"

if __name__ == '__main__':
    mcp.run(transport="stdio")
