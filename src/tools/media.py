"""Media retrieval and post inspection tools for Instagram."""

import json
from typing import Optional
from mcp.server.mcpserver import MCPServer
from src.client import InstagramClient


def register_media_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_get_recent_media",
        description="Retrieve a paginated list of published posts, Reels, and videos from the connected Instagram account. Supports after_cursor for pagination.",
    )
    async def get_recent_media(
        limit: int = 10,
        after_cursor: Optional[str] = None,
    ) -> str:
        fields = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,like_count,comments_count"
        params = {"fields": fields, "limit": min(max(limit, 1), 50)}
        if after_cursor:
            params["after"] = after_cursor

        res = await client.get(f"{client.account_id}/media", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_media_details",
        description="Get detailed metadata for a specific media item (post, Reel, or video) by its Instagram media ID.",
    )
    async def get_media_details(media_id: str) -> str:
        fields = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,like_count,comments_count,is_comment_enabled,is_shared_to_feed"
        res = await client.get(media_id, params={"fields": fields})
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_carousel_children",
        description="Retrieve individual child media items (photos/videos) that belong to a Carousel album.",
    )
    async def get_carousel_children(media_id: str) -> str:
        fields = "id,media_type,media_url,permalink,timestamp"
        res = await client.get(f"{media_id}/children", params={"fields": fields})
        return json.dumps(res, indent=2)
