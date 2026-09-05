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

            await session.initialize()

            resources = await session.list_resources()

            print("\nAvailable resources:")

            for resource in resources.resources:
                print("-", resource.uri)

            result = await session.read_resource("tasks://all")

            print("\nResource contents:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())