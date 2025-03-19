import discord
from discord.ext import commands
from utils.discord_helpers import to_fancy_font

class OfficeManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createhouse(self, ctx, house_name: str, member: discord.Member):
        guild = ctx.guild

        # Convert house name to fancy font
        fancy_house_name = to_fancy_font(house_name)

        # Use self.bot.config to get configuration values
        category_id = self.bot.config['office_channels']['category_id']

        # Check if category exists using ID
        category = discord.utils.get(guild.categories, id=category_id)
        if not category:
            return await ctx.send("⚠️ Category not found. Please configure the correct ID in the bot config.")

        # Create voice channel with fancy font name
        voice_channel = await guild.create_voice_channel(fancy_house_name, category=category)

        # Create a role with fancy font
        fancy_role_name = to_fancy_font(f"{house_name} Key")
        office_role = await guild.create_role(name=fancy_role_name)

        # Assign the role to the mentioned user
        await member.add_roles(office_role)
        
        # Set channel permissions using role and channel IDs
        await voice_channel.set_permissions(member, overwrite=discord.PermissionOverwrite(manage_channels=True, view_channel=True, connect=True, speak=True, USE_VAD=True))
        await voice_channel.set_permissions(guild.default_role, overwrite=discord.PermissionOverwrite(view_channel=False, connect=False))

        mod_role_id = self.bot.config['office_channels']['mod_role_id']
        mod_role = guild.get_role(mod_role_id)
        if mod_role:
            await voice_channel.set_permissions(mod_role, overwrite=discord.PermissionOverwrite(manage_channels=True, view_channel=True))

        await ctx.send(f"🏠 House `{fancy_house_name}` has been created for {member.mention}!")

async def setup(bot):
    await bot.add_cog(OfficeManagement(bot))
