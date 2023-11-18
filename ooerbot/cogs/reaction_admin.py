from typing import Annotated

from discord import Colour, Embed
from discord.ext import commands
from discord.ext.commands import Context

from ooerbot.api.client import ReactionAPI
from ooerbot.bot import OoerBot
from ooerbot.utils.converters import CleanMentions


class ReactionAdmin(commands.Cog):
    def __init__(self, bot: OoerBot) -> None:
        self.bot = bot
        self.api = ReactionAPI(str(bot.settings.api_url), bot.settings.api_key)

    async def cog_unload(self) -> None:
        await self.api.close()

    @commands.command(aliases=("addcustreact", "acr"))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def addreaction(
        self,
        ctx: Context[OoerBot],
        trigger: str,
        *,
        response: Annotated[str, CleanMentions],
    ) -> None:
        """Adds a new reaction."""

        assert ctx.guild is not None

        reaction = await self.api.create_reaction(ctx.guild.id, trigger, response)

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction.id} added")
        embed.add_field(name="Trigger", value=reaction.trigger)
        embed.add_field(name="Response", value=reaction.response)

        await ctx.send(embed=embed)

    @commands.command(aliases=("editcustreact", "ecr"))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def editreaction(
        self,
        ctx: Context[OoerBot],
        reaction_id: int,
        *,
        response: Annotated[str, CleanMentions],
    ) -> None:
        """Edits the reaction."""

        assert ctx.guild is not None

        reaction = await self.api.update_reaction(ctx.guild.id, reaction_id, response)

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction.id} edited")
        embed.add_field(name="Trigger", value=reaction.trigger)
        embed.add_field(name="Response", value=reaction.response)

        await ctx.send(embed=embed)

    @commands.command(aliases=("listcustreact", "lcr"))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def listreactions(self, ctx: Context[OoerBot]) -> None:
        """Lists all reactions."""

        await ctx.send(
            f"Reaction admin is now available at {self.bot.settings.api_url}",
        )

    @commands.command(aliases=("showcustreact", "scr"))
    @commands.check_any(commands.guild_only())
    async def showreaction(self, ctx: Context[OoerBot], reaction_id: int) -> None:
        """Shows a reaction."""

        assert ctx.guild is not None

        reaction = await self.api.get_reaction(ctx.guild.id, reaction_id)

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction.id}")
        embed.add_field(name="Trigger", value=reaction.trigger)
        embed.add_field(name="Response", value=reaction.response)

        await ctx.send(embed=embed)

    @commands.command(aliases=("delcustreact", "dcr"))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def deletereaction(self, ctx: Context[OoerBot], reaction_id: int) -> None:
        """Deletes the reaction."""

        assert ctx.guild is not None

        await self.api.delete_reaction(ctx.guild.id, reaction_id)

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction_id} deleted")

        await ctx.send(embed=embed)

    @commands.command(name="crca")
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def contains_anywhere(self, ctx: Context[OoerBot], reaction_id: int) -> None:
        """Toggles searching for the trigger anywhere in a message."""

        assert ctx.guild is not None

        reaction = await self.api.get_reaction(ctx.guild.id, reaction_id)
        reaction = await self.api.update_reaction(
            ctx.guild.id,
            reaction_id,
            contains_anywhere=not reaction.contains_anywhere,
        )

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction_id} edited")
        embed.add_field(name="Contains anywhere", value=reaction.contains_anywhere)

        await ctx.send(embed=embed)

    @commands.command(name="crdm")
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def dm_response(self, ctx: Context[OoerBot], reaction_id: int) -> None:
        """Toggles direct messaging the reaction response."""

        assert ctx.guild is not None

        reaction = await self.api.get_reaction(ctx.guild.id, reaction_id)
        reaction = await self.api.update_reaction(
            ctx.guild.id,
            reaction_id,
            dm_response=not reaction.dm_response,
        )

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction_id} edited")
        embed.add_field(name="DM response", value=reaction.dm_response)

        await ctx.send(embed=embed)

    @commands.command(name="crad")
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def delete_trigger(self, ctx: Context[OoerBot], reaction_id: int) -> None:
        """Toggles deleting the reaction trigger."""

        assert ctx.guild is not None

        reaction = await self.api.get_reaction(ctx.guild.id, reaction_id)
        reaction = await self.api.update_reaction(
            ctx.guild.id,
            reaction_id,
            delete_trigger=not reaction.delete_trigger,
        )

        embed = Embed(colour=Colour.pink(), title=f"Reaction #{reaction_id} edited")
        embed.add_field(name="Delete trigger", value=reaction.delete_trigger)

        await ctx.send(embed=embed)


async def setup(bot: OoerBot) -> None:
    await bot.add_cog(ReactionAdmin(bot))
