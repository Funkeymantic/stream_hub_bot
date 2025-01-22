import logging
from twitchio.ext import commands
from discord.ext import commands as discord_commands

# Change logging to WARNING level to hide detailed debug logs
logging.basicConfig(level=logging.WARNING)

class TwitchBot(discord_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Read Twitch credentials from bot config
        self.twitch_token = bot.config['twitch']['access_token']
        self.twitch_prefix = bot.config['twitch'].get('prefix', '!')
        self.twitch_channel = bot.config['twitch']['channel']

        # Initialize Twitch bot instance
        self.twitch_bot = commands.Bot(
            token=self.twitch_token,
            prefix=self.twitch_prefix,
            initial_channels=[self.twitch_channel]
        )

    async def event_ready(self):
        print(f"✅ Twitch bot connected as {self.twitch_bot.nick}")

    async def event_message(self, message):
        if message.content.startswith(self.twitch_prefix):
            print(f"📩 Received command: {message.content}")
        await self.twitch_bot.handle_commands(message)

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.name}!")

    async def start_twitch_bot(self):
        print("🚀 Starting Twitch bot...")
        try:
            await self.twitch_bot.start()
        except Exception as e:
            logging.error(f"❌ Twitch bot failed to start: {e}")

async def setup(bot):
    cog = TwitchBot(bot)
    bot.loop.create_task(cog.start_twitch_bot())  # Run Twitch bot asynchronously
    await bot.add_cog(cog)
