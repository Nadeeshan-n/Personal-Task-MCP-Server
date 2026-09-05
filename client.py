import asyncio
#mport resource
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize connection
            await session.initialize()

            resources = await session.list_resources()

            print("\nAvailable resources:")

            for resource in resources.resources:
                print(f"- {resource.uri}")

            prompts = await session.list_prompts()

            print("\nAvailable prompts:")

            for prompt in prompts.prompts:
                print(f"- {prompt.name}")

            resource = await session.read_resource("tasks://all")

            print("\nAll tasks:")
            print(resource.contents)

            # Discover available tools
            tools = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call add_task
            result = await session.call_tool(
                "add_task",
                arguments={
                    "title": "Build an AI Agent"
                }
            )

            print("\nAdd task result:")
            print(result.content)

            # Call list_tasks
            result = await session.call_tool(
                "list_tasks",
                arguments={}
            )

            print("\nTask list:")
            print(result.content)

            result = await session.call_tool(
                "delete_task",
                arguments={
                    "task_id": 1
                }
            )
            print(result.content)




if __name__ == "__main__":
    asyncio.run(main())