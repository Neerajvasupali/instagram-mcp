"""
Instagram Graph API Client
Handles authenticated HTTP requests, error parsing, and container status polling.
"""

import asyncio
import os
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables initially
load_dotenv()


class InstagramAPIError(Exception):
    """Raised when the Meta Graph API returns an error response."""

    def __init__(
        self,
        message: str,
        code: Optional[int] = None,
        subcode: Optional[int] = None,
        fbtrace_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.code = code
        self.subcode = subcode
        self.fbtrace_id = fbtrace_id


class InstagramClient:
    """Async client for interacting with the Meta Graph API for Instagram."""

    def __init__(
        self,
        access_token: Optional[str] = None,
        account_id: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        self._explicit_token = access_token
        self._explicit_account_id = account_id
        self._explicit_api_version = api_version

        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
        self.account_id = account_id or os.getenv("INSTAGRAM_ACCOUNT_ID", "").strip()
        self.api_version = api_version or os.getenv("GRAPH_API_VERSION", "v22.0").strip()
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def ensure_configured(self, require_account_id: bool = True) -> None:
        """
        Reload environment variables dynamically to prevent stale tokens
        and verify that required credentials are present.
        """
        load_dotenv(override=True)
        if not self._explicit_token:
            self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
        if not self._explicit_account_id:
            self.account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "").strip()
        if not self._explicit_api_version:
            self.api_version = os.getenv("GRAPH_API_VERSION", "v22.0").strip()
            self.base_url = f"https://graph.facebook.com/{self.api_version}"

        missing = []
        if not self.access_token:
            missing.append("INSTAGRAM_ACCESS_TOKEN")
        if require_account_id and not self.account_id:
            missing.append("INSTAGRAM_ACCOUNT_ID")
        if missing:
            raise ValueError(
                f"Missing required Instagram credentials in .env or environment: {', '.join(missing)}. "
                f"Please populate .env with your {' and '.join(missing)}."
            )

    def _get_auth_headers(self) -> Dict[str, str]:
        """Return Authorization Bearer header to avoid token leakage in query strings."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def _safe_parse_json(self, resp: httpx.Response) -> Dict[str, Any]:
        """Safely parse JSON response from Meta, handling HTML error pages or empty bodies gracefully."""
        try:
            return resp.json()
        except Exception:
            return {
                "error": {
                    "message": f"HTTP {resp.status_code} Non-JSON response from server: {resp.text[:200]}",
                    "code": resp.status_code,
                }
            }

    def _parse_error(self, response_data: Dict[str, Any]) -> str:
        """Extract a readable error message from Meta's response."""
        if "error" in response_data:
            err = response_data["error"]
            msg = err.get("message", "Unknown Meta API error")
            code = err.get("code")
            subcode = err.get("error_subcode")
            fbtrace = err.get("fbtrace_id")
            details = f"Meta API Error ({code}): {msg}"
            if subcode:
                details += f" [Subcode: {subcode}]"
            if fbtrace:
                details += f" (Trace ID: {fbtrace})"
            return details
        return "Unknown error occurred"

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        require_account_id: bool = True,
    ) -> Dict[str, Any]:
        """Perform an authenticated GET request."""
        self.ensure_configured(require_account_id=require_account_id)
        params = params or {}
        # Also include access_token parameter for endpoints where Bearer header isn't parsed
        params.setdefault("access_token", self.access_token)

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_auth_headers()
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            data = self._safe_parse_json(resp)
            if resp.status_code >= 400 or "error" in data:
                err_msg = self._parse_error(data)
                raise InstagramAPIError(err_msg, code=data.get("error", {}).get("code"))
            return data

    async def post(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        require_account_id: bool = True,
    ) -> Dict[str, Any]:
        """
        Perform an authenticated POST request.
        Payload is transmitted in the POST body (data or json_data),
        preventing URL query string errors and token leakage.
        """
        self.ensure_configured(require_account_id=require_account_id)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_auth_headers()

        # If sending form data in body, include access_token in body as well
        if data is not None:
            data = dict(data)
            data.setdefault("access_token", self.access_token)
        elif json_data is not None:
            json_data = dict(json_data)
            json_data.setdefault("access_token", self.access_token)
        else:
            # Fallback if no body provided
            params = params or {}
            params.setdefault("access_token", self.access_token)

        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(
                url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
            )
            data_res = self._safe_parse_json(resp)
            if resp.status_code >= 400 or "error" in data_res:
                err_msg = self._parse_error(data_res)
                raise InstagramAPIError(err_msg, code=data_res.get("error", {}).get("code"))
            return data_res

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        require_account_id: bool = True,
    ) -> Dict[str, Any]:
        """Perform an authenticated DELETE request."""
        self.ensure_configured(require_account_id=require_account_id)
        params = params or {}
        params.setdefault("access_token", self.access_token)

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_auth_headers()
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.delete(url, params=params, headers=headers)
            data = self._safe_parse_json(resp)
            if resp.status_code >= 400 or "error" in data:
                err_msg = self._parse_error(data)
                raise InstagramAPIError(err_msg, code=data.get("error", {}).get("code"))
            return data

    async def wait_for_container(
        self, container_id: str, timeout_seconds: int = 60, poll_interval: int = 3
    ) -> Dict[str, Any]:
        """
        Poll a media container until its status becomes FINISHED or PUBLISHED.
        Raises an error on ERROR or EXPIRED status.
        """
        elapsed = 0
        while elapsed < timeout_seconds:
            res = await self.get(container_id, {"fields": "status_code,status"})
            status_code = res.get("status_code", "").upper()

            if status_code in ("FINISHED", "PUBLISHED"):
                return res
            elif status_code in ("ERROR", "EXPIRED"):
                raise InstagramAPIError(
                    f"Media container {container_id} failed with status: {status_code} ({res.get('status', 'No error detail')})"
                )

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(
            f"Timed out after {timeout_seconds}s waiting for container {container_id} to finish processing."
        )
