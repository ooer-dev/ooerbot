import logging
from typing import Any, List

import discord
from discord.ext import commands

from config import ADMIN_USER_IDS


class OoerBot(commands.Bot):
    def __init__(self, **kwargs: Any) -> None:
        command_prefix = '.'
        owner_ids = kwargs.pop('owner_ids', set(ADMIN_USER_IDS))
        case_insensitive = kwargs.pop('case_insensitive', True)

        default_intents = discord.Intents(
            members=True,  # privileged intent, enable Members in dashbaord
            guilds=True,
            messages=True,
        )

        intents = kwargs.pop('intents', default_intents)

        super().__init__(
            command_prefix,
            owner_ids=owner_ids,
            case_insensitive=case_insensitive,
            intents=intents,
            activity=discord.Game('OMAN I AM NOT GOOD WITH COMPUTER'),
            **kwargs,
        )

        self.banned_user_ids: List[int] = []

        self.log = logging.getLogger(__name__)
        self._extensions_to_load = [
            'ooerbot.cogs.reactions',
        ]

    def load_extensions(self) -> None:
        for name in self._extensions_to_load:
            try:
                self.load_extension(name)
            except Exception as error:
                self.log.error('%s cannot be loaded: %s', name, error)

    def reload_extensions(self) -> None:
        for name in self._extensions_to_load:
            try:
                self.reload_extension(name)
            except Exception as error:
                self.log.error('%s cannot be reloaded: %s', name, error)

    async def on_ready(self) -> None:
        self.log.info('OoerBot is online')

    async def on_resumed(self) -> None:
        self.log.warning('OoerBot RECONNECT')

    def add_command(self, command: commands.Command) -> None:
        command.cooldown_after_parsing = True

        super().add_command(command)
