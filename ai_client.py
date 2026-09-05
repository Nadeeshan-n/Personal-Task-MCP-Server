import asyncio
import json
import os
import re

from google import genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # 1. Discover MCP tools
            tools_result = await session.list_tools()

            tool_descriptions = []

            for tool in tools_result.tools:
                tool_descriptions.append({
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                })

            tools_text = json.dumps(
                tool_descriptions,
                indent=2
            )

            # 2. Get user request
            user_message = input("\nYou: ")

            # 3. Ask Gemini which tool to use
            prompt = f"""
You are an AI assistant connected to an MCP task server.

Available MCP tools:

{tools_text}

User request:

{user_message}

If an MCP tool is required, respond ONLY with valid JSON:

{{
  "tool": "tool_name",
  "arguments": {{}}
}}

If no tool is required, respond ONLY with:

{{
  "tool": null,
  "arguments": {{}}
}}
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            decision_text = response.text.strip()

            print("\nGemini decision:")
            print(decision_text)

            # 4. Extract JSON
            match = re.search(
                r"\{.*\}",
                decision_text,
                re.DOTALL
            )

            if not match:
                print("Could not understand Gemini response.")
                return

            decision = json.loads(match.group())

            tool_name = decision["tool"]
            arguments = decision["arguments"]

            # 5. No tool required
            if tool_name is None:
                print("\nFinal answer:")
                print(user_message)
                return

            # 6. Call MCP tool
            print(f"\nCalling MCP tool: {tool_name}")
            print(f"Arguments: {arguments}")

            result = await session.call_tool(
                tool_name,
                arguments=arguments
            )

            # 7. Get MCP result
            tool_result = "\n".join(
                getattr(content, "text", str(content))
                for content in result.content
            )

            print("\nMCP result:")
            print(tool_result)

            # 8. Send MCP result back to Gemini
            final_prompt = f"""
Answer the user's request using the MCP tool result.

User:
{user_message}

MCP tool used:
{tool_name}

MCP result:
{tool_result}

Give a short natural-language response to the user.
"""

            final_response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=final_prompt
            )

            print("\nFinal answer:")
            print(final_response.text)


if __name__ == "__main__":
    asyncio.run(main())