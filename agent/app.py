import asyncio
import json
import os

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.openai_client import OpenAIClient
from agent.models.message import Message, Role
from constants import OPENAI_API_KEY

SYSTEM_PROMPT="""
You are the **User Management Agent** responsible for handling user-related operations within a controlled system.

Your role:
- Manage user data in a professional, consistent, and domain-safe manner.

Your tasks:
- Perform CRUD operations (create, read, update, delete) on user records.
- Search and filter users by given parameters.
- Process web search
- Enrich or update user profiles using available non-sensitive information.
- Validate data integrity before any operation.
- Confirm each successful operation and provide concise, structured responses.

Constraints:
- Never generate, infer, or expose any sensitive or personally identifiable information (PII).
- Do not access or discuss data outside the defined user domain.
- Stay within the limits of authorized API functions and provided context.

Behavior:
- Maintain a professional and neutral tone.
- Always explain detected errors or validation issues briefly and suggest corrective actions.
- When uncertain or missing data, request clarification rather than guessing.

Goal:
Provide safe, deterministic, and auditable user management assistance.
"""
async def main():
    #TODO:
    # 1. Take a look what applies OpenAIClient
    # 2. Create empty list where you save tools from MCP Servers later
    # 3. Create empty dict where where key is str (tool name) and value is instance of MCPClient or CustomMCPClient
    # 4. Create UMS MCPClient, url is `http://localhost:8006/mcp` (use static method create and don't forget that its async)
    # 5. Collect tools and dict [tool name, mcp client]
    # 6. Do steps 4 and 5 for `https://remote.mcpservers.org/fetch/mcp`
    # 7. Create OpenAIClient
    # 8. Create array with Messages and add there System message with simple instructions for LLM that it should help to handle user request
    # 9. Create simple console chat (as we done in previous tasks)
    tools = []
    tool_to_client: dict[str, MCPClient] = {}

    ums_client = await MCPClient.create(
        mcp_server_url="http://localhost:8006/mcp"
    )

    ums_tools = await ums_client.get_tools()
    for tool in ums_tools:
        tools.append(tool)
        tool_to_client[tool["function"]["name"]] = ums_client

    remote_client = await MCPClient.create(
        mcp_server_url="https://remote.mcpservers.org/fetch/mcp"
    )

    remote_tools = await remote_client.get_tools()
    for tool in remote_tools:
        tools.append(tool)
        tool_to_client[tool["function"]["name"]] = remote_client

    openai_client = OpenAIClient(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        tools=tools,
        tool_name_client_map=tool_to_client
    )

    messages = [
        Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)
    ]

    print("\n--- Console Chat (type 'exit' to quit) ---")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append(Message(role="user", content=user_input))

        ai_response = await openai_client.get_completion(messages)
        print(f"AI: {ai_response.content}")

        messages.append(Message(role="assistant", content=ai_response.content))



if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him