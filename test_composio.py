
import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

API_KEY = os.getenv("COMPOSIO_CONSUMER_API_KEY", "").strip()
MCP_URL = os.getenv(
    "COMPOSIO_MCP_URL",
    "https://connect.composio.dev/mcp"
).strip()

async def main():
    print("Connecting to Composio...")

    client = MultiServerMCPClient({
        "composio": {
            "transport": "streamable_http",
            "url": MCP_URL,
            "headers": {
                "x-consumer-api-key": API_KEY
            }
        }
    })

    tools = await client.get_tools()

    print("\n========== CONNECTION SUCCESSFUL ==========")
    print("Total tools available:", len(tools))

    print("\n========== AVAILABLE TOOLS ==========")

    for index, tool in enumerate(tools, start=1):
        print(f"{index}. {tool.name}")
        print(f"   Description: {tool.description[:200]}")

    print("\nComposio MCP test completed!")

if __name__ == "__main__":
    asyncio.run(main())
