from discord.ext import commands

class EventLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            log_channel = self.bot.get_channel(YOUR_LOG_CHANNEL_ID)
            await log_channel.send(f"✏️ Message edited in {before.channel}: {before.content} -> {after.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(YOUR_LOG_CHANNEL_ID)
        await log_channel.send(f"🗑️ Message deleted in {message.channel}: {message.content}")

async def setup(bot):
    await bot.add_cog(EventLogger(bot))
