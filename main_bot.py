import os
from dotenv import load_dotenv
from bot_core import BotCore
import discord
import json

# Load environment variables from .env
load_dotenv()

# Load sensitive credentials from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = BotCore(command_prefix="~", intents=intents)

# Run the bot
if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ DISCORD_TOKEN not found in environment variables!")


async def main():
    config_files = [f for f in os.listdir('configs') if f.endswith('.json')]
    if not config_files:
        print("⚠️ No config files found in 'configs' directory.")
        return

    for config_file in config_files:
        with open(f'configs/{config_file}') as f:
            config = json.load(f)
            print(f"📄 Loaded config: {config_file}")
            await run_bot(config)

if __name__ == "__main__":
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ ERROR: DISCORD_TOKEN not found in environment variables!")