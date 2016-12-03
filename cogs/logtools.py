import discord
from .utils import checks
from discord.ext import commands
from .utils.dataIO import fileIO
from __main__ import send_cmd_help
from time import time
import os


class LogTools:
    def __init__(self, bot):
        self.bot = bot
        self.file = 'data/logtools/{}.log'
        self.ignore_file = 'data/logtools/logtools.json'

    @commands.group(pass_context=True, no_pm=True, name='logs', aliases=['log'])
    async def _logs(self, context):
        """Retrieve logs, the slowpoke way."""
        if context.invoked_subcommand is None:
            await send_cmd_help(context)


    @_logs.command(pass_context=True, no_pm=True, name='username')
    @checks.mod_or_permissions(manage_channels=True)
    async def _username(self, context, username: discord.Member, channel: discord.Channel, number: int):
        """[mention] [channel] [number]"""
        data = fileIO(self.ignore_file, "load")
        current_server = context.message.server.id
        current_channel = channel.id
        if current_server not in data:
            data[current_server] = []
        if current_channel not in data[current_server]:
            log = []
            try:
                async for message in self.bot.logs_from(channel, limit=number):
                    author = message.author
                    if username.id == author.id:
                        content = message.clean_content
                        timestamp = str(message.timestamp)[:-7]
                        log_msg = '[{}] {} ({}): {}'.format(timestamp, author.name, author.id, content)
                        log.append(log_msg)
                try:
                    t = self.file.format(str(time()).split('.')[0])
                    with open(t, encoding='utf-8', mode="w") as f:
                        for message in log[::-1]:
                            f.write(message+'\n')
                    f.close()
                    await self.bot.send_file(context.message.channel, t)
                    os.remove(t)
                except Exception as error:
                    print(error)
            except discord.errors.Forbidden:
                await self.bot.say('Nope can\'t do, I don\'t have permission you savage!')

    @_logs.command(pass_context=True, no_pm=True, name='all')
    @checks.mod_or_permissions(manage_channels=True)
    async def _get(self, context, channel: discord.Channel, number: int):
        """[channel] [number]"""
        data = fileIO(self.ignore_file, "load")
        current_server = context.message.server.id
        current_channel = channel.id
        if current_server not in data:
            data[current_server] = []
        if current_channel not in data[current_server]:
            log = []
            try:
                async for message in self.bot.logs_from(channel, limit=number):
                    author = message.author
                    content = message.clean_content
                    timestamp = str(message.timestamp)[:-7]
                    log_msg = '[{}] {} ({}): {}'.format(timestamp, author.name, author.id, content)
                    log.append(log_msg)
                try:
                    t = self.file.format(str(time()).split('.')[0])
                    with open(t, encoding='utf-8', mode="w") as f:
                        for message in log[::-1]:
                            f.write(message+'\n')
                    f.close()
                    await self.bot.send_file(context.message.channel, t)
                    os.remove(t)
                except Exception as error:
                    print(error)
            except discord.errors.Forbidden:
                await self.bot.say('Nope can\'t do, I don\'t have permission you savage!')

    @_logs.command(pass_context=True, no_pm=True, name='roleplay', aliases=['rp'])
    @checks.mod_or_permissions(manage_channels=True)
    async def _roleplay(self, context, channel: discord.Channel, number: int):
        """[channel] [number]"""
        data = fileIO(self.ignore_file, "load")
        current_server = context.message.server.id
        current_channel = channel.id
        if current_server not in data:
            data[current_server] = []
        if current_channel not in data[current_server]:
            log = []
            try:
                async for message in self.bot.logs_from(channel, limit=number):
                    author = message.author
                    content = message.clean_content
                    timestamp = str(message.timestamp)[:-7]
                    log_msg = '[{}] {}: {}'.format(timestamp, author.name, content)
                    log.append(log_msg)

                try:
                    t = self.file.format(str(time()))
                    with open(t, encoding='utf-8', mode="w") as f:
                        for message in log[::-1]:
                            f.write(message+'\n')
                    f.close()
                    await self.bot.send_file(context.message.channel, t)
                    os.remove(t)
                except Exception as error:
                    print(error)
            except discord.errors.Forbidden:
                await self.bot.say('Nope can\'t do, I don\'t have permission you savage!')

    @_logs.command(pass_context=True, no_pm=True, name='ignore')
    @checks.mod_or_permissions(administrator=True)
    async def _ignore(self, context, channel: discord.Channel):
        """[channel]"""
        data = fileIO(self.ignore_file, "load")
        current_server = context.message.server.id
        current_channel = channel.id
        if current_server not in data:
            data[current_server] = []
        if current_channel not in data[current_server]:
            data[current_server].append(current_channel)
            message = 'Ignoring {}'.format(channel.mention)
        else:
            data[current_server].remove(current_channel)
            message = 'Unignoring {}'.format(channel.mention)

        fileIO(self.ignore_file, "save", data)
        await self.bot.say('*{}*'.format(message))

def check_folder():
    if not os.path.exists("data/logtools"):
        print("Creating data/logtools folder...")
        os.makedirs("data/logtools")

def check_file():
    data = {}
    f = "data/logtools/logtools.json"
    if not fileIO(f, "check"):
        print("Creating default logtools.json...")
        fileIO(f, "save", data)

def setup(bot):
    check_folder()
    check_file()
    n = LogTools(bot)
    bot.add_cog(n)
