import random
import re

import discord
from discord.ext import commands

from ooerbot.api.client import ReactionAPI
from ooerbot.api.models import Reaction
from ooerbot.bot import OoerBot
from ooerbot.utils.replacer import replace_reaction_placeholders


class Reactions(commands.Cog):
    def __init__(self, bot: OoerBot) -> None:
        self.bot = bot
        self.api = ReactionAPI(str(bot.settings.api_url), bot.settings.api_key)
        self._reaction_cache: dict[int, list[Reaction]] = {}

    async def cog_unload(self) -> None:
        await self.api.close()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.fetch_initial_reactions()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return

        reactions = self._get_possible_reactions(message)
        if not reactions:
            return

        reaction = random.choice(reactions)

        reference: discord.Message | None = message
        messageable: discord.abc.Messageable = message.channel

        if reaction.delete_trigger:
            reference = None
            await message.delete(delay=0)  # delay=0 runs in background

        if reaction.dm_response:
            messageable = message.author
            reference = None

        response = replace_reaction_placeholders(self.bot, message, reaction.response)

        if reaction.has_target:
            target = message.content.removeprefix(reaction.trigger + " ")
            response = response.replace("%target%", target)

        await messageable.send(content=response, reference=reference)  # type: ignore[arg-type]

    async def fetch_initial_reactions(self) -> None:
        guild: discord.Guild
        for guild in self.bot.guilds:
            reactions = await self.api.get_reactions(guild.id)

            self._reaction_cache[guild.id] = reactions

    def _get_possible_reactions(self, message: discord.Message) -> list[Reaction]:
        trigger: str = message.content.lower().rstrip()
        for mention in message.mentions:
            trigger = trigger.replace(f"<@!{mention.id}>", f"<@{mention.id}>", 1)

        assert message.guild is not None

        reactions = self._reaction_cache.get(message.guild.id)
        if reactions is None:
            return []

        matches = []
        for reaction in reactions:
            if len(trigger) > len(reaction.trigger):
                if reaction.contains_anywhere:
                    if re.search(f"\\b{re.escape(reaction.trigger)}\\b", trigger):
                        matches.append(reaction)
                    else:
                        continue

                if reaction.has_target and trigger.startswith(reaction.trigger + " "):
                    matches.append(reaction)
            elif len(trigger) == len(reaction.trigger):
                if trigger == reaction.trigger:
                    matches.append(reaction)

        return matches


async def setup(bot: OoerBot) -> None:
    await bot.add_cog(Reactions(bot))
