import discord
from discord.ext import commands, tasks
import aiohttp
import os

class LiveNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.own_channel_id = int(os.getenv("OWN_CHANNEL_ID"))
        self.performance_channel_id = int(os.getenv("PERFORMANCE_CHANNEL_ID"))
        self.performance_role_name = "Performance Check"
        self.token = None
        self.streamers = {}
        self.live_messages = {}
        self.check_streamers.start()

    async def cog_load(self):
        await self.refresh_twitch_users()
        print("[LiveNotifier] Cog loaded and stream check started.")

    async def get_twitch_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.twitch_client_id,
            "client_secret": self.twitch_client_secret,
            "grant_type": "client_credentials"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    self.token = data["access_token"]

    async def refresh_twitch_users(self):
        guild = self.bot.guilds[0]  # Assuming single guild
        role = discord.utils.get(guild.roles, name=self.performance_role_name)
        if role:
            self.streamers = {member.display_name: member for member in role.members}

    async def check_if_live(self, streamer_name):
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": self.twitch_client_id,
            "Authorization": f"Bearer {self.token}"
        }
        params = {"user_login": streamer_name}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                return bool(data.get("data"))

    @tasks.loop(minutes=5)
    async def check_streamers(self):
        if not self.token:
            await self.get_twitch_token()
        await self.refresh_twitch_users()

        for streamer_name, member in self.streamers.items():
            is_live = await self.check_if_live(streamer_name)

            channel_id = self.own_channel_id if streamer_name.lower() == "funkeymantic" else self.performance_channel_id
            channel = self.bot.get_channel(channel_id)

            if is_live:
                if streamer_name not in self.live_messages and channel:
                    message = await channel.send(f"{streamer_name} is now live! https://twitch.tv/{streamer_name}")
                    self.live_messages[streamer_name] = message.id
            else:
                if streamer_name in self.live_messages and channel:
                    try:
                        message = await channel.fetch_message(self.live_messages.pop(streamer_name))
                        await message.delete()
                    except discord.NotFound:
                        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(LiveNotifier(bot))
