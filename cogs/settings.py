
from discord import (ApplicationContext, Embed, IntegrationType,
                     InteractionContextType)
from discord.ext import commands


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='settings',
        description='Set the addresses to monitor (max 5) and other info',
        integration_types=[
            IntegrationType.user_install,
            IntegrationType.guild_install,
        ],
        contexts=[
            InteractionContextType.guild,
            InteractionContextType.bot_dm,
            InteractionContextType.private_channel,
        ],
    )
    async def settings(
        self,
        ctx: ApplicationContext
    ):
        latency = self.bot.latency
        embed = Embed(
            title='Settings',
            description=f'{latency * 1000:.2f} ms ({latency:.2f} s)',
            color=0xFFA46E
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(settings(bot))
