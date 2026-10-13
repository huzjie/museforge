"""Optional integrations (LangChain, MCP). Each degrades gracefully."""
from . import langchain, mcp

__all__ = ["langchain", "mcp"]
