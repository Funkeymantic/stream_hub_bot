from twitchio.ext import commands

class TwitchBot(commands.Bot):
    def __init__(self, token, prefix, channel):
        super().__init__(token=token, prefix=prefix, initial_channels=[channel])

    async def event_ready(self):
        print(f"Twitch bot connected as {self.nick}")

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.name}!")

async def setup(bot):
    await bot.add_cog(TwitchBot(bot))
