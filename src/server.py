"""
Instagram Model Context Protocol (MCP) Server.
Exposes Instagram Graph API capabilities as tools for AI agents and LLMs.
"""

from mcp.server.mcpserver import MCPServer
from src.client import InstagramClient
from src.tools import (
    register_profile_tools,
    register_publishing_tools,
    register_media_tools,
    register_comments_tools,
    register_insights_tools,
    register_discovery_tools,
    register_hashtag_tools,
    register_mentions_tools,
)

# Initialize MCP Server
server = MCPServer(
    name="instagram-mcp",
    instructions="This MCP server provides tools to manage, publish, moderate, and analyze Instagram Professional (Creator & Business) accounts via the Meta Graph API.",
)

# Initialize Graph API client
client = InstagramClient()

# Register all tool suites
register_profile_tools(server, client)
register_publishing_tools(server, client)
register_media_tools(server, client)
register_comments_tools(server, client)
register_insights_tools(server, client)
register_discovery_tools(server, client)
register_hashtag_tools(server, client)
register_mentions_tools(server, client)


def main():
    """Run the MCP server over standard I/O (stdio)."""
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
