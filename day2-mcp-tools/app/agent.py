# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioServerParameters
from google.adk.tools.mcp_tool import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        query: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


# Check if an API key is configured for the official Developer Knowledge MCP server
dk_api_key = (
    os.environ.get("DEVELOPER_KNOWLEDGE_API_KEY")
    or os.environ.get("X_Goog-Api-Key")
    or os.environ.get("GOOGLE_API_KEY")
)

if dk_api_key:
    # Use official Developer Knowledge MCP server over SSE/Streamable HTTP
    mcp_toolset = McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="https://developerknowledge.googleapis.com/mcp",
            headers={"X-Goog-Api-Key": dk_api_key},
        )
    )
else:
    # Fallback to local mock MCP server via stdio transport
    mcp_toolset = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uv",
                args=["run", "python", "app/mock_mcp_server.py"],
            )
        )
    )


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are a helpful AI assistant designed to provide accurate and useful information. "
        "Use the developer documentation tools to search and retrieve information when asked "
        "about Google Developer topics such as ADK, MCP, or Agent Engines."
    ),
    tools=[get_weather, get_current_time, mcp_toolset],
)

app = App(
    root_agent=root_agent,
    name="app",
)
