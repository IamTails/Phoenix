import discord
from cogs.utils import checks
from discord.ext import commands


class SendMsg:
    """Say stuff wherever. Owner only."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command()
    async def sendmsg(self, destination: discord.Channel, content: str):
        """Say stuff wherever"""

        await self.bot.send_message(destination, content)


def setup(bot):
    bot.add_cog(SendMsg(bot))
