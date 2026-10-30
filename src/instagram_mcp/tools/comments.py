"""Comment management and moderation tools for Instagram."""

import json
from typing import Optional
from mcp.server.mcpserver import MCPServer
from instagram_mcp.client import InstagramClient


def register_comments_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_get_post_comments",
        description="Retrieve top-level comments on a specific post or Reel. Supports cursor-based pagination.",
    )
    async def get_post_comments(
        media_id: str,
        limit: int = 25,
        after_cursor: Optional[str] = None,
    ) -> str:
        fields = "id,text,timestamp,username,like_count,hidden,replies"
        params = {"fields": fields, "limit": min(max(limit, 1), 50)}
        if after_cursor:
            params["after"] = after_cursor

        res = await client.get(f"{media_id}/comments", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_comment_replies",
        description="Retrieve threaded sub-replies under a specific comment ID. Supports cursor-based pagination.",
    )
    async def get_comment_replies(
        comment_id: str,
        limit: int = 25,
        after_cursor: Optional[str] = None,
    ) -> str:
        fields = "id,text,timestamp,username,like_count,hidden"
        params = {"fields": fields, "limit": min(max(limit, 1), 50)}
        if after_cursor:
            params["after"] = after_cursor

        res = await client.get(f"{comment_id}/replies", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_post_comment",
        description="Post a new top-level comment onto an Instagram media post.",
    )
    async def post_comment(media_id: str, message: str) -> str:
        res = await client.post(f"{media_id}/comments", data={"message": message})
        return json.dumps(
            {"success": True, "comment_id": res.get("id"), "message": "Comment posted"},
            indent=2,
        )

    @server.tool(
        name="instagram_reply_to_comment",
        description="Reply directly to a specific comment on an Instagram post.",
    )
    async def reply_to_comment(comment_id: str, message: str) -> str:
        res = await client.post(f"{comment_id}/replies", data={"message": message})
        return json.dumps(
            {"success": True, "reply_id": res.get("id"), "message": "Reply posted"},
            indent=2,
        )

    @server.tool(
        name="instagram_hide_comment",
        description="Hide or unhide a comment on your post (hides comment from public view without deleting).",
    )
    async def hide_comment(comment_id: str, hide: bool = True) -> str:
        res = await client.post(comment_id, data={"hide": "true" if hide else "false"})
        return json.dumps({"success": res.get("success", True), "hidden": hide}, indent=2)

    @server.tool(
        name="instagram_delete_comment",
        description="Permanently delete a comment from your Instagram post.",
    )
    async def delete_comment(comment_id: str) -> str:
        res = await client.delete(comment_id)
        return json.dumps({"success": res.get("success", True), "deleted_id": comment_id}, indent=2)

    @server.tool(
        name="instagram_toggle_comments",
        description="Enable or disable commenting on a specific Instagram media post.",
    )
    async def toggle_comments(media_id: str, enabled: bool) -> str:
        # Per Meta docs, the correct parameter is `comment_enabled` (true/false) on POST /{ig-media-id}
        res = await client.post(
            media_id,
            data={"comment_enabled": "true" if enabled else "false"},
        )
        return json.dumps(
            {"success": res.get("success", True), "comments_enabled": enabled},
            indent=2,
        )
