# Model Context Protocol (MCP) in ADK

The Model Context Protocol (MCP) allows agents to connect to external data sources and tools using a unified protocol.

## McpToolset

In ADK, `McpToolset` acts as a client that connects to an MCP server and dynamically registers all its tools to the ADK agent.

### Imports
```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioServerParameters
from google.adk.tools.mcp_tool import StdioConnectionParams
```

### Connection Types

#### 1. Stdio Connection (Local MCP Server)
Runs the server as a local subprocess via stdio.
```python
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", "app/mock_mcp_server.py"]
        )
    )
)
```

#### 2. SSE Connection (Remote/Network Server)
Connects to an HTTP/SSE endpoint.
```python
from google.adk.tools.mcp_tool import SseConnectionParams

mcp_toolset = McpToolset(
    connection_params=SseConnectionParams(
        url="https://developerknowledge.googleapis.com/mcp",
        headers={"X-Goog-Api-Key": "YOUR_API_KEY"}
    )
)
```
