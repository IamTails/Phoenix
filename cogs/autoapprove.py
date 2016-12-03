from discord.ext import commands
from cogs.utils.dataIO import fileIO
from cogs.utils import checks
from __main__ import send_cmd_help
import urllib.parse as up
import os
import json
import aiohttp


class AutoApprove:
    """Let's bypass the dumb manage_server requirements"""

    def __init__(self, bot):
        self.bot = bot
        self.base_api_url = "https://discordapp.com/api/oauth2/authorize?"
        self.enabled = fileIO('data/autoapprove/enabled.json', 'load')
        self.session = aiohttp.ClientSession()

    def __unload(self):
        self.session.close()

    def save_enabled(self):
        fileIO('data/autoapprove/enabled.json', 'save', self.enabled)

    @commands.group(no_pm=True, pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def autoapprove(self, ctx):
        server = ctx.message.server
        channel = ctx.message.channel
        me = server.me
        if not channel.permissions_for(me).manage_messages:
            await self.bot.say("I don't have manage_messages permissions."
                               " I do not recommend submitting your "
                               "authorization key until I do.")
            return
        if not channel.permissions_for(me).manage_server:
            await self.bot.say("I do not have manage_server. This cog is "
                               "useless until I do.")
            return
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @autoapprove.command(no_pm=True, pass_context=True, name="toggle")
    @checks.serverowner_or_permissions(manage_server=True)
    async def _autoapprove_toggle(self, ctx):
        server = ctx.message.server
        if server.id not in self.enabled:
            await self.bot.say('AutoApprove not set up for this server.')
        else:
            self.enabled[server.id]["ENABLED"] = \
                not self.enabled[server.id]["ENABLED"]
            self.save_enabled()
            if self.enabled[server.id]["ENABLED"]:
                await self.bot.say("AutoApprove enabled.")
            else:
                await self.bot.say("AutoApprove disabled.")

    @autoapprove.command(no_pm=True, pass_context=True, name="setup")
    @checks.serverowner_or_permissions(manage_server=True)
    async def _autoapprove_setup(self, ctx, authorization_key):
        """You will need to submit the user Authorization header key
            (can be found using dev tools in Chrome) of some user that will
            always have manage_server on this server."""
        server = ctx.message.server
        if server.id not in self.enabled:
            self.enabled[server.id] = {"ENABLED": False}
        self.enabled[server.id]['KEY'] = authorization_key
        self.save_enabled()
        await self.bot.delete_message(ctx.message)
        await self.bot.say('Key saved. Deleted message for security.'
                           ' Use `autoapprove toggle` to enable.')

    @commands.command(no_pm=True, pass_context=True)
    async def addbot(self, ctx, oauth_url):
        """Requires your OAUTH2 URL to automatically approve your bot to
            join"""
        server = ctx.message.server
        if server.id not in self.enabled:
            await self.bot.say('AutoApprove not set up for this server.'
                               ' Let the server owner know if you think it'
                               ' should be.')
            return
        elif not self.enabled[server.id]['ENABLED']:
            await self.bot.say('AutoApprove not enabled for this server.'
                               ' Let the server owner know if you think it'
                               ' should be.')
            return

        key = self.enabled[server.id]['KEY']
        parsed = up.urlparse(oauth_url)
        queryattrs = up.parse_qs(parsed.query)
        queryattrs['client_id'] = int(queryattrs['client_id'][0])
        queryattrs['scope'] = queryattrs['scope'][0]
        queryattrs.pop('permissions', None)
        full_url = self.base_api_url + up.urlencode(queryattrs)
        status = await self.get_bot_api_response(full_url, key, server.id)
        if status < 400:
            await self.bot.say("Succeeded!")
        else:
            await self.bot.say("Failed, error code {}. ".format(status))

    async def get_bot_api_response(self, url, key, serverid):
        data = {"guild_id": serverid, "permissions": 0, "authorize": True}
        data = json.dumps(data).encode('utf-8')
        headers = {'authorization': key, 'content-type': 'application/json'}
        async with self.session.post(url, data=data, headers=headers) as r:
            status = r.status
        return status


def check_folder():
    if not os.path.exists("data/autoapprove"):
        print("Creating data/autoapprove folder...")
        os.makedirs("data/autoapprove")


def check_file():
    enabled = {}

    f = "data/autoapprove/enabled.json"
    if not fileIO(f, "check"):
        print("Creating default autoapprove's enabled.json...")
        fileIO(f, "save", enabled)


def setup(bot):
    check_folder()
    check_file()
    n = AutoApprove(bot)
    bot.add_cog(n)
