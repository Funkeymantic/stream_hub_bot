import tweepy
from discord.ext import commands

class TwitterBot(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.api = tweepy.Client(bearer_token=config['bearer_token'])

    @commands.command(name="tweet")
    async def post_tweet(self, ctx, *, message):
        self.api.create_tweet(text=message)
        await ctx.send("✅ Tweet posted successfully!")

async def setup(bot):
    await bot.add_cog(TwitterBot(bot))
