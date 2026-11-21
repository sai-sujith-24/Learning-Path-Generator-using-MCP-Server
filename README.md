# AI Learning Path Generator using MCP

A Streamlit app that uses LangChain/LangGraph, Gemini, and Composio MCP tools to build a learning path, research YouTube learning videos, and request a Google Drive document or Notion page plus a playlist.

## Requirements
- Python 3.10+
- Google Gemini API key
- Composio account and MCP consumer key
- Connected YouTube and Google Drive or Notion integration in Composio

## Quick start
```bash
git clone https://github.com/sai-sujith-24/Learning-Path-Generator-using-MCP-Server.git
cd Learning-Path-Generator-using-MCP-Server
python -m venv .venv
pip install -r requirements.txt
```

Create a local `.env` using `.env.example` as a template. Never commit live API keys.

```bash
streamlit run app.py
```

Open the Streamlit address shown in your terminal (usually http://localhost:8501). Enter a Gemini API key, your learning goal, and a Google Drive/Notion destination. Confirm integration authorizations separately in Composio.

## Configuration
- `COMPOSIO_CONSUMER_API_KEY`: secret Composio consumer key.
- `COMPOSIO_MCP_URL`: MCP endpoint for your Composio session. Replace the example URL with the one your account supplies.
- `GEMINI_MODEL`: Gemini model ID (defaults to `gemini-2.5-flash`; check availability for your account).

Use `python test_composio.py` to verify which tools are available. `generate_mcp.py` demonstrates creating a session; it never prints authentication headers.

## Files
- `app.py`: Streamlit frontend
- `utils.py`: agent and MCP client
- `prompt.py`: agent instructions
- `generate_mcp.py`: MCP session example
- `test_composio.py`: connection tester

## Limitations and safety
Creating playlists/documents requires live authorized services, permissions, and tool schemas. Tools may fail independently; inspect actual outputs and do not assume success. The model may select unsuitable results; review generated links and content. For public deployment, add per-user authorization, safe error handling, connection cleanup, rate limits and automated integration tests.
