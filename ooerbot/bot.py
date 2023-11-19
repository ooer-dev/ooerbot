from __future__ import annotations

import logging
from typing import Any

import discord
from discord.ext import commands
from discord.ext.commands import CommandError, CommandNotFound, Context

from ooerbot.settings import Settings


class OoerBot(commands.Bot):
    def __init__(self, settings: Settings, **kwargs: Any) -> None:
        command_prefix = "."

        owner_ids = kwargs.pop("owner_ids", settings.admin_user_ids)

        case_insensitive = kwargs.pop("case_insensitive", True)

        default_intents = discord.Intents(
            guilds=True,
            members=True,  # privileged intent
            guild_messages=True,
            message_content=True,  # privileged intent
        )

        intents = kwargs.pop("intents", default_intents)

        super().__init__(
            command_prefix,
            owner_ids=owner_ids,
            case_insensitive=case_insensitive,
            intents=intents,
            activity=discord.Game("OMAN I AM NOT GOOD WITH COMPUTER"),
            **kwargs,
        )

        self.log = logging.getLogger(__name__)
        self.settings = settings
        self._extensions_to_load = [
            "ooerbot.cogs.reactions",
            "ooerbot.cogs.reaction_admin",
            "ooerbot.cogs.utilities",
        ]

    async def setup_hook(self) -> None:
        for name in self._extensions_to_load:
            try:
                await self.load_extension(name)
            except Exception as error:
                self.log.error("%s cannot be loaded: %s", name, error)

    async def on_ready(self) -> None:
        self.log.info("OoerBot is online")

    async def on_resumed(self) -> None:
        self.log.warning("OoerBot RECONNECT")

    async def on_command_error(
        self,
        context: Context[OoerBot],  # type: ignore[override]
        exception: CommandError,
    ) -> None:
        if isinstance(exception, CommandNotFound):
            return

        await super().on_command_error(context, exception)
