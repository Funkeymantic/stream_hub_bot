import discord
from discord.ext import commands
import re

class EventLogger(commands.Cog):
    """Logs server events to designated channels without pinging members."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Logs deleted messages without pinging the user."""
        if message.guild is None or message.author.bot:
            return  # Ignore DMs or bot messages

        guild_id = message.guild.id
        config = self.bot.get_server_config(guild_id)
        if not config:
            return

        channel_id = config.get('logging', {}).get('edit_delete_channel_id')
        if not channel_id:
            return
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(
                f"🗑️ **Message Deleted** in {message.channel.mention} by `{message.author.name}#{message.author.discriminator}`:\n"
                f"**Deleted Content:** {message.content}"
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Logs edited messages but ignores embedded updates and GIF changes."""
        if before.guild is None or before.author.bot:
            return

        before_content = before.content or ""
        after_content = after.content or ""

        if before_content == after_content:
            return

        if not before_content and after_content:
            return  # Ignore link previews

        gif_regex = r"(https?:\/\/(tenor\.com|giphy\.com|media\.giphy\.com|cdn\.discordapp\.com).*\.(gif|mp4))"
        if re.match(gif_regex, before_content) and re.match(gif_regex, after_content):
            return  # Ignore GIF changes

        guild_id = before.guild.id
        config = self.bot.get_server_config(guild_id)
        if not config:
            return

        channel_id = config.get('logging', {}).get('edit_delete_channel_id')
        if not channel_id:
            return
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(
                f"✏️ **Message Edited** in {before.channel.mention} by `{before.author.name}#{before.author.discriminator}`:\n"
                f"**Before:** {before_content}\n"
                f"**After:** {after_content}"
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Logs when a member leaves the server without pinging."""
        if member.guild is None:
            return

        guild_id = member.guild.id
        config = self.bot.get_server_config(guild_id)
        if not config:
            return

        channel_id = config.get('logging', {}).get('leave_channel_id')
        if not channel_id:
            return
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(f"🚪 **{member.name}#{member.discriminator}** has left the server.")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Logs when a member is banned without pinging and notifies them via DM (if possible)."""
        config = self.bot.get_server_config(guild.id)
        if not config:
            return

        channel_id = config.get('logging', {}).get('moderation_channel_id')
        if not channel_id:
            return
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(f"⛔ **{user.name}#{user.discriminator}** has been banned from the server.")

        # Try to notify the user via DM
        try:
            await user.send(f"⚠️ You have been banned from **{guild.name}**.")
        except discord.HTTPException:
            pass  # Ignore if DMs are closed

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        """Logs when a member is kicked without pinging and notifies them via DM (if possible)."""
        config = self.bot.get_server_config(guild.id)
        if not config:
            return

        channel_id = config.get('logging', {}).get('moderation_channel_id')
        if not channel_id:
            return
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(f"⚠️ **{user.name}#{user.discriminator}** has been kicked from the server.")

        # Try to notify the user via DM
        try:
            await user.send(f"⚠️ You have been kicked from **{guild.name}**.")
        except discord.HTTPException:
            pass  # Ignore if DMs are closed

async def setup(bot):
    await bot.add_cog(EventLogger(bot))