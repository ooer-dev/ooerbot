from discord.ext import commands


class CleanMentions(commands.Converter):
    async def convert(self, ctx: commands.Context, string: str) -> str:
        """Clean up those silly mention inconsistencies across platforms."""
        for mention in ctx.message.mentions:
            string = string.replace(f'<@!{mention.id}>', f'<@{mention.id}>', 1)

        return string
