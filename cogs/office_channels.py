import discord
from discord.ext import commands
from db_utils import add_house, get_house_by_name, add_key, remove_key

class OfficeChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_house")
@commands.has_permissions(administrator=True)
async def create_house(self, ctx, house_name: str, member: discord.Member):
    """Creates a house (text and voice channels) for the given user."""
    existing_house = await get_house_by_name(house_name)
    if existing_house:
        await ctx.send(f"⚠️ A house named `{house_name}` already exists!")
        return

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="Houses") or await guild.create_category("Houses")

    # Error handling for permission issues
    try:
        text_channel = await category.create_text_channel(house_name)
        voice_channel = await category.create_voice_channel(house_name)
        role_name = f"{house_name} 🔑"
        role = await guild.create_role(name=role_name)
        await member.add_roles(role)

        await text_channel.set_permissions(role, read_messages=True, send_messages=True)
        await voice_channel.set_permissions(role, connect=True, speak=True)

        await add_house(house_name, member.id, text_channel.id, voice_channel.id)
        await ctx.send(f"🏠 House `{house_name}` created successfully for {member.mention}.")
    except discord.Forbidden:
        await ctx.send("⚠️ I do not have permission to create channels or roles. Please check my role permissions.")


    @commands.command(name="give_key")
    async def give_key(self, ctx, member: discord.Member):
        """Gives the specified user access to the current house."""
        house = await get_house_by_name(ctx.channel.name)
        if house:
            role = discord.utils.get(ctx.guild.roles, name=f"{house.name} 🔑")
            if role:
                await member.add_roles(role)
                await add_key(house.id, member.id, role.id)
                await ctx.send(f"🔑 {member.mention} now has access to `{house.name}`.")
            else:
                await ctx.send("⚠️ Role not found. Please check the house name.")
        else:
            await ctx.send("⚠️ No house associated with this channel.")

    @commands.command(name="take_key")
    async def take_key(self, ctx, member: discord.Member):
        """Removes the specified user's access from the current house."""
        house = await get_house_by_name(ctx.channel.name)
        if house:
            role = discord.utils.get(ctx.guild.roles, name=f"{house.name} 🔑")
            if role and role in member.roles:
                await member.remove_roles(role)
                await remove_key(member.id)
                await ctx.send(f"🔐 {member.mention} no longer has access to `{house.name}`.")
            else:
                await ctx.send("⚠️ User does not have access to this house.")
        else:
            await ctx.send("⚠️ No house associated with this channel.")

async def setup(bot):
    await bot.add_cog(OfficeChannels(bot))
