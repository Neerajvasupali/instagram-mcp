"""Hashtag search and trend research tools for Instagram."""

import json
from typing import Optional
from mcp.server.mcpserver import MCPServer
from src.client import InstagramClient


def register_hashtag_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_search_hashtag",
        description="Search for an Instagram hashtag to retrieve its unique Meta hashtag ID (required for querying hashtag media).",
    )
    async def search_hashtag(hashtag: str) -> str:
        clean_tag = hashtag.lstrip("#").strip()
        if not clean_tag:
            raise ValueError("Hashtag query cannot be empty.")
        params = {"user_id": client.account_id, "q": clean_tag}
        res = await client.get("ig_hashtag_search", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_hashtag_top_media",
        description="Retrieve top/trending public media associated with a specific hashtag ID. Supports after_cursor for pagination.",
    )
    async def get_hashtag_top_media(
        hashtag_id: str,
        limit: int = 10,
        after_cursor: Optional[str] = None,
    ) -> str:
        fields = "id,caption,media_type,permalink,like_count,comments_count,timestamp"
        params = {
            "user_id": client.account_id,
            "fields": fields,
            "limit": min(max(limit, 1), 50),
        }
        if after_cursor:
            params["after"] = after_cursor

        res = await client.get(f"{hashtag_id}/top_media", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_hashtag_recent_media",
        description="Retrieve most recently published public media associated with a specific hashtag ID. Supports after_cursor for pagination.",
    )
    async def get_hashtag_recent_media(
        hashtag_id: str,
        limit: int = 10,
        after_cursor: Optional[str] = None,
    ) -> str:
        fields = "id,caption,media_type,permalink,like_count,comments_count,timestamp"
        params = {
            "user_id": client.account_id,
            "fields": fields,
            "limit": min(max(limit, 1), 50),
        }
        if after_cursor:
            params["after"] = after_cursor

        res = await client.get(f"{hashtag_id}/recent_media", params=params)
        return json.dumps(res, indent=2)
