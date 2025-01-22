import logging
from twitchio.ext import commands

# Replace with your Twitch credentials
TOKEN = "4c9q2appj21qtihhk5iroonnrfae6y"
CHANNEL = "Funkeymantic"

bot = commands.Bot(
    token=TOKEN,
    prefix="!",
    initial_channels=[CHANNEL]
)

@bot.event
async def event_ready():
    print(f"✅ Connected to Twitch as {bot.nick}")

@bot.event
async def event_message(message):
    print(f"📩 Twitch message received: {message.content}")
    await bot.handle_commands(message)

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.name}!")

try:
    bot.run()
except Exception as e:
    print(f"❌ Error starting Twitch bot: {e}")
