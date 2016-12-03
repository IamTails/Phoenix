from discord.ext import commands
from cogs.utils.dataIO import fileIO
from cogs.utils import checks
import os
import copy


class ChannelLogger(object):
    """docstring for ChannelLogger"""

    def __init__(self, bot):
        super(ChannelLogger, self).__init__()
        self.bot = bot

        self.channels = fileIO("data/channellogger/channels.json", "load")

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def channellogger(self, ctx):
        """Toggles logging for a channel"""
        channel = ctx.message.channel
        if channel.id not in self.channels:
            self.channels[channel.id] = True
        else:
            self.channels[channel.id] = not self.channels[channel.id]
        if self.channels[channel.id]:
            await self.bot.say('Logging enabled'
                               ' for {}'.format(channel.mention))
        else:
            await self.bot.say('Logging disabled'
                               ' for {}'.format(channel.mention))
        self.save_channels()

    def save_channels(self):
        fileIO('data/channellogger/channels.json', 'save', self.channels)

    def log(self, message):
        serverid = message.server.id
        channelid = message.channel.id
        if not os.path.exists('data/channellogger/{}'.format(serverid)):
            os.mkdir('data/channellogger/{}'.format(serverid))
        fname = 'data/channellogger/{}/{}.log'.format(serverid, channelid)
        with open(fname, 'a', errors='backslashreplace') as f:
            message = ("{0.timestamp} #{1.name} @{2.name}#{2.discriminator}: "
                       "{0.clean_content}\n".format(message, message.channel,
                                                    message.author))
            f.write(message)

    async def message_logger(self, message):
        enabled = self.channels.get(message.channel.id, False)
        if enabled:
            self.log(message)

    async def message_edit_logger(self, before, after):
        new_message = copy.deepcopy(after)
        new_content = ("EDIT: \nBefore: "
                       "{}\nAfter: {}".format(before.clean_content,
                                              after.clean_content))
        new_message.content = new_content
        await self.message_logger(new_message)


def check_folders():
    if not os.path.exists("data/channellogger"):
        os.mkdir("data/channellogger")


def check_files():
    if not os.path.exists("data/channellogger/channels.json"):
        fileIO("data/channellogger/channels.json", "save", {})


def setup(bot):
    check_folders()
    check_files()
    n = ChannelLogger(bot)
    bot.add_cog(n)
    bot.add_listener(n.message_logger, "on_message")
    bot.add_listener(n.message_edit_logger, 'on_message_edit')
