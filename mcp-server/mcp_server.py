#!/usr/bin/env python3
"""
Intigriti Researcher API MCP Server
Integrated into hrlpavan/ethical-hacking-playbook.

Enables AI assistants (Antigravity, Claude Desktop, Cursor) to interact directly
with the Intigriti bug bounty platform via the official Researcher API v1.0.

Collaborative implementation drawing from:
- jdc94/mcp-intigriti-server
- alpernae/intigriti-mcp
"""

import asyncio
import fnmatch
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urljoin, urlparse

import httpx
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import AnyUrl

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("intigriti-mcp-server")


class IntigritiAPIError(Exception):
    """Custom exception for Intigriti API errors."""
    pass


class IntigritiResearcherAPI:
    """Client for the Intigriti Researcher API v1.0."""

    def __init__(self, base_url: str = "https://api.intigriti.com/external/researcher", api_token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token or os.getenv("INTIGRITI_API_TOKEN")

        if not self.api_token:
            raise ValueError(
                "Intigriti API token is missing. Please set the INTIGRITI_API_TOKEN environment variable."
            )

        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": "EthicalHackingPlaybook-MCP/1.0",
        }

        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request to the Intigriti API with error handling and rate limit tracking."""
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))

        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs,
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "60")
                raise IntigritiAPIError(f"Rate limited by Intigriti API. Retry after {retry_after} seconds.")

            # Handle authentication errors
            if response.status_code == 401:
                raise IntigritiAPIError("Authentication failed (401). Check that your INTIGRITI_API_TOKEN is valid.")

            if response.status_code == 403:
                raise IntigritiAPIError("Forbidden (403). Your account may not have permission to access this endpoint.")

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise IntigritiAPIError(f"API request failed: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Network error: {e}")
            raise IntigritiAPIError(f"Network error: {e}")

    async def get_programs(
        self,
        status_id: Optional[int] = None,
        type_id: Optional[int] = None,
        following: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """List all programs accessible to the researcher."""
        params: Dict[str, Any] = {"limit": min(limit, 500), "offset": offset}
        if status_id is not None:
            params["statusId"] = status_id
        if type_id is not None:
            params["typeId"] = type_id
        if following is not None:
            params["following"] = following

        return await self._make_request("GET", "v1/programs", params=params)

    async def get_program_details(self, program_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific bug bounty program."""
        return await self._make_request("GET", f"v1/programs/{program_id}")

    async def get_program_activities(
        self,
        created_since: Optional[int] = None,
        following: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Retrieve recent program announcements and updates."""
        params: Dict[str, Any] = {"limit": min(limit, 500), "offset": offset}
        if created_since is not None:
            params["createdSince"] = created_since
        if following is not None:
            params["following"] = following

        return await self._make_request("GET", "v1/programs/activities", params=params)

    async def get_program_domains(self, program_id: str, version_id: str) -> Dict[str, Any]:
        """Retrieve domains/assets in scope for a specific program version."""
        return await self._make_request("GET", f"v1/programs/{program_id}/domains/{version_id}")

    async def get_program_rules_of_engagement(self, program_id: str, version_id: str) -> Dict[str, Any]:
        """Retrieve the Rules of Engagement and testing constraints for a program version."""
        return await self._make_request("GET", f"v1/programs/{program_id}/rules-of-engagements/{version_id}")

    async def validate_scope(self, program_id: str, target: str) -> Dict[str, Any]:
        """
        Ethical Pre-flight Check:
        Verifies whether a given hostname/domain is in-scope for the program.
        """
        details = await self.get_program_details(program_id)
        domains_version_id = details.get("domainsVersionId") or details.get("versionId")

        if not domains_version_id:
            return {
                "in_scope": False,
                "reason": "Could not determine domains version ID from program details.",
            }

        domains_data = await self.get_program_domains(program_id, domains_version_id)
        content_items = domains_data.get("content", [])

        # Parse target hostname
        parsed = urlparse(target if "://" in target else f"https://{target}")
        target_host = parsed.hostname or target

        in_scope_matches = []
        out_of_scope_matches = []

        for item in content_items:
            endpoint = item.get("endpoint", "")
            tier = item.get("tier", {}).get("value", "")
            is_in_scope = tier.lower() != "out of scope" and item.get("type", {}).get("value", "").lower() != "out of scope"

            # Check wildcard match (e.g. *.example.com)
            if fnmatch.fnmatch(target_host.lower(), endpoint.lower()) or target_host.lower() == endpoint.lower():
                if is_in_scope:
                    in_scope_matches.append(item)
                else:
                    out_of_scope_matches.append(item)

        if out_of_scope_matches:
            return {
                "target": target_host,
                "in_scope": False,
                "reason": "Target matched an explicit Out-of-Scope rule.",
                "matched_rule": out_of_scope_matches[0],
            }

        if in_scope_matches:
            return {
                "target": target_host,
                "in_scope": True,
                "reason": "Target is explicitly covered by an In-Scope asset.",
                "matched_asset": in_scope_matches[0],
            }

        return {
            "target": target_host,
            "in_scope": False,
            "reason": "Target was not found in the In-Scope assets list. Under ethical guidelines, assume OUT OF SCOPE.",
        }


# Initialize the MCP server
app = Server("intigriti-ethical-playbook")
api_client: Optional[IntigritiResearcherAPI] = None


def get_client() -> IntigritiResearcherAPI:
    global api_client
    if not api_client:
        api_client = IntigritiResearcherAPI()
    return api_client


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """Expose available MCP tools to the AI assistant."""
    return [
        types.Tool(
            name="get_programs",
            description="List all accessible Intigriti bug bounty programs with optional filters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status_id": {"type": "integer", "description": "Filter by program status ID"},
                    "type_id": {"type": "integer", "description": "Filter by program type ID"},
                    "following": {"type": "boolean", "description": "Filter by followed programs"},
                    "limit": {"type": "integer", "description": "Items per page (max 500)", "default": 20},
                    "offset": {"type": "integer", "description": "Pagination offset", "default": 0},
                },
            },
        ),
        types.Tool(
            name="get_program_details",
            description="Get complete metadata, current version IDs, and guidelines for a program.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "string", "description": "Unique GUID identifier of the program"}
                },
                "required": ["program_id"],
            },
        ),
        types.Tool(
            name="get_program_activities",
            description="Get recent activity updates, scope changes, and announcements.",
            inputSchema={
                "type": "object",
                "properties": {
                    "created_since": {"type": "integer", "description": "Unix timestamp filter"},
                    "following": {"type": "boolean", "description": "Filter by followed programs"},
                    "limit": {"type": "integer", "default": 20},
                    "offset": {"type": "integer", "default": 0},
                },
            },
        ),
        types.Tool(
            name="get_program_domains",
            description="Retrieve the exact in-scope assets and domains for a given program version.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "string", "description": "Program GUID"},
                    "version_id": {"type": "string", "description": "Domains version GUID"},
                },
                "required": ["program_id", "version_id"],
            },
        ),
        types.Tool(
            name="get_program_rules_of_engagement",
            description="Retrieve testing rules, custom headers, and safe harbor constraints.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "string", "description": "Program GUID"},
                    "version_id": {"type": "string", "description": "Rules version GUID"},
                },
                "required": ["program_id", "version_id"],
            },
        ),
        types.Tool(
            name="validate_scope",
            description="Ethical Pre-flight: Check whether a specific domain/URL is in-scope before testing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "string", "description": "Program GUID"},
                    "target": {"type": "string", "description": "Domain, hostname, or URL to validate"},
                },
                "required": ["program_id", "target"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[types.TextContent]:
    """Execute tool requests."""
    try:
        client = get_client()

        if name == "get_programs":
            result = await client.get_programs(
                status_id=arguments.get("status_id"),
                type_id=arguments.get("type_id"),
                following=arguments.get("following"),
                limit=arguments.get("limit", 20),
                offset=arguments.get("offset", 0),
            )
        elif name == "get_program_details":
            result = await client.get_program_details(arguments["program_id"])
        elif name == "get_program_activities":
            result = await client.get_program_activities(
                created_since=arguments.get("created_since"),
                following=arguments.get("following"),
                limit=arguments.get("limit", 20),
                offset=arguments.get("offset", 0),
            )
        elif name == "get_program_domains":
            result = await client.get_program_domains(
                program_id=arguments["program_id"], version_id=arguments["version_id"]
            )
        elif name == "get_program_rules_of_engagement":
            result = await client.get_program_rules_of_engagement(
                program_id=arguments["program_id"], version_id=arguments["version_id"]
            )
        elif name == "validate_scope":
            result = await client.validate_scope(
                program_id=arguments["program_id"], target=arguments["target"]
            )
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

        formatted = json.dumps(result, indent=2, ensure_ascii=False)
        return [types.TextContent(type="text", text=formatted)]

    except IntigritiAPIError as e:
        return [types.TextContent(type="text", text=f"Intigriti API Error: {e}")]
    except Exception as e:
        logger.error(f"Error handling tool {name}: {e}")
        return [types.TextContent(type="text", text=f"Execution error: {e}")]


@app.list_resources()
async def list_resources() -> List[types.Resource]:
    """List resources available through the server."""
    return [
        types.Resource(
            uri=AnyUrl("intigriti://status"),
            name="Intigriti API Status",
            description="Check API connectivity and account validity",
            mimeType="text/plain",
        )
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read a specific resource."""
    if str(uri) == "intigriti://status":
        try:
            client = get_client()
            res = await client.get_programs(limit=1)
            return f"✅ Intigriti API Connected successfully. Accessible programs: {res.get('maxCount', 'Unknown')}"
        except Exception as e:
            return f"❌ Connection failed: {e}"
    raise ValueError(f"Unknown resource: {uri}")


async def cleanup():
    global api_client
    if api_client:
        await api_client.close()


async def main():
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
