from typing import Any

import aiohttp

from ooerbot.api.models import Reaction


class ReactionAPI:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.client = aiohttp.ClientSession(
            base_url=base_url,
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer " + api_key,
                "User-Agent": "OoerBot/1.0",
            },
        )

    async def close(self) -> None:
        await self.client.close()

    async def get_reactions(self, guild_id: int) -> list[Reaction]:
        async with self.client.get(f"/api/guild/{guild_id}/reaction") as resp:
            json = await resp.json()
            data = json["data"]

        return [Reaction(**r) for r in data]

    async def create_reaction(
        self,
        guild_id: int,
        trigger: str,
        response: str,
    ) -> Reaction:
        async with self.client.post(
            f"/api/guild/{guild_id}/reaction",
            json={
                "trigger": trigger,
                "response": response,
            },
        ) as resp:
            json = await resp.json()
            data = json["data"]

        return Reaction(**data)

    async def get_reaction(self, guild_id: int, reaction_id: int) -> Reaction:
        async with self.client.get(
            f"/api/guild/{guild_id}/reaction/{reaction_id}",
        ) as resp:
            json = await resp.json()
            data = json["data"]

        return Reaction(**data)

    async def update_reaction(
        self,
        guild_id: int,
        reaction_id: int,
        response: str | None = None,
        contains_anywhere: bool | None = None,
        delete_trigger: bool | None = None,
        dm_response: bool | None = None,
    ) -> Reaction:
        json: dict[str, Any] = {}
        if response is not None:
            json["response"] = response
        if contains_anywhere is not None:
            json["contains_anywhere"] = contains_anywhere
        if delete_trigger is not None:
            json["delete_trigger"] = delete_trigger
        if dm_response is not None:
            json["dm_response"] = dm_response

        async with self.client.patch(
            f"/api/guild/{guild_id}/reaction/{reaction_id}",
            json=json,
        ) as resp:
            json = await resp.json()
            data = json["data"]

        return Reaction(**data)

    async def delete_reaction(self, guild_id: int, reaction_id: int) -> bool:
        async with self.client.delete(
            f"/api/guild/{guild_id}/reaction/{reaction_id}",
        ) as resp:
            return resp.status == 204
