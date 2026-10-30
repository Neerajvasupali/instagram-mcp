"""Tool registration modules for Instagram MCP Server."""

from src.tools.profile import register_profile_tools
from src.tools.publishing import register_publishing_tools
from src.tools.media import register_media_tools
from src.tools.comments import register_comments_tools
from src.tools.insights import register_insights_tools
from src.tools.discovery import register_discovery_tools
from src.tools.hashtags import register_hashtag_tools
from src.tools.mentions import register_mentions_tools

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
