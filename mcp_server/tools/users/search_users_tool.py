from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class SearchUsersTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        #TODO: Provide tool name as `search_users`
        return "search_users"

    @property
    def description(self) -> str:
        #TODO: Provide description of this tool
        return "Search users by a given parameters(name, surname, email, gender)"

    @property
    def input_schema(self) -> dict[str, Any]:
        #TODO:
        # Provide tool params Schema:
        # - name: str
        # - surname: str
        # - email: str
        # - gender: str
        # None of them are required (see UserClient.search_users method)
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User name"
                },
                "surname": {
                    "type": "string",
                    "description": "Surname of a user"
                },
                "email": {
                    "type": "string",
                    "description": "Email of a user"
                },
                "gender": {
                    "type": "string",
                    "description": "Gender of a user"
                }
            }
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        #TODO:
        # Call user_client search_users (with `**arguments`) and return its results (it is async, don't forget to await)
        return await self._user_client.search_users(**arguments)