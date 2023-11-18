from discord.ext.commands import Context, Converter

from ooerbot.bot import OoerBot


class CleanMentions(Converter[str]):
    async def convert(self, ctx: Context[OoerBot], string: str) -> str:  # type: ignore[override]
        """Clean up those silly mention inconsistencies across platforms."""
        for mention in ctx.message.mentions:
            string = string.replace(f"<@!{mention.id}>", f"<@{mention.id}>", 1)

        return string
