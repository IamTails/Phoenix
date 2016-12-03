from __main__ import send_cmd_help
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
import discord

class MessageEconomy:
    """A cog for rewarding active users."""
    def __init__(self, bot):
        self.bot = bot
        self.economy = self.bot.get_cog("Economy")
        try:
            self.db = dataIO.load_json("./data/message_economy.json")
        except FileNotFoundError:
            self.db = {}

    def save(self):
        dataIO.save_json("./data/message_economy.json", self.db)

    def create_if_not_exist(self, server):
        server = server.id
        if server not in self.db:
            self.db[server] = {}
            self.db[server]["credits"] = 1
            self.db[server]["channels"] = []

    @checks.admin_or_permissions(manage_channels=True)
    @commands.group(name="msgeset", pass_context=True)
    async def set_cmd(self, ctx):
        """Manages MessageEconomy-related settings."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @checks.admin_or_permissions(manage_channels=True)
    @set_cmd.command(pass_context=True)
    async def toggle(self, ctx, channel: discord.Channel):
        """Adds/removes the channel to/from the MessageEconomy list."""
        self.create_if_not_exist(ctx.message.server)
        if channel.id not in self.db[ctx.message.server.id]["channels"]:
            self.db[ctx.message.server.id]["channels"].append(channel.id)
            self.save()
            await self.bot.say("Channel added!")
        else:
            self.db[ctx.message.server.id]["channels"].remove(channel.id)
            self.save()
            await self.bot.say("Channel removed!")

    @checks.admin_or_permissions(manage_channels=True)
    @set_cmd.command(pass_context=True)
    async def credits(self, ctx, credits: int):
        """Sets the amount of credits you receive per message."""
        self.create_if_not_exist(ctx.message.server)
        self.db[ctx.message.server.id]["credits"] = credits
        self.save()
        await self.bot.say("Credits for this server set to {0}!".format(credits))

    async def process_message(self, message):
        channel = message.channel.id
        server = message.server.id
        self.create_if_not_exist(message.server)
        if channel not in self.db[server]["channels"]:
            pass
        else:
            if self.economy.bank.account_exists(message.author):
                self.economy.bank.deposit_credits(message.author, self.db[server]["credits"])
                self.save()


def setup(bot):
    n = MessageEconomy(bot)
    bot.add_listener(n.process_message, "on_message")
    bot.add_cog(n)
