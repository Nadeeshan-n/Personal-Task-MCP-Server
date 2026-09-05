from pathlib import Path
import sys

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters


# Find server.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MCP_SERVER = PROJECT_ROOT / "server.py"


# Connect ADK to our MCP server
task_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[str(MCP_SERVER)],
        ),
        timeout=10,
    )
)


# ADK Agent
root_agent = Agent(
    name="task_agent",
    model="gemini-3.6-flash",
    description="An AI assistant that manages tasks using an MCP server.",
    instruction="""
You are a task management assistant.

You have access to task-management tools through an MCP server.

You can:
- Add tasks
- List tasks
- Complete tasks
- Delete tasks
- Search tasks

Always use the available MCP tools when the user wants to perform
an operation on their tasks.

Be concise and helpful.
""",
    tools=[task_mcp],
)