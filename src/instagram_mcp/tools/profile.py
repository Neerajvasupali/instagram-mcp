"""Profile, authentication check, and account management tools for Instagram."""

import json
from typing import Optional
from mcp.server.mcpserver import MCPServer
from instagram_mcp.client import InstagramClient


def register_profile_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_validate_token",
        description="Verify that the configured Instagram/Meta access token is valid and unexpired.",
    )
    async def validate_token() -> str:
        try:
            res = await client.get("me", {"fields": "id,name"}, require_account_id=False)
            return json.dumps(
                {
                    "valid": True,
                    "account_id": client.account_id or "Not configured in .env",
                    "meta_user": res,
                    "message": "Access token is valid and active.",
                },
                indent=2,
            )
        except Exception as e:
            return json.dumps(
                {
                    "valid": False,
                    "error": str(e),
                    "message": "Access token validation failed. Please refresh your token in .env.",
                },
                indent=2,
            )

    @server.tool(
        name="instagram_list_connected_accounts",
        description=(
            "List Facebook Pages and connected Instagram Business/Creator accounts associated with the access token. "
            "Use this to find your numeric INSTAGRAM_ACCOUNT_ID when setting up your .env configuration."
        ),
    )
    async def list_connected_accounts() -> str:
        fields = "id,name,instagram_business_account{id,username,name}"
        res = await client.get("me/accounts", {"fields": fields}, require_account_id=False)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_profile",
        description="Get Instagram account metadata including username, name, biography, follower count, follows count, media count, website, and profile picture URL.",
    )
    async def get_profile(account_id: Optional[str] = None) -> str:
        target_id = account_id or client.account_id
        fields = "id,username,name,biography,profile_picture_url,website,followers_count,follows_count,media_count"
        res = await client.get(target_id, {"fields": fields})
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_publishing_quota",
        description="Check current 24-hour content publishing limit and usage for the connected Instagram account.",
    )
    async def get_publishing_quota() -> str:
        fields = "config,quota_usage"
        res = await client.get(f"{client.account_id}/content_publishing_limit", {"fields": fields})
        return json.dumps(res, indent=2)
