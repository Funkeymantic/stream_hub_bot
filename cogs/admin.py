from discord.ext import commands
import discord
import os
import sys
import subprocess

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

        # Run git pull and restart the bot using subprocess
        try:
            # Perform git pull
            subprocess.run(["git", "pull"], check=True)

            # Restart the bot
            os.execv(sys.executable, [sys.executable, "main_bot.py"])
        except Exception as e:
            await ctx.send(f"❌ Failed to restart the bot: {e}")

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
        """Adds a role to a user."""
        await member.add_roles(role)
        await ctx.send(f"✅ Added {role.name} to {member.mention}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
