import discord
from discord.ext import commands
import os

class BotCore(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.messages = True
        intents.message_content = True  # Important for command processing

        super().__init__(command_prefix=config['discord']['prefix'], intents=intents)
        self.config = config

    async def on_ready(self):
        print(f"✅ Bot {self.user} is online and ready!")
        for cog in self.cogs:
            print(f"✅ Loaded cog: {cog}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f"DEBUG: Received message - {message.content}")
        await self.process_commands(message)

    async def setup_hook(self):
        # Load cogs dynamically
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    print(f"✅ Loaded cog: {cog_name}")
                except Exception as e:
                    print(f"❌ Failed to load cog {cog_name}: {e}")

async def run_bot(config):
    bot = BotCore(config)
    await bot.start(config['discord']['token'])
