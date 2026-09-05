from google.adk.agents import Agent


root_agent = Agent(
    name="task_agent",
    model="gemini-2.5-flash",
    description="An AI assistant that manages tasks.",
    instruction="""
    You are a task management assistant.

    You help users:
    - Add tasks
    - List tasks
    - Complete tasks
    - Delete tasks
    - Search tasks
    """,
)