import discord
from discord.ext import commands
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException  # Fix: Correctly importing SpotifyException
import os
import asyncio
from urllib.parse import urlparse

def extract_spotify_id(spotify_url, content_type="track"):
    """Extracts the Spotify track ID from a URL and removes unnecessary parameters."""
    if "open.spotify.com" not in spotify_url:
        return spotify_url.split("?")[0].strip()  # If it's already an ID, just clean it

    parsed_url = urlparse(spotify_url)
    path_parts = parsed_url.path.split("/")

    # Validate that the URL is a proper Spotify link
    if len(path_parts) > 2 and path_parts[1] == content_type:
        track_id = path_parts[2].split("?")[0]  # Remove everything after '?'
        return track_id
    else:
        raise ValueError(f"❌ Invalid Spotify {content_type} URL.")


class SpotifyCog(commands.Cog):
    """Spotify integration for collaborative playlist management."""

    def __init__(self, bot):
        self.bot = bot
        self.spotify = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri="http://localhost:8888/callback",
                scope="playlist-modify-public playlist-modify-private user-read-playback-state"
            )
        )
        self.pending_requests = {}

    def get_server_config(self, guild_id):
        """Retrieve the config for a specific server."""
        return self.bot.get_server_config(guild_id)

    async def is_moderator(self, member, mod_role_ids):
        """Check if the user has any of the specified moderator roles."""
        for role_id in mod_role_ids:
            role = member.guild.get_role(role_id)
            if role and role in member.roles:
                return True
        return False

    @commands.command(name="addsong")
async def add_song(self, ctx, *, song_url: str):
    """Adds a song to the collaborative playlist."""
    guild_id = ctx.guild.id
    config = self.get_server_config(guild_id)

    if not config:
        return await ctx.send("❌ No configuration found for this server.")

    playlist_id = config.get("spotify", {}).get("playlist_id")
    ban_role_id = config.get("spotify", {}).get("ban_role_id")

    if not playlist_id:
        return await ctx.send("❌ No playlist configured for this server.")

    # Check if user is banned
    banned_role = ctx.guild.get_role(ban_role_id)
    if banned_role and banned_role in ctx.author.roles:
        return await ctx.send("🚫 You are banned from adding songs.")

    try:
        track_id = extract_spotify_id(song_url, content_type="track")
        track = self.spotify.track(track_id)  # ✅ Fetch track details from Spotify API
    except ValueError:
        return await ctx.send("❌ Invalid Spotify track URL or ID.")
    except SpotifyException as e:
        return await ctx.send(f"❌ Spotify error: {e}")

    # Debugging Output (Remove later)
    print(f"🎵 Extracted Track ID: {track_id}")

    # Verify if the track exists before adding
    if not track:
        return await ctx.send("❌ Could not find this track on Spotify.")

    # Add song to the playlist
    try:
        self.spotify.playlist_add_items(playlist_id, [track_id])
        await ctx.send(f"✅ Added **{track['name']}** by **{track['artists'][0]['name']}** to the playlist!")
    except SpotifyException as e:
        await ctx.send(f"❌ Failed to add song: {e}")

    async def handle_request_timeout(self, message, requester):
        """Handles a pending song request timing out after 1 day."""
        try:
            await asyncio.sleep(86400)

            if message.id in self.pending_requests:
                del self.pending_requests[message.id]
                await message.channel.send(f"⏳ The song request from {requester.mention} has expired.")
                await requester.send("⚠️ Your song request has expired after 24 hours without moderator action.")
        except asyncio.CancelledError:
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handles mod approval or rejection of explicit songs."""
        if user.bot:
            return

        message_id = reaction.message.id
        if message_id not in self.pending_requests:
            return

        guild_id = reaction.message.guild.id
        config = self.get_server_config(guild_id)
        if not config:
            return

        request = self.pending_requests[message_id]
        mod_role_ids = request["mod_role_ids"]
        if not await self.is_moderator(user, mod_role_ids):
            return

        track_id = request["track_id"]
        playlist_id = request["playlist_id"]
        requester = request["user"]

        if reaction.emoji == "✅":
            self.spotify.playlist_add_items(playlist_id, [track_id])
            await reaction.message.channel.send(f"✅ Approved by {user.mention}. Song added to the playlist!")
            await requester.send(f"🎶 Your song has been approved and added to the playlist!")
        elif reaction.emoji == "❌":
            await reaction.message.channel.send(f"❌ Rejected by {user.mention}. Song was not added.")
            await requester.send(f"⚠️ Your song request was rejected by a moderator.")

        del self.pending_requests[message_id]


async def setup(bot):
    await bot.add_cog(SpotifyCog(bot))
