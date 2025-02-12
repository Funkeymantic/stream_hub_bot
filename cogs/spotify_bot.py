import discord
from discord.ext import commands, tasks
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from utils.spotify_helpers import is_explicit
import asyncio

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
        self.pending_requests = {}  # Track pending song requests (keyed by message ID)

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

    @commands.command(name="addsong", help="Search for a song and add it to the playlist.")
    async def add_song(self, ctx, *, search_query: str):
        """Searches for a song by name and artist and adds it to the playlist."""

        guild_id = ctx.guild.id
        config = self.get_server_config(guild_id)

        if not config:
            return await ctx.send("❌ No configuration found for this server.")

        # Fetch Spotify settings from the server config
        playlist_id = config.get("spotify", {}).get("playlist_id")
        ban_role_id = config.get("spotify", {}).get("ban_role_id")
        mod_role_ids = config.get("spotify", {}).get("mod_role_ids", [])

        if not playlist_id:
            return await ctx.send("❌ No playlist configured for this server.")

        # Check if the user is banned
        banned_role = ctx.guild.get_role(ban_role_id)
        if banned_role and banned_role in ctx.author.roles:
            return await ctx.send("🚫 You are banned from adding songs to the playlist.")

        # Search Spotify for the song
        results = self.spotify.search(q=search_query, type="track", limit=10)

        if not results["tracks"]["items"]:
            return await ctx.send("⚠️ No matching song found on Spotify. Please provide the correct song name and artist.")

        # Extract song details and filter for an exact match
        best_match = None
        for track in results["tracks"]["items"]:
            track_name = track["name"]
            track_artists = [artist["name"].lower() for artist in track["artists"]]
            search_parts = search_query.lower().split()

            # Ensure both song name and artist appear in search results
            if all(part in track_name.lower() or part in " ".join(track_artists) for part in search_parts):
                best_match = track
                break

        if not best_match:
            return await ctx.send("⚠️ Couldn't find an exact match. Try refining your search.")

        # Extract final song details
        song_name = best_match["name"]
        artist_name = ", ".join(artist["name"] for artist in best_match["artists"])
        album_name = best_match["album"]["name"]
        duration_ms = best_match["duration_ms"]
        song_url = best_match["external_urls"]["spotify"]
        album_cover = best_match["album"]["images"][0]["url"]
        track_uri = best_match["uri"]

        # Convert duration
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        duration = f"{minutes}:{seconds:02d}"

        # Check if the song is explicit
        if is_explicit(best_match):
            # Notify mods for approval if song is explicit
            mod_channel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
            if mod_channel:
                embed = discord.Embed(
                    title="⚠️ Explicit Song Request",
                    description=f"**User:** {ctx.author.mention}\n"
                                f"**Track:** {song_name} by {artist_name}\n"
                                f"[Open in Spotify]({song_url})",
                    color=discord.Color.orange()
                )
                embed.set_footer(text=f"Track URI: {track_uri}")
                embed.set_thumbnail(url=album_cover)

                message = await mod_channel.send(embed=embed)
                self.pending_requests[message.id] = {
                    "track_uri": track_uri,
                    "user": ctx.author,
                    "playlist_id": playlist_id,
                    "mod_role_ids": mod_role_ids
                }

                # Add reactions for mod approval
                await message.add_reaction("✅")  # Approve
                await message.add_reaction("❌")  # Reject

                # Wait for mod approval or timeout
                await self.handle_request_timeout(message, ctx.author)

            return await ctx.send("⚠️ This song is explicit and is pending mod approval.")

        # Add song to playlist
        self.spotify.playlist_add_items(playlist_id, [track_uri])

        # Send confirmation message
        embed = discord.Embed(
            title=f"✅ Added to Playlist: {song_name}",
            url=song_url,
            description=f"🎤 **Artist**: {artist_name}\n🎵 **Album**: {album_name}\n⏱ **Duration**: {duration}",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=album_cover)
        embed.set_footer(text="Added to your playlist successfully!")

        await ctx.send(embed=embed)

    async def handle_request_timeout(self, message, requester):
        """Handles a pending song request timing out after 1 day."""
        try:
            await asyncio.sleep(86400)  # Wait for 24 hours

            # If the request is still pending, notify and delete it
            if message.id in self.pending_requests:
                del self.pending_requests[message.id]  # Remove from pending
                await message.channel.send(f"⏳ The song request from {requester.mention} has expired.")
                await requester.send("⚠️ Your song request has expired after 24 hours without moderator action.")
        except asyncio.CancelledError:
            pass  # Gracefully handle task cancellation

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handles mod approval or rejection of explicit songs."""
        if user.bot:
            return  # Ignore bot reactions

        message_id = reaction.message.id
        if message_id not in self.pending_requests:
            return  # Ignore unrelated messages

        guild_id = reaction.message.guild.id
        config = self.get_server_config(guild_id)
        if not config:
            return

        # Check if the user is a mod
        request = self.pending_requests[message_id]
        mod_role_ids = request["mod_role_ids"]
        if not await self.is_moderator(user, mod_role_ids):
            return  # User is not a moderator

        # Handle approval or rejection
        track_uri = request["track_uri"]
        playlist_id = request["playlist_id"]
        requester = request["user"]

        if reaction.emoji == "✅":  # Approve
            self.spotify.playlist_add_items(playlist_id, [track_uri])
            await reaction.message.channel.send(f"✅ Approved by {user.mention}. Song added to the playlist!")
            await requester.send(f"🎶 Your song has been approved and added to the playlist!")
        elif reaction.emoji == "❌":  # Reject
            await reaction.message.channel.send(f"❌ Rejected by {user.mention}. Song was not added.")
            await requester.send(f"⚠️ Your song request was rejected by a moderator.")

        # Remove the pending request
        del self.pending_requests[message_id]

async def setup(bot):
    await bot.add_cog(SpotifyCog(bot))
