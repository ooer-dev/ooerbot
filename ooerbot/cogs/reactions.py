import random
import re
from typing import Dict, List

import discord
from discord.ext import commands

from ooerbot.apis.reactions import get_reactions_for_guild
from ooerbot.bot import OoerBot
from ooerbot.models.reaction import Reaction
from ooerbot.utils.replacer import replace_reaction_placeholders


class Reactions(commands.Cog):
    def __init__(self, bot: OoerBot) -> None:
        self.bot = bot
        self._reaction_cache: Dict[int, List[Reaction]] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.fetch_initial_reactions()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        reactions = self._get_possible_reactions(message)
        if not reactions:
            return

        reaction = random.choice(reactions)

        reference = message
        messageable = message.channel

        if reaction.delete_trigger:
            reference = None
            await message.delete(delay=0)  # setting this to a 0 delay just puts it in the background immediately

        if reaction.dm_response:
            messageable = message.author
            reference = None

        response = replace_reaction_placeholders(self.bot, message, reaction.response)

        if reaction.has_target:
            target = message.content.removeprefix(reaction.trigger + ' ')
            response = response.replace('%target%', target)

        await messageable.send(response, reference=reference)

    async def fetch_initial_reactions(self):
        guild: discord.Guild
        for guild in self.bot.guilds:
            reactions = await get_reactions_for_guild(guild.id)

            self._reaction_cache[guild.id] = reactions

    def _get_possible_reactions(self, message: discord.Message) -> List[Reaction]:
        trigger: str = message.content
        trigger.rstrip()
        for mention in message.mentions:
            trigger = trigger.replace(f'<@!{mention.id}>', f'<@{mention.id}>', 1)

        reactions = self._reaction_cache.get(message.guild.id)
        if reactions is None:
            return []

        matches = []
        for reaction in reactions:
            if len(trigger) > len(reaction.trigger):
                if reaction.contains_anywhere:
                    if re.search(f'\\b{re.escape(reaction.trigger)}\\b', trigger, re.IGNORECASE):
                        matches.append(reaction)
                    else:
                        continue

                if reaction.has_target and trigger.startswith(reaction.trigger + ' '):
                    matches.append(reaction)
            elif len(trigger) == len(reaction.trigger):
                if trigger == reaction.trigger:
                    matches.append(reaction)

        return matches


def setup(bot: OoerBot) -> None:
    bot.add_cog(Reactions(bot))
