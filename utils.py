
import os
import asyncio
from typing import Optional, Callable, Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI

from prompt import user_goal_prompt

load_dotenv()

COMPOSIO_MCP_URL = os.getenv(
    "COMPOSIO_MCP_URL",
    "https://connect.composio.dev/mcp"
).strip()

COMPOSIO_API_KEY = os.getenv(
    "COMPOSIO_CONSUMER_API_KEY",
    ""
).strip()

cfg = RunnableConfig(recursion_limit=100)


def initialize_model(google_api_key: str):
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=google_api_key,
        temperature=0
    )


async def setup_agent_with_tools(
    google_api_key: str,
    progress_callback: Optional[Callable[[str], None]] = None
) -> Any:

    if progress_callback:
        progress_callback("Setting up Composio connection...")

    if not COMPOSIO_API_KEY:
        raise ValueError(
            "COMPOSIO_CONSUMER_API_KEY is missing from your .env file."
        )

    if not COMPOSIO_API_KEY.startswith("ck_"):
        raise ValueError(
            "Invalid Composio consumer key. Expected a key starting with ck_."
        )

    if progress_callback:
        progress_callback("Connecting to Composio MCP...")

    tools_config = {
        "composio": {
            "transport": "streamable_http",
            "url": COMPOSIO_MCP_URL,
            "headers": {
                "x-consumer-api-key": COMPOSIO_API_KEY
            }
        }
    }

    mcp_client = MultiServerMCPClient(tools_config)

    if progress_callback:
        progress_callback("Discovering available Composio tools...")

    tools = await mcp_client.get_tools()

    if not tools:
        raise RuntimeError("No tools were returned by Composio.")

    if progress_callback:
        progress_callback(
            f"Loaded {len(tools)} Composio tools successfully."
        )

    if progress_callback:
        progress_callback("Creating AI agent...")

    model = initialize_model(google_api_key)

    agent = create_react_agent(
        model,
        tools
    )

    if progress_callback:
        progress_callback("Agent setup complete!")

    return agent


def run_agent_sync(
    google_api_key: str,
    user_goal: str = "",
    progress_callback: Optional[Callable[[str], None]] = None
) -> dict:

    async def _run():

        agent = await setup_agent_with_tools(
            google_api_key=google_api_key,
            progress_callback=progress_callback
        )

        learning_path_prompt = (
            "User Goal: " + user_goal + "\n\n"
            + user_goal_prompt
        )

        if progress_callback:
            progress_callback("Generating your learning path...")

        result = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content=learning_path_prompt)
                ]
            },
            config=cfg
        )

        if progress_callback:
            progress_callback("Learning path generation complete!")

        return result

    loop = asyncio.new_event_loop()

    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_run())
    finally:
        loop.close()
