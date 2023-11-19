import random

from discord import Embed, Role
from discord.ext import commands
from discord.ext.commands import Context

from ooerbot.bot import OoerBot


class Utilities(commands.Cog):
    def __init__(self, bot: OoerBot) -> None:
        self.bot = bot

    @commands.command()
    async def inrole(self, ctx: Context[OoerBot], *, role: Role) -> None:
        """List all members with a given role."""

        members = [m.mention for m in role.members]

        embed = Embed(
            title=f"Members in role {role.name}",
            description="\n".join(members),
        )
        embed.set_footer(text=f"Total: {len(members)}")

        await ctx.send(embed=embed)

    @commands.command()
    async def raffle(self, ctx: Context[OoerBot], *, role: Role) -> None:
        """Select a random member with a given role."""

        winner = random.choice(role.members).mention

        embed = Embed(title=f"{winner} is one of today's lucky 10,000!")

        await ctx.send(embed=embed)


async def setup(bot: OoerBot) -> None:
    await bot.add_cog(Utilities(bot))
