
from mcp.server.fastmcp import FastMCP
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
    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "title": title,
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
            task["completed"] = True
            save_tasks(tasks)
            return f"Task {task_id} completed."

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




if __name__ == "__main__":
    mcp.run()