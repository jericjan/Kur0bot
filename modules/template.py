# type: ignore
from typing import Any

import disnake
from disnake.ext import commands


class Cog_Name_Here(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def stuff(self, ctx: commands.Context[Any], arg):
        await ctx.send(arg)


def setup(client: commands.Bot):
    client.add_cog(Cog_Name_Here(client))
