import asyncio

import disnake
from disnake.ext import commands


class Pinglimit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pinglimit(self, ctx):
        start = 9
        end = 11

        await ctx.send("Starting in 3secs...")
        await asyncio.sleep(3)

        for x in range(start, end + 1):
            await ctx.send(
                f"{x} - " + "<@850336994299215892> " * x + ctx.author.mention
            )
            await asyncio.sleep(3)


def setup(client):
    client.add_cog(Pinglimit(client))
