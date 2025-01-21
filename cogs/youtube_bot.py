from googleapiclient.discovery import build
from discord.ext import commands
import os

class YouTubeBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("YOUTUBE_API_KEY")

    @commands.command(name="yt_latest")
    async def youtube_latest(self, ctx, channel_id: str):
        """Fetch the latest video from a given YouTube channel ID."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)

        try:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                maxResults=1
            )
            response = request.execute()

            if response['items']:
                video_id = response['items'][0]['id']['videoId']
                video_title = response['items'][0]['snippet']['title']
                await ctx.send(f"📺 Latest video: {video_title} - https://youtube.com/watch?v={video_id}")
            else:
                await ctx.send("⚠️ No videos found for this channel.")
        except Exception as e:
            await ctx.send("⚠️ Failed to fetch video. Check your API key and channel ID.")
            print(f"Error fetching video: {e}")

async def setup(bot):
    await bot.add_cog(YouTubeBot(bot))
