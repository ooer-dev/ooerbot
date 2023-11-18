import datetime
import random
import re

import discord

from ooerbot.bot import OoerBot


def replace_reaction_placeholders(
    bot: OoerBot, message: discord.Message, response: str
) -> str:
    # Doing some asserts here to make sure we don't get any weird types
    assert bot.user is not None

    guild = message.guild
    assert guild is not None

    channel = message.channel
    assert isinstance(channel, (discord.TextChannel, discord.Thread))
    assert channel.created_at is not None

    member = message.author
    assert isinstance(member, discord.Member)
    assert member.joined_at is not None

    # This maintains a lot of parity with a similar bot's reaction placeholders
    replacements = {
        "bot.avatar": str(bot.user.display_avatar.url),
        "bot.discrim": bot.user.discriminator,
        "bot.fullname": str(bot.user),
        "bot.id": str(bot.user.id),
        "bot.latency": str(bot.latency),
        "bot.mention": bot.user.mention,
        "bot.name": bot.user.name,
        "bot.status": str(guild.me.status),
        "bot.time": datetime.datetime.utcnow().strftime("%H:%M UTC"),
        "channel.created": channel.created_at.strftime("%H:%M %d.%m.%Y"),
        "channel.id": str(channel.id),
        "channel.mention": channel.mention,
        "channel.name": channel.name,
        "channel.nsfw": str(getattr(channel, "nsfw", False)),
        "channel.topic": getattr(channel, "topic", ""),
        "server.id": str(guild.id),
        "server.members": str(guild.member_count),
        "server.name": guild.name,
        "server.time": datetime.datetime.utcnow().strftime("%H:%M UTC"),
        "user": member.mention,
        "user.avatar": str(member.display_avatar.url),
        "user.created_date": member.created_at.strftime("%d.%m.%Y"),
        "user.created_time": member.created_at.strftime("%H:%M"),
        "user.discrim": str(member.discriminator),
        "user.fullname": str(member),
        "user.id": str(member.id),
        "user.joined_date": member.joined_at.strftime("%d.%m.%Y"),
        "user.joined_time": member.joined_at.strftime("%H:%M"),
        "user.mention": member.mention,
        "user.name": member.name,
    }

    def lookup(match: re.Match[str]) -> str:
        orig = match.group(0)
        key = match.group(1)
        return replacements.get(key, orig)

    response = re.sub(r"%([a-z._]+)%", lookup, response)

    def rng(match: re.Match[str]) -> str:
        start = int(match.group("from") or 0)
        stop = int(match.group("to") or 0)

        if start == 0 and stop == 0:
            start = 0
            stop = 10

        if start >= stop:
            return ""

        return str(random.randint(start, stop))

    response = re.sub(r"%rng(?:(?P<from>(?:-)?\d+)-(?P<to>(?:-)?\d+))?%", rng, response)

    return response
