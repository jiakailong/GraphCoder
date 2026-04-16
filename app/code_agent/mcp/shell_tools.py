import subprocess
import shlex
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field
from app.code_agent.mcp.docker_sandbox import run_in_docker

mcp = FastMCP()

@mcp.tool(name="run_shell", description="Run a shell command inside an isolated Docker sandbox")
def run_shell_command(command:
    Annotated[str, Field(description="shell command will be executed inside Docker container", examples="ls -al")]) -> str:
    try:
        # Pass command directly to Docker container
        return run_in_docker(command, image="python:3.12-slim")
    except Exception as e:
        return str(e)

def run_shell_command_by_popen(commands):
    # Backward compatibility, or optionally modify if used
    p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = p.communicate()
    if stdout:
        return stdout
    return stderr

if __name__ == "__main__":
    mcp.run(transport="stdio")
