from langchain_mcp_adapters.client import MultiServerMCPClient
import os

async def create_mcp_stdio_client(name, params):
    # Ensure subprocess inherits the current environment (including PYTHONPATH)
    env = os.environ.copy()
    if "env" in params:
        env.update(params["env"])
    params["env"] = env

    config = {
        name: {
            "transport": "stdio",
            **params,
        }
    }

    client = MultiServerMCPClient(config)

    tools = await client.get_tools()

    return client, tools