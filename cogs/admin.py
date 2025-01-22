from discord.ext import commands
import discord
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):
        await ctx.send("Test successful!")

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
    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command(name="addrole")
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"Added {role.name} to {member.mention}")

        
async def setup(bot):
    await bot.add_cog(Admin(bot))
