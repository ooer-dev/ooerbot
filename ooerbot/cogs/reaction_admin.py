from discord.ext import commands

from ooerbot.apis import reactions as crapi
from ooerbot.bot import OoerBot
from ooerbot.utils.converters import CleanMentions


class ReactionAdmin(commands.Cog):
    def __init__(self, bot: OoerBot) -> None:
        self.bot = bot

    @commands.command(aliases=('addcustreact', 'acr'))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def addreaction(self, ctx: commands.Context, trigger: str, *, response: CleanMentions) -> None:
        """Add a new reaction with a trigger and a response."""

        reaction = await crapi.create_reaction(ctx.guild.id, trigger, response)

        await ctx.send('')

    @commands.command(aliases=('editcustreact', 'ecr'))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def editreaction(self, ctx: commands.Context, reaction_id: int, *, response: CleanMentions) -> None:
        """Edits the reaction's response."""

        reaction = await crapi.update_reaction(ctx.guild.id, reaction_id, response)

        await ctx.send('')

    @commands.command(aliases=('listcustreact', 'lcr'))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def listreactions(self, ctx: commands.Context) -> None:
        """List all reactions in the guild."""

        await ctx.send('Reaction list and mass edit is now available at https://crapi.ooer.lol')

    @commands.command(aliases=('showcustreact', 'scr'))
    @commands.check_any(commands.guild_only())
    async def showreaction(self, ctx: commands.Context, reaction_id: int) -> None:
        """Shows a reaction's response."""

        reaction = await crapi.get_reaction(ctx.guild.id, reaction_id)

        await ctx.send('')

    @commands.command(aliases=('delcustreact', 'dcr'))
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def deletereaction(self, ctx: commands.Context, reaction_id: int) -> None:
        """Shows a reaction's response."""

        success = await crapi.delete_reaction(ctx.guild.id, reaction_id)

        await ctx.send('')

    @commands.command(name='crca')
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def set_contains_anywhere(self, ctx: commands.Context, reaction_id: int) -> None:
        """Toggles whether the reaction will trigger if the triggering message contains the keyword."""

        await ctx.send('')

    @commands.command(name='crdm')
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def set_dm_response(self, ctx: commands.Context, reaction_id: int) -> None:
        """Toggles whether the response of the reaction will be sent as a direct message."""

        await ctx.send('')

    @commands.command(name='crad')
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def set_delete_trigger(self, ctx: commands.Context, reaction_id: int) -> None:
        """Toggles whether the message triggering the reaction will be automatically deleted."""

        await ctx.send('')

    @commands.command(name='crat')
    @commands.check_any(
        commands.guild_only(),
        commands.has_permissions(administrator=True),
    )
    async def set_has_target(self, ctx: commands.Context, reaction_id: int) -> None:
        """
        Toggles whether the reaction will allow extra input after the trigger.
        For example, with this feature enabled,
            a reaction with trigger 'hi' will be invoked when a user types 'hi there'.
        This feature is automatically enabled on reactions which have '%target%' in their response.
        """

        await ctx.send('')


def setup(bot: OoerBot) -> None:
    bot.add_cog(ReactionAdmin(bot))
