import disnake
from disnake.ext import commands


class Cog_Name_Here(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stuff(self, ctx, arg):
        await ctx.send(arg)


def setup(client):
    client.add_cog(Cog_Name_Here(client))
