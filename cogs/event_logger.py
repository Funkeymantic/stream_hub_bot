import discord
from discord.ext import commands
import re

class EventLogger(commands.Cog):
    """Logs server events to designated channels."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Logs deleted messages."""
        if message.guild is None or message.author.bot:
            return  # Ignore DMs or bot messages

        # Get the config for this guild
        guild_id = message.guild.id
        config = self.bot.get_server_config(guild_id)
        if not config:
            return  # No config for this server

        # Get the edit/delete log channel
        channel_id = config.get('logging', {}).get('edit_delete_channel_id')
        if not channel_id:
            return  # No channel configured
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(
                f"🗑️ **Message Deleted** in {message.channel.mention}:\n{message.content}"
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Logs edited messages but ignores embedded updates and GIF changes."""

        if before.guild is None or before.author.bot:
            return  # Ignore DMs or bot messages

        # Ignore cases where the content hasn't changed
        if before.content == after.content:
            return  # Avoid logging if no real change occurred

        # Check if the edit only modified an embedded preview
        if not before.content and after.content:
            return  # Ignore Discord link previews

        # Ignore GIF link edits (Tenor, Giphy, etc.)
        gif_regex = r"(https?:\/\/(tenor\.com|giphy\.com|media\.giphy\.com|cdn\.discordapp\.com).*\.(gif|mp4))"
        if re.match(gif_regex, before.content or "") and re.match(gif_regex, after.content or ""):
            return  # Ignore GIF changes

        # Get the config for this guild
        guild_id = before.guild.id
        config = self.bot.get_server_config(guild_id)
        if not config:
            return  # No config for this server

        # Get the edit/delete log channel
        channel_id = config.get('logging', {}).get('edit_delete_channel_id')
        if not channel_id:
            return  # No channel configured
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(
                f"✏️ **Message Edited** in {before.channel.mention} by {member.name}:\n"
                f"**Before:** {before.content}\n"
                f"**After:** {after.content}"
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Logs when a member leaves the server."""
        if member.guild is None:
            return  # Ignore DMs or bot messages

        # Get the config for this guild
        guild_id = member.guild.id
        config = self.bot.get_server_config(guild_id)
        if not config:
            return  # No config for this server

        # Get the leave log channel
        channel_id = config.get('logging', {}).get('leave_channel_id')
        if not channel_id:
            return  # No channel configured
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(f"🚪 **Member Left:** {member.name}#{member.discriminator}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Logs when a member is banned."""
        config = self.bot.get_server_config(guild.id)
        if not config:
            return  # No config for this server

        # Get the moderation log channel
        channel_id = config.get('logging', {}).get('moderation_channel_id')
        if not channel_id:
            return  # No channel configured
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(f"⛔ **Member Banned:** {user.name}#{user.discriminator}")

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        """Logs when a member is kicked."""
        config = self.bot.get_server_config(guild.id)
        if not config:
            return  # No config for this server

        # Get the moderation log channel
        channel_id = config.get('logging', {}).get('moderation_channel_id')
        if not channel_id:
            return  # No channel configured
        log_channel = self.bot.get_channel(channel_id)

        if log_channel:
            await log_channel.send(f"⚠️ **Member Kicked:** {user.name}#{user.discriminator}")

async def setup(bot):
    await bot.add_cog(EventLogger(bot))
