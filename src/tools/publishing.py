"""Content publishing tools for Instagram."""

import json
from typing import Any, Dict, List, Optional
from mcp.server.mcpserver import MCPServer
from src.client import InstagramClient


def register_publishing_tools(server: MCPServer, client: InstagramClient) -> None:
    @server.tool(
        name="instagram_publish_photo",
        description="Publish a single photo post to the Instagram feed. Note: image_url must be a publicly accessible direct image URL (JPEG format recommended).",
    )
    async def publish_photo(
        image_url: str,
        caption: str = "",
        location_id: Optional[str] = None,
        timeout_seconds: int = 45,
    ) -> str:
        # Step 1: Create photo media container (in POST body)
        data: Dict[str, Any] = {"image_url": image_url}
        if caption:
            data["caption"] = caption
        if location_id:
            data["location_id"] = location_id

        container_res = await client.post(f"{client.account_id}/media", data=data)
        container_id = container_res.get("id")

        # Step 2: Ensure container is ready before publishing (prevents race condition)
        await client.wait_for_container(container_id, timeout_seconds=timeout_seconds)

        # Step 3: Publish media container
        publish_res = await client.post(
            f"{client.account_id}/media_publish",
            data={"creation_id": container_id},
        )
        return json.dumps(
            {
                "success": True,
                "message": "Photo published successfully",
                "container_id": container_id,
                "media_id": publish_res.get("id"),
            },
            indent=2,
        )

    @server.tool(
        name="instagram_publish_reel",
        description="Publish a video Reel to Instagram. Automatically waits for video processing/transcoding before publishing. video_url must be a publicly accessible video URL (MP4/MOV).",
    )
    async def publish_reel(
        video_url: str,
        caption: str = "",
        cover_url: Optional[str] = None,
        share_to_feed: bool = True,
        audio_name: Optional[str] = None,
        timeout_seconds: int = 90,
    ) -> str:
        # Step 1: Create Reels container (in POST body)
        data: Dict[str, Any] = {
            "media_type": "REELS",
            "video_url": video_url,
            "share_to_feed": "true" if share_to_feed else "false",
        }
        if caption:
            data["caption"] = caption
        if cover_url:
            data["cover_url"] = cover_url
        if audio_name:
            data["audio_name"] = audio_name

        container_res = await client.post(f"{client.account_id}/media", data=data)
        container_id = container_res.get("id")

        # Step 2: Poll container until transcoding finishes
        await client.wait_for_container(container_id, timeout_seconds=timeout_seconds)

        # Step 3: Publish container
        publish_res = await client.post(
            f"{client.account_id}/media_publish",
            data={"creation_id": container_id},
        )
        return json.dumps(
            {
                "success": True,
                "message": "Reel published successfully",
                "container_id": container_id,
                "media_id": publish_res.get("id"),
            },
            indent=2,
        )

    @server.tool(
        name="instagram_publish_story",
        description="Publish a Story (photo or video) to Instagram. Ephemeral 24-hour content. media_url must be publicly accessible.",
    )
    async def publish_story(
        media_url: str,
        media_type: str = "IMAGE",  # IMAGE or VIDEO
        timeout_seconds: int = 60,
    ) -> str:
        media_type_upper = media_type.upper()
        data: Dict[str, Any] = {"media_type": "STORIES"}

        if media_type_upper == "VIDEO":
            data["video_url"] = media_url
        else:
            data["image_url"] = media_url

        container_res = await client.post(f"{client.account_id}/media", data=data)
        container_id = container_res.get("id")

        # Always verify container readiness before publish
        await client.wait_for_container(container_id, timeout_seconds=timeout_seconds)

        publish_res = await client.post(
            f"{client.account_id}/media_publish",
            data={"creation_id": container_id},
        )
        return json.dumps(
            {
                "success": True,
                "message": "Story published successfully",
                "container_id": container_id,
                "media_id": publish_res.get("id"),
            },
            indent=2,
        )

    @server.tool(
        name="instagram_publish_carousel",
        description="Publish a Carousel album (multi-photo/video post up to 20 items) to the Instagram feed.",
    )
    async def publish_carousel(
        media_urls: List[str],
        media_types: Optional[List[str]] = None,
        caption: str = "",
        timeout_seconds: int = 120,
    ) -> str:
        if not (2 <= len(media_urls) <= 20):
            raise ValueError("Carousels require between 2 and 20 media items.")

        types = media_types or ["IMAGE"] * len(media_urls)
        if len(types) != len(media_urls):
            raise ValueError("media_types list length must match media_urls length.")

        # Step 1: Create child item containers in POST body
        child_container_ids: List[str] = []
        for url, mtype in zip(media_urls, types):
            is_video = mtype.upper() == "VIDEO"
            sub_data: Dict[str, Any] = {"is_carousel_item": "true"}
            if is_video:
                sub_data["media_type"] = "VIDEO"
                sub_data["video_url"] = url
            else:
                sub_data["image_url"] = url

            child_res = await client.post(f"{client.account_id}/media", data=sub_data)
            cid = child_res.get("id")
            await client.wait_for_container(cid, timeout_seconds=timeout_seconds)
            child_container_ids.append(cid)

        # Step 2: Create parent carousel container with children IDs in POST body
        parent_data: Dict[str, Any] = {
            "media_type": "CAROUSEL",
            "children": ",".join(child_container_ids),
        }
        if caption:
            parent_data["caption"] = caption

        parent_res = await client.post(f"{client.account_id}/media", data=parent_data)
        parent_id = parent_res.get("id")

        await client.wait_for_container(parent_id, timeout_seconds=timeout_seconds)

        # Step 3: Publish carousel
        publish_res = await client.post(
            f"{client.account_id}/media_publish",
            data={"creation_id": parent_id},
        )
        return json.dumps(
            {
                "success": True,
                "message": "Carousel published successfully",
                "container_id": parent_id,
                "media_id": publish_res.get("id"),
                "children": child_container_ids,
            },
            indent=2,
        )

    @server.tool(
        name="instagram_check_container_status",
        description="Check processing/transcoding status of an upload container (IN_PROGRESS, FINISHED, ERROR, EXPIRED).",
    )
    async def check_container_status(container_id: str) -> str:
        res = await client.get(container_id, {"fields": "status_code,status,id"})
        return json.dumps(res, indent=2)
