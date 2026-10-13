"""Run the MCP server over stdio (for testing in an MCP client)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from museforge import MuseAgent, Config
from museforge.integrations.mcp import serve


def main():
    agent = MuseAgent(Config())
    serve(agent)


if __name__ == "__main__":
    main()
