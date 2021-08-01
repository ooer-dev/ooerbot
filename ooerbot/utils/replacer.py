import re

import discord

from ooerbot.bot import OoerBot


def replace_reaction_placeholders(bot: OoerBot, message: discord.Message, response: str) -> str:
    guild: discord.Guild = message.guild
    channel: discord.TextChannel = message.channel
    member: discord.Member = message.author

    # This maintains a lot of parity with a similar bot's reaction placeholders
    replacements = {
        'bot.avatar': str(bot.user.avatar_url),
        'bot.discrim': bot.user.discriminator,
        'bot.fullname': str(bot.user),
        'bot.id': str(bot.user.id),
        'bot.latency': str(bot.latency),
        'bot.mention': bot.user.mention,
        'bot.name': bot.user.name,
        'bot.status': str(message.guild.me.status),
        'bot.time': '',

        'channel.created': '',
        'channel.id': str(channel.id),
        'channel.mention': channel.mention,
        'channel.name': channel.name,
        'channel.nsfw': str(channel.nsfw),
        'channel.topic': channel.topic,

        'server.id': str(guild.id),
        'server.members': str(guild.member_count),
        'server.name': guild.name,
        'server.time': '',

        'user': member.mention,
        'user.avatar': str(member.avatar_url),
        'user.created_date': '',
        'user.created_time': '',
        'user.discrim': str(member.discriminator),
        'user.fullname': str(member),
        'user.id': str(member.id),
        'user.joined_date': '',
        'user.joined_time': '',
        'user.mention': member.mention,
        'user.name': member.name,
    }

    def lookup(match):
        orig = match.group(0)
        key = match.group(1)
        return replacements.get(key, orig)

    response = re.sub(r'%([a-z.]+)%', lookup, response)

    return response
