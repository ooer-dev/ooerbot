from discord.ext import commands


class NotAdmin(commands.CheckFailure):
    pass


# TODO: Figure out how to type hint the return type of this decorator
def is_admin():  # type: ignore
    async def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id not in ctx.bot.owner_ids:
            raise NotAdmin('You are not an admin of this bot.')
        return True

    return commands.check(predicate)


def is_guild_admin():
    original = commands.has_permissions(administrator=True).predicate

    async def extended_check(ctx: commands.Context) -> bool:
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)

    return commands.check(extended_check)
