# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import sys

from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPSessionManager
from mcp import StdioServerParameters


async def main():
    print("Initializing MCPSessionManager for local mock MCP server...")

    # Configure stdio connection params to launch our mock_mcp_server.py
    connection_params = StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", "app/mock_mcp_server.py"],
        )
    )

    # Initialize the session manager
    session_manager = MCPSessionManager(connection_params=connection_params)

    try:
        # Create/initialize the MCP session
        print("Connecting to local MCP server...")
        session = await session_manager.create_session()

        # 1. Search documentation for "strict schema"
        print("\nStep 1: Searching documentation for 'strict schema'...")
        search_result = await session.call_tool(
            "search_documents", {"query": "strict schema"}
        )

        # Display search results
        print("\n--- Search Results ---")
        for content_part in search_result.content:
            if hasattr(content_part, "text"):
                print(content_part.text)

        # 2. Get the specific document developer_api_schema.md
        print("\nStep 2: Retrieving full content of 'developer_api_schema.md'...")
        doc_result = await session.call_tool(
            "get_document", {"doc_name": "developer_api_schema.md"}
        )

        # Display document contents
        print("\n--- Document Contents ---")
        for content_part in doc_result.content:
            if hasattr(content_part, "text"):
                print(content_part.text)

    except Exception as e:
        print(f"Error during MCP query: {e}", file=sys.stderr)
    finally:
        # Gracefully shut down the connection
        print("\nClosing MCP session...")
        await session_manager.close()
        print("MCP session closed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
