from discord.ext import commands
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        """Restarts the bot."""
        await ctx.send("🔄 Restarting the bot...")
        os.system("git pull && python main_bot.py")
        await self.bot.close()

    @commands.command(name="shutdown")
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """Shuts down the bot."""
        await ctx.send("🔴 Shutting down...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Admin(bot))
