import asyncio
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

            # Discover available tools
            tools = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call add_task
            result = await session.call_tool(
                "add_task",
                arguments={
                    "title": "Learn MCP"
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


if __name__ == "__main__":
    asyncio.run(main())