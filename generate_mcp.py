
import os
from dotenv import load_dotenv
from composio import Composio

load_dotenv()

composio = Composio()

session = composio.sessions.create(
    user_id="learning_path_user",
    toolkits=["youtube"],
    mcp=True
)

print("YOUTUBE MCP URL:")
print(session.mcp.url)

print("MCP connection configured. Connection headers are intentionally hidden.")
