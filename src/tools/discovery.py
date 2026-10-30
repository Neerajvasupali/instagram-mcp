"""Competitor research and business discovery tools for Instagram."""

import json
from mcp.server.mcpserver import MCPServer
from src.client import InstagramClient


def register_discovery_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_discover_business",
        description="Lookup public metadata, follower counts, and recent posts from other Instagram Business or Creator accounts for competitor intelligence.",
    )
    async def discover_business(target_username: str, media_limit: int = 10) -> str:
        # Sanitize username
        clean_username = target_username.lstrip("@").strip()
        if not clean_username:
            raise ValueError("target_username cannot be empty.")
        limit = min(max(media_limit, 1), 25)
        fields = (
            f"business_discovery.username({clean_username})"
            f"{{username,name,biography,website,followers_count,follows_count,media_count,profile_picture_url,"
            f"media.limit({limit}){{id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count}}}}"
        )
        res = await client.get(client.account_id, params={"fields": fields})
        return json.dumps(res, indent=2)
