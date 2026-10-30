"""Tool registration modules for Instagram MCP Server."""

from instagram_mcp.tools.profile import register_profile_tools
from instagram_mcp.tools.publishing import register_publishing_tools
from instagram_mcp.tools.media import register_media_tools
from instagram_mcp.tools.comments import register_comments_tools
from instagram_mcp.tools.insights import register_insights_tools
from instagram_mcp.tools.discovery import register_discovery_tools
from instagram_mcp.tools.hashtags import register_hashtag_tools
from instagram_mcp.tools.mentions import register_mentions_tools

__all__ = [
    "register_profile_tools",
    "register_publishing_tools",
    "register_media_tools",
    "register_comments_tools",
    "register_insights_tools",
    "register_discovery_tools",
    "register_hashtag_tools",
    "register_mentions_tools",
]
