import disnake
from disnake.ext import commands

from myfunctions import msg_link_grabber
from myfunctions.greenscreen import GreenScreener, GreenScreenerHandler
from typing import Any

class ThisRightHere(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["this"])
    async def thisrighthere(self, ctx: commands.Context[Any], link=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)
        g_screen_han = GreenScreenerHandler(
            ctx,
            link,
            "videos/this_right_here/",
            342,
            640,
            25.0,
            "this.mp4",
            "mark",
        )
        await g_screen_han.start()


def setup(client: commands.Bot):
    client.add_cog(ThisRightHere(client))
