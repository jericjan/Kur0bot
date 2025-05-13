import random
from typing import Any, TYPE_CHECKING

from disnake.ext import commands

from modules.events import sus_replies
if TYPE_CHECKING:
    from main import MyBot

class Sus(commands.Cog):
    def __init__(self, client: "MyBot"):
        self.client = client

    @commands.command()
    async def bulk(self, ctx: commands.Context[Any], number: int):
        print(ctx.channel.id)
        if (channel_name := getattr(ctx.channel, "name", None)) is None:
            await ctx.send("This command can only be used in text channels.")
            return
        if channel_name == "sus-town":
            for _ in range(int(number)):
                await ctx.send(random.choice(sus_replies))
        else:
            await ctx.send(
                "Only usable in channels named `sus-town` <:sus:850628234746920971>"
            )

    @commands.command()
    async def on(self, ctx: commands.Context[Any]):
        self.client.sus_on = True
        await ctx.send("Permanent Sus enabled!")

    @commands.command()
    async def off(self, ctx: commands.Context[Any]):
        self.client.sus_on = False
        await ctx.send("Permanent Sus disabled!")


def setup(client: "MyBot"):
    client.add_cog(Sus(client))
