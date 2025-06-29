import json
from typing import Any, Optional

import disnake
from disnake.ext import commands


class Hall_Of_Shame(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def hallofshame(self, ctx: commands.Context[Any], channel_str: Optional[str]=None):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return
        
        hall_of_shame_json = json.load(open("modules/others/hall_of_shame_ids.json"))
        if channel_str == None:
            await ctx.send("Give the channel ID for the hall of shame.")
            return
        elif channel_str == "remove" or channel_str == "delete":
            await ctx.send(f"<#{hall_of_shame_json[str(ctx.guild.id)]}> removed.")
            hall_of_shame_json.pop(str(ctx.guild.id))
        else:
            converter = commands.TextChannelConverter()
            try:
                channel = await converter.convert(ctx, channel_str)  # pyright: ignore[reportUnknownMemberType]
            except commands.ChannelNotFound:
                await ctx.send(f"Dawg. {channel_str} ain't a channel.")
                return
            em = disnake.Embed(
                title="The Hall Of Shame",
                description="These are the 10 recent players who have committed the cringe AKA playing league.",
            )
            new_embed = await channel.send(embed=em)
            hall_of_shame_json[str(ctx.guild.id)] = {}
            hall_of_shame_json[str(ctx.guild.id)]["channel-id"] = channel.id
            hall_of_shame_json[str(ctx.guild.id)]["embed-id"] = new_embed.id
            await ctx.send(f"<#{channel.id}> is now the Hall Of Shame!")
        with open("modules/others/hall_of_shame_ids.json", "w") as f:
            f.write(json.dumps(hall_of_shame_json))


def setup(client: commands.Bot):
    client.add_cog(Hall_Of_Shame(client))
