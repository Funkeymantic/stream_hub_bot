import discord
from discord.ext import commands
import os
import asyncio
from database import init_db

class BotCore(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents.all()
        super().__init__(command_prefix=config['discord']['prefix'], intents=intents)

    async def setup_hook(self):
        await init_db()  # Initialize the database
        
        # Dynamically load all cogs from the 'cogs' directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != "__init__.py":
                cog_name = f"cogs.{filename[:-3]}"  # Remove '.py' and add package prefix
                try:
                    await self.load_extension(cog_name)
                    print(f"✅ Loaded cog: {cog_name}")
                except Exception as e:
                    print(f"❌ Failed to load cog {cog_name}: {e}")

    async def on_ready(self):
        print(f"✅ Bot {self.user} is online.")

def run_bot(config):
    bot = BotCore(config)
    bot.run(config['discord']['token'])
