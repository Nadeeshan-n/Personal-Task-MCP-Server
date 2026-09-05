
from mcp.server.fastmcp import FastMCP
from google.adk.tools import FunctionTool
import json

mcp = FastMCP("Task Server")

TASKS_FILE = "tasks.json"


def load_tasks():
    with open(TASKS_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)


@mcp.tool()
def add_task(title: str) -> str:
    """Add a new task."""

    if not title.strip():
        return "Error: Task title cannot be empty."

    tasks = load_tasks()

    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    task = {
        "id": new_id,
        "title": title.strip(),
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return f"Task created: {task['id']} - {task['title']}"

@mcp.tool()
def list_tasks() -> str:
    """List all tasks."""
    tasks = load_tasks()

    if not tasks:
        return "No tasks found."

    return "\n".join(
        f"{task['id']} - {task['title']} - "
        f"{'completed' if task['completed'] else 'pending'}"
        for task in tasks
    )


@mcp.tool()
def complete_task(task_id: int) -> str:
    """Mark a task as completed."""

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            if task["completed"]:
                return f"Task {task_id} is already completed."

            task["completed"] = True
            save_tasks(tasks)

            return f"Task {task_id} completed."

    return f"Task {task_id} not found."

@mcp.tool()
def delete_task(task_id: int) -> str:
    """Delete a task."""

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)
            save_tasks(tasks)

            return f"Task {task_id} deleted."

    return f"Task {task_id} not found."

@mcp.resource("tasks://all")
def get_all_tasks() -> str:
    """Return all tasks."""
    tasks = load_tasks()

    return json.dumps(tasks, indent=2)
@mcp.prompt()
def daily_task_review() -> str:
    """Create a prompt for reviewing today's tasks."""
    return """
Review my current tasks.

Identify:
1. Which tasks are still pending.
2. Which task should be completed first.
3. Give a short reason for your recommendation.
"""

@mcp.tool()
def search_tasks(keyword: str) -> str:
    """Search tasks by title."""

    if not keyword.strip():
        return "Error: Search keyword cannot be empty."

    tasks = load_tasks()

    matches = [
        task for task in tasks
        if keyword.lower() in task["title"].lower()
    ]

    if not matches:
        return f"No tasks found matching '{keyword}'."

    return "\n".join(
        f"{task['id']} - {task['title']} - "
        f"{'completed' if task['completed'] else 'pending'}"
        for task in matches
    )

from google.adk.tools import FunctionTool


def get_current_tasks() -> str:
    """
    Read the current tasks from the task MCP server.

    This function is only a demonstration of how an ADK agent
    can use MCP-provided data as context.
    """
    # We will connect this directly to the MCP resource
    # in the next step.
    return "Use the MCP tasks resource: tasks://all"


get_tasks_tool = FunctionTool(func=get_current_tasks)


if __name__ == "__main__":
    mcp.run()