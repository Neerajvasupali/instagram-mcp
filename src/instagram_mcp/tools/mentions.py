"""Mentions and tagged media tools for Instagram."""

import json
from typing import Optional
from mcp.server.mcpserver import MCPServer
from instagram_mcp.client import InstagramClient


def register_mentions_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_get_tagged_media",
        description=(
            "Retrieve media items in which the connected Instagram account was visually tagged "
            "(photo/video user-tagging) by other users. NOTE: This retrieves user-tagged posts, "
            "not text caption @mentions. Supports after_cursor for pagination."
        ),
    )
    async def get_tagged_media(
        limit: int = 10,
        after_cursor: Optional[str] = None,
    ) -> str:
        fields = "id,caption,media_type,permalink,timestamp,like_count,comments_count"
        params = {"fields": fields, "limit": min(limit, 25)}
        if after_cursor:
            params["after"] = after_cursor

        res = await client.get(f"{client.account_id}/tags", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_mentioned_comment",
        description=(
            "Lookup details of a specific comment where your Instagram account was @mentioned. "
            "Returns the comment text, username of author, timestamp, like count, and media ID."
        ),
    )
    async def get_mentioned_comment(comment_id: str) -> str:
        clean_id = comment_id.strip()
        fields = f"mentioned_comment.comment_id({clean_id}){{id,text,timestamp,like_count,username,media{{id,media_url}}}}"
        res = await client.get(client.account_id, params={"fields": fields})
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_mentioned_media",
        description=(
            "Lookup details of a media post (photo, reel, video) where your Instagram account was @mentioned in the caption. "
            "Returns caption, media_type, permalink, timestamp, and engagement counts."
        ),
    )
    async def get_mentioned_media(media_id: str) -> str:
        clean_id = media_id.strip()
        fields = f"mentioned_media.media_id({clean_id}){{id,caption,media_type,media_url,permalink,timestamp,comments_count,like_count}}"
        res = await client.get(client.account_id, params={"fields": fields})
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_reply_to_mention",
        description=(
            "Post a reply comment when your account has been @mentioned in a comment. "
            "Requires media_id (the post containing the comment), comment_id (the specific comment with the @mention), and message."
        ),
    )
    async def reply_to_mention(media_id: str, comment_id: str, message: str) -> str:
        data = {
            "media_id": media_id.strip(),
            "comment_id": comment_id.strip(),
            "message": message,
        }
        res = await client.post(f"{client.account_id}/mentions", data=data)
        return json.dumps(
            {"success": True, "comment_id": res.get("id"), "message": "Mention reply posted"},
            indent=2,
        )
