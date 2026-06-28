# Google Agent Development Kit (ADK) Guidance

The Google Agent Development Kit (ADK) is an open-source, code-first framework designed for building, debugging, and deploying sophisticated AI agents.

## Core Concepts

### 1. Agent
An `Agent` object represents an individual LLM-powered entity. It has a specific role, defined by instructions, models, and tools.
Example:
```python
from google.adk.agents import Agent
from google.adk.models import Gemini

agent = Agent(
    name="my_agent",
    model=Gemini(model="gemini-flash-latest"),
    instruction="You are a helper agent.",
    tools=[some_function],
)
```

### 2. App
An `App` connects the agent system together and wraps them for execution.
Example:
```python
from google.adk.apps import App

app = App(
    root_agent=agent,
    name="my_app",
)
```

### 3. Toolset
A `Toolset` exposes a group of tools. The `McpToolset` is used to integrate external MCP servers.
