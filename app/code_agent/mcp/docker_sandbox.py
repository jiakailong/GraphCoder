import subprocess
import os
import shlex

def run_in_docker(command: str, image: str = "ubuntu:latest") -> str:
    """Run a shell command inside a Docker container for isolation."""
    workspace = os.getenv("WORKSPACE_ROOT", os.getcwd())
    
    # Use docker run with automatic removal, volume mount, and dropping privileges if needed.
    # For now, just mount the workspace.
    cmd_template = [
        "docker", "run", "--rm",
        "-v", f"{workspace}:/workspace",
        "-w", "/workspace",
        image,
        "bash", "-c", command
    ]
    
    try:
        res = subprocess.run(cmd_template, capture_output=True, text=True)
        if res.returncode != 0:
            return f"Error ({res.returncode}):\n{res.stderr}"
        return res.stdout
    except Exception as e:
        return f"Docker execution failed: {str(e)}"
