import json
from pathlib import Path

import tekore as tk
from discord import Embed
from discord.ext import commands

cwd = Path(__file__).cwd()
cwd = str(cwd)

hiding = json.load(open(cwd + '/hiding.json'))
client_id = hiding['client_id']
client_secret = hiding['client_secret']
token_spotify = tk.request_client_token(client_id=client_id,
                                        client_secret=client_secret)
spotify = tk.Spotify(token_spotify,
                     asynchronous=True)


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command(aliases=['tk'])
    async def track(self, ctx, *, query: str = None):
        if query is None:
            await ctx.send("No search query specified")
            await ctx.send("The command should look like this ```$ track [Name] ```")
            return
        tracks, = await spotify.search(query, limit=5)

        embed = Embed(title="Track search results", color=0x921030)
        embed.set_thumbnail(url="https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png")
        embed.set_footer(text="Requested by " + ctx.author.display_name)
        for t in tracks.items:
            artist = t.artists[0].name
            url = t.external_urls["spotify"]

            message = "\n".join([
                f"[Open on Spotify](" + url + ")",
                ":musical_note: " + artist,
                ":star: " + t.album.name
            ])
            embed.add_field(name=t.name, value=message, inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Spotify(bot))
