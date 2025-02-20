import logging
from twitchio.ext import commands
from discord.ext import commands as discord_commands

# Set logging level to WARNING to suppress debug logs
logging.basicConfig(level=logging.WARNING)

class TwitchBot(discord_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_token = bot.configs.get('twitch', {}).get('access_token')
        self.twitch_prefix = bot.configs.get('twitch', {}).get('prefix', '!')
        self.twitch_channel = bot.configs.get('twitch', {}).get('channel')

        if not self.twitch_token or not self.twitch_channel:
            logging.error("❌ Twitch credentials not found in config!")
            return
        
        # Initialize Twitch bot instance
        self.twitch_bot = commands.Bot(
            token=self.twitch_token,
            prefix=self.twitch_prefix,
            initial_channels=[self.twitch_channel]
        )

        # Attach event handlers properly
        self.twitch_bot.event(self.event_ready)
        self.twitch_bot.event(self.event_message)

    async def event_ready(self):
        print(f"✅ Twitch bot connected as {self.twitch_bot.nick}")

    async def event_message(self, message):
        if message.echo:
            return  # Ignore bot's own messages
        if message.content.startswith(self.twitch_prefix):
            print(f"📩 Received command: {message.content}")
        await self.twitch_bot.handle_commands(message)

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.name}!")

    async def start_twitch_bot(self):
        """Starts the Twitch bot asynchronously."""
        if not self.twitch_token or not self.twitch_channel:
            logging.error("❌ Cannot start Twitch bot: Missing credentials.")
            return

        print("🚀 Starting Twitch bot...")
        try:
            await self.twitch_bot.start()
        except Exception as e:
            logging.error(f"❌ Twitch bot failed to start: {e}")

async def setup(bot):
    """Setup function for the Discord bot to load Twitch integration."""
    cog = TwitchBot(bot)
    if cog.twitch_token and cog.twitch_channel:
        bot.loop.create_task(cog.start_twitch_bot())  # Start Twitch bot asynchronously
    await bot.add_cog(cog)
