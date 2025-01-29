import discord
from discord.ext import commands
from discord import app_commands

class SampleCog(commands.Cog):
    """Example cog with a slash command."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello to the bot!")
    async def hello(self, interaction: discord.Interaction):
        """Responds to a slash command `/hello`."""
        await interaction.response.send_message(f"Hello, {interaction.user.name}!")

    @app_commands.command(name="add", description="Add two numbers.")
    async def add(self, interaction: discord.Interaction, a: int, b: int):
        """Adds two numbers provided as slash command arguments."""
        result = a + b
        await interaction.response.send_message(f"The sum of {a} and {b} is {result}!")

async def setup(bot):
    await bot.add_cog(SampleCog(bot))
