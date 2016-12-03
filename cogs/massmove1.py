import discord
from discord.ext import commands
from .utils import checks
import asyncio
import logging
log = logging.getLogger('red.massmove')


class Massmove:
    """Massmove users to another voice channel"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def massmove(self, ctx, from_channel: discord.Channel, to_channel: discord.Channel):
        """Massmove users to another voice channel"""
        # check if channels are voice channels. Or moving will be very... interesting...
        type_from = str(from_channel.type)
        type_to = str(to_channel.type)
        if type_from == 'text':
            await self.bot.say('{} is not a valid voice channel'.format(from_channel.name))
            log.debug('SID: {}, from_channel not a voice channel'.format(from_channel.server.id))
        elif type_to == 'text':
            await self.bot.say('{} is not a valid voice channel'.format(to_channel.name))
            log.debug('SID: {}, to_channel not a voice channel'.format(to_channel.server.id))
        else:
            try:
                log.debug('Starting move on SID: {}'.format(from_channel.server.id))
                log.debug('Getting copy of current list to move')
                voice_list = list(from_channel.voice_members)
                msg = ctx.message
                await self.bot.delete_message(msg)
                for member in voice_list:
                    await self.bot.move_member(member, to_channel)
                    log.debug('Member {} moved to channel {}'.format(member.id, to_channel.id))
                    await asyncio.sleep(0.05)
            except discord.Forbidden:
                await self.bot.say('I have no permission to move members.')
            except discord.HTTPException:
                await self.bot.say('A error occured. Please try again')

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def massadd(self, ctx):
        """yup"""
        await self.bot.say("Adding everyone to role 'Members', please wait!")
        role = discord.utils.get(ctx.message.server.roles, name="Members")
        for member in ctx.message.server.members:
            await self.bot.add_roles(member, role)
        await self.bot.say("Finished Adding Roles!")

def setup(bot):
    n = Massmove(bot)
    bot.add_cog(n)
