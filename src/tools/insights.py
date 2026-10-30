"""Analytics and performance metrics tools for Instagram."""

import json
from typing import Optional
from mcp.server.mcpserver import MCPServer
from src.client import InstagramClient


def register_insights_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_get_account_insights",
        description=(
            "Retrieve account-level analytics (reach, views, follower_count, accounts_engaged, total_interactions). "
            "Periods: 'day', 'week', 'days_28'. Note: 'views' metric automatically sets metric_type to 'total_value'."
        ),
    )
    async def get_account_insights(
        metric: str = "reach,total_interactions",
        period: str = "day",
        metric_type: Optional[str] = None,
        breakdown: Optional[str] = None,
    ) -> str:
        params = {"metric": metric, "period": period}
        if metric_type:
            params["metric_type"] = metric_type
        elif "views" in metric:
            params["metric_type"] = "total_value"
        if breakdown:
            params["breakdown"] = breakdown

        res = await client.get(f"{client.account_id}/insights", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_media_insights",
        description=(
            "Retrieve detailed engagement and reach metrics for a specific post, Reel, or Story. "
            "Uses v22.0-aligned metric names (views replaces impressions, total_interactions replaces engagement)."
        ),
    )
    async def get_media_insights(
        media_id: str,
        media_type: str = "IMAGE",  # IMAGE, VIDEO, REELS, STORIES, CAROUSEL_ALBUM
    ) -> str:
        media_type_upper = media_type.upper()

        # v22.0 metric sets per media type (impressions/plays/engagement deprecated April 2025)
        if media_type_upper == "REELS":
            metrics = "views,reach,total_interactions,likes,comments,saved,shares,ig_reels_avg_watch_time,ig_reels_video_view_total_time"
        elif media_type_upper == "STORIES":
            # Stories: views replaces impressions; exits→exit, taps_forward→tap_forward, taps_back→tap_back
            metrics = "views,reach,replies,shares,tap_forward,tap_back"
        elif media_type_upper in ("CAROUSEL_ALBUM", "IMAGE", "VIDEO"):
            # Standard photo, video, or carousel — unified v22 metrics
            metrics = "views,reach,saved,likes,comments,shares,total_interactions"
        else:
            metrics = "views,reach,saved,total_interactions"

        params = {"metric": metrics}
        res = await client.get(f"{media_id}/insights", params=params)
        return json.dumps(res, indent=2)

    @server.tool(
        name="instagram_get_audience_demographics",
        description=(
            "Retrieve follower demographic breakdowns using the Meta Graph API v18+ follower_demographics metric. "
            "Optional breakdown parameter: 'country', 'city', 'age', or 'gender'. If omitted, fetches all 4 breakdowns. "
            "Note: Requires at least 100 followers on the account."
        ),
    )
    async def get_audience_demographics(breakdown: Optional[str] = None) -> str:
        breakdowns = [breakdown] if breakdown else ["country", "city", "age", "gender"]
        results = {}

        for b in breakdowns:
            clean_b = b.lower().strip()
            params = {
                "metric": "follower_demographics",
                "period": "lifetime",
                "metric_type": "total_value",
                "breakdown": clean_b,
            }
            try:
                data = await client.get(f"{client.account_id}/insights", params=params)
                results[clean_b] = data
            except Exception as e:
                results[clean_b] = {"error": str(e)}

        return json.dumps(results, indent=2)

    @server.tool(
        name="instagram_get_online_followers",
        description="Retrieve follower activity by hour of day (online followers). Period is strictly 'day'. Note: Requires at least 100 followers.",
    )
    async def get_online_followers() -> str:
        params = {"metric": "online_followers", "period": "day"}
        res = await client.get(f"{client.account_id}/insights", params=params)
        return json.dumps(res, indent=2)
