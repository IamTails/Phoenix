from __main__ import send_cmd_help
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils import chat_formatting
import discord
import inspect
import subprocess
import sys


class HelpfulUtils:
    def __init__(self, bot):
        self.bot = bot
        self.version = "2016-09-16 v.1"
        try:
            self.config = dataIO.load_json("./data/helpful_utils.json")  # because this cog only uses one json file,
            # I might as well just store it in ./data
        except FileNotFoundError:
            dataIO.save_json("./data/helpful_utils.json", {})
            self.config = dataIO.load_json("./data/helpful_utils.json")
        if "void_warranty" not in self.config:  # because people are fucking idiots T_T
            self.config["void_warranty"] = False
            self.save_db()

    def save_db(self):
        dataIO.save_json("./data/helpful_utils.json", self.config)

    @checks.is_owner()
    @commands.group(name="utils", pass_context=True, invoke_without_command=True)
    async def group_cmd(self, ctx):
        """A bunch of useful commands all in one!"""
        await send_cmd_help(ctx)

    @checks.is_owner()
    @group_cmd.command()
    async def ping(self):
        """Check if your bot is responding."""
        await self.bot.say("All critical systems functional.")

    @checks.is_owner()
    @group_cmd.command(name="listcogs")
    async def list_cogs(self):
        """A command to list the currently active cogs."""
        cogs = dataIO.load_json("data/red/cogs.json")

        # So IDEA shuts up:
        # noinspection PyProtectedMember
        existing_cogs = self.bot.cogs['Owner']._list_cogs()
        enabled_cogs = []
        disabled_cogs = []

        for cog in cogs:
            if cogs.get(cog) and cog in existing_cogs:
                enabled_cogs.append(cog)
            elif cog in existing_cogs:
                disabled_cogs.append(cog)

        enabled_str = "Enabled cogs:"

        for cog in sorted(enabled_cogs):
            enabled_str = enabled_str + "\n+ " + str(cog)

        disabled_str = "Disabled cogs:"

        for cog in sorted(disabled_cogs):
            disabled_str = disabled_str + "\n- " + str(cog)

        assembled_str = "```diff\n" + enabled_str + "\n\n" + disabled_str + "```"

        await self.bot.say(assembled_str)

    @checks.is_owner()
    @group_cmd.command()
    async def update(self, hard: bool=False):
        """Update the bot. Defaults to regular git pull."""
        if sys.platform == "linux":
            if not hard:
                command = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + output + "```")
                if "Already up-to-date." not in output:
                    await self.bot.say("I recommend restarting your bot now to apply the changes.")
            else:
                command = subprocess.Popen(["git", "fetch --force"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + output + "```")
                command = subprocess.Popen(["git", "reset --hard"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + output + "```")
                command = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + str(output) + "```")
        else:
            await self.bot.say("Incompatible OS. This usually means you are running Windows, which does not allow "
                               "for files to be changed while they are open.")

    @checks.is_owner()
    @group_cmd.command(pass_context=True)
    async def terminal(self, ctx, *, command: str=None):
        """Run a terminal command."""
        # ENGAGE IDIOT PROOFING 101
        if self.config["void_warranty"]:
            if command is not None:
                command = command.replace("`", "")
                command = command.split()
                command_run = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command_run.stdout.read().decode()
                paged = chat_formatting.pagify(output, delims="\n")
                for page in paged:
                    await self.bot.say("```{0}```".format(page))
            else:
                await self.bot.say("You *do* realize you need to enter a command, right?")
        else:
            await self.bot.say("**This might void your warranty!**\n"
                               "Changing these advanced settings can be harmful to the stability, security, "
                               "and performance of this application. You should only continue if you are sure "
                               "of what you are doing.\n"
                               "\n"
                               "Type \"I accept the risk!\" to continue.")
            answer = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if answer.content.lower() == "i accept the risk!":
                self.config["void_warranty"] = True
                self.save_db()
                await self.bot.say("Your warranty is now void.")
            else:
                await self.bot.say("Not enabling advanced settings.")

    @checks.is_owner()
    @group_cmd.command(name="listprefixes")
    async def list_prefixes(self):
        """List the bot's prefixes."""
        prefixes = ""
        for i in self.bot.command_prefix:
            prefixes += "\"" + i + "\" "
        await self.bot.say("My current prefixes: {0}".format(prefixes))

    @group_cmd.command(name="version")
    async def version_cmd(self):
        """Check the helpful utils version."""
        await self.bot.say("I am currently running helpful utils version {0}.".format(self.version))

    @checks.is_owner()
    @group_cmd.command()
    async def unvoid(self):
        """Unvoids your warranty."""
        if self.config["void_warranty"]:
            self.config["void_warranty"] = False
            self.save_db()
            await self.bot.say("Warranty unvoided.")
        else:
            await self.bot.say("Your warranty isn't void!")

    @checks.is_owner()
    @group_cmd.group(name="perms", pass_context=True, invoke_without_command=True)
    async def perms_cmd(self, ctx):
        """Commands related to managing permissions."""
        await send_cmd_help(ctx)

    @checks.is_owner()
    @perms_cmd.command(name="calc")
    async def perms_calc(self, bitwise: int):
        """A permissions calculator."""
        machine_permissions = inspect.getmembers(discord.permissions.Permissions(bitwise))
        human_permissions = {}
        for i in machine_permissions:
            if i[1] is True or i[1] is False:
                human_permissions[i[0]] = i[1]
        human_readable_permissions = ""
        for i in sorted(human_permissions):
            if human_permissions[i]:
                human_readable_permissions += "\n:ballot_box_with_check: - " + i
            else:
                human_readable_permissions += "\n:negative_squared_cross_mark: - " + i
        await self.bot.say(human_readable_permissions)

    @checks.is_owner()
    @perms_cmd.command(name="get")
    async def perms_get(self, user: discord.Member, channel: discord.Channel):
        """Gets permissions for the user in the specified channel."""
        filter = ['speak', 'use_voice_activation', 'mute_members', 'move_members', 'deafen_members', 'connect']
        machine_permissions = inspect.getmembers(user.permissions_in(channel))
        human_permissions = {}
        for i in machine_permissions:
            if i[0] not in filter:
                if i[1] is True or i[1] is False:
                    human_permissions[i[0]] = i[1]
        human_readable_permissions = ""
        for i in sorted(human_permissions):
            if human_permissions[i]:
                human_readable_permissions += "\n:ballot_box_with_check: - " + i
            else:
                human_readable_permissions += "\n:negative_squared_cross_mark: - " + i
        await self.bot.say(human_readable_permissions)


def setup(bot):
    n = HelpfulUtils(bot)
    bot.add_cog(n)
