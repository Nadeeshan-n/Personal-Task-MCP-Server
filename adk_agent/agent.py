from pathlib import Path
import sys

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MCP_SERVER = PROJECT_ROOT / "server.py"


root_agent = LlmAgent(
    name="task_agent",
    model="gemini-flash-latest",
    description="An AI task manager using an MCP server.",
    instruction="""
You are a task management assistant.

Use the MCP tools to manage the user's tasks.

You can:
- Add tasks
- List tasks
- Complete tasks
- Delete tasks
- Search tasks

When the user asks you to perform an operation on a task,
use the appropriate MCP tool.

After completing an operation, clearly tell the user what happened.
""",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,
                    args=[str(MCP_SERVER)],
                ),
                timeout=10,
            ),
            tool_filter=[
                "add_task",
                "list_tasks",
                "complete_task",
            ],
        )
    ]   
)