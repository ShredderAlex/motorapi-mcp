#!/usr/bin/env python3
"""MCP Server for MotorAPI.dk - Danish vehicle registration lookup."""

import os
import asyncio
import httpx
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Configuration
BASE_URL = "https://v1.motorapi.dk"
API_KEY = os.getenv("MOTORAPI_KEY", "ggsysjljhuwad03hcxvlwnqgf5toihft")
AUTH_HEADER = "X-AUTH-TOKEN"

# Initialize MCP server
app = Server("motorapi-mcp")


class MotorAPIClient:
    """Client for interacting with MotorAPI.dk."""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            AUTH_HEADER: API_KEY,
            "Accept": "application/json"
        }
    
    async def get_vehicle(self, reg_no_or_vin: str) -> dict:
        """Get vehicle details by registration number or VIN."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/vehicles/{reg_no_or_vin}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return {"error": f"Vehicle not found: {reg_no_or_vin}"}
                raise
            except Exception as e:
                return {"error": str(e)}
    
    async def get_environment(self, reg_no_or_vin: str) -> dict:
        """Get environmental details for a vehicle."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/vehicles/{reg_no_or_vin}/environment",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return {"error": f"Environmental data not found for: {reg_no_or_vin}"}
                raise
            except Exception as e:
                return {"error": str(e)}
    
    async def get_equipment(self, reg_no_or_vin: str) -> dict:
        """Get equipment details for a vehicle."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/vehicles/{reg_no_or_vin}/equipment",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return {"error": f"Equipment data not found for: {reg_no_or_vin}"}
                raise
            except Exception as e:
                return {"error": str(e)}
    
    async def get_usage(self) -> dict:
        """Get API usage statistics."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/usage",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": str(e)}


# Initialize client
client = MotorAPIClient()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_vehicle",
            description="Get detailed information about a Danish vehicle by registration number or VIN. Returns vehicle specifications, registration details, and technical information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reg_no_or_vin": {
                        "type": "string",
                        "description": "Vehicle registration number (e.g., 'AB12345') or VIN number"
                    }
                },
                "required": ["reg_no_or_vin"]
            }
        ),
        Tool(
            name="get_vehicle_environment",
            description="Get environmental information for a Danish vehicle, including emissions data, fuel consumption, and environmental classification.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reg_no_or_vin": {
                        "type": "string",
                        "description": "Vehicle registration number (e.g., 'AB12345') or VIN number"
                    }
                },
                "required": ["reg_no_or_vin"]
            }
        ),
        Tool(
            name="get_vehicle_equipment",
            description="Get equipment and features list for a Danish vehicle, including factory-installed options and accessories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reg_no_or_vin": {
                        "type": "string",
                        "description": "Vehicle registration number (e.g., 'AB12345') or VIN number"
                    }
                },
                "required": ["reg_no_or_vin"]
            }
        ),
        Tool(
            name="get_api_usage",
            description="Get current API usage statistics, including request count, quota limits, and remaining requests.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    import json
    
    try:
        if name == "get_vehicle":
            reg_no_or_vin = arguments["reg_no_or_vin"]
            result = await client.get_vehicle(reg_no_or_vin)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "get_vehicle_environment":
            reg_no_or_vin = arguments["reg_no_or_vin"]
            result = await client.get_environment(reg_no_or_vin)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "get_vehicle_equipment":
            reg_no_or_vin = arguments["reg_no_or_vin"]
            result = await client.get_equipment(reg_no_or_vin)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "get_api_usage":
            result = await client.get_usage()
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
