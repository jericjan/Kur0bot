import asyncio
from typing import Any

import disnake
from disnake.ext import commands


class Pinglimit(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def pinglimit(self, ctx: commands.Context[Any]):
        start = 9
        end = 11

        await ctx.send("Starting in 3secs...")
        await asyncio.sleep(3)

        for x in range(start, end + 1):
            await ctx.send(
                f"{x} - " + "<@850336994299215892> " * x + ctx.author.mention
            )
            await asyncio.sleep(3)


def setup(client: commands.Bot):
    client.add_cog(Pinglimit(client))
