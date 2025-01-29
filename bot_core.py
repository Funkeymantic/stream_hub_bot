import os
import json
from discord.ext import commands


class BotCore(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        self.configs = {}

    async def setup_hook(self):
        """Load cogs and server-specific configurations."""
        await self.load_all_configs()  # Load configs dynamically

        # Dynamically load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    print(f"✅ Loaded cog: {cog_name}")
                except Exception as e:
                    print(f"❌ Failed to load cog {cog_name}: {e}")

    async def load_all_configs(self):
        """Load all JSON configs for servers."""
        self.configs = {}  # Clear current configs
        for file in os.listdir('./configs'):
            if file.endswith('.json'):
                with open(f'./configs/{file}', 'r') as f:
                    config = json.load(f)
                    server_id = str(config.get('discord', {}).get('guild_id'))
                    if server_id:
                        self.configs[server_id] = config
        print("✅ All server configurations loaded.")

    def get_server_config(self, guild_id):
        """Retrieve the config for a specific server."""
        return self.configs.get(str(guild_id), None)
