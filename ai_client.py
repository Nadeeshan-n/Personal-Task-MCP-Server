import asyncio
import os

from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # Gemini client
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    # MCP server configuration
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    # Start MCP server
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP
            await session.initialize()

            # Discover MCP tools
            tools_result = await session.list_tools()

            print("\nMCP tools:")

            for tool in tools_result.tools:
                print(f"- {tool.name}")

            # Convert MCP tools to a simple description
            tool_descriptions = []

            for tool in tools_result.tools:
                tool_descriptions.append(
                    f"""
Tool: {tool.name}
Description: {tool.description}
Input schema: {tool.inputSchema}
"""
                )

            tools_text = "\n".join(tool_descriptions)

            # User request
            user_message = input("\nYou: ")

            prompt = f"""
You are an AI assistant connected to an MCP server.

Available MCP tools:

{tools_text}

User request:
{user_message}

Decide whether an MCP tool should be used.

If a tool is needed, respond ONLY with:

TOOL: tool_name
ARGUMENTS: JSON

If no tool is needed, respond ONLY with:

NO_TOOL
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            print("\nGemini:")
            print(response.text)


if __name__ == "__main__":
    asyncio.run(main())