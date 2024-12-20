import re
import urllib.parse
from io import BytesIO

import aiohttp
import disnake
from disnake.ext import commands

from myfunctions import msg_link_grabber


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx, top_text, bottom_text, img_url=None):
        img_url = await msg_link_grabber.grab_link(ctx, img_url)
        img_url = urllib.parse.quote(img_url)
        replacements = {
            "-": "--",
            "_": "__",
            " ": "_",
            "\?": "~q",
            "&": "~a",
            "%": "~p",
            "#": "~h",
            r"\/": "~s",
            r"\\": "~b",
            "<": "~l",
            ">": "~g",
            '"': "''",
        }
        for replaced, replacer in replacements.items():
            top_text = re.sub(replaced, replacer, top_text)
            bottom_text = re.sub(replaced, replacer, bottom_text)
        async with aiohttp.ClientSession() as session:
            url = (
                "https://api.memegen.link/images/custom/"
                f"{top_text}/"
                f"{bottom_text}.png?"
                f"background={img_url}"
            )
            print(f"url is {url}")
            async with session.get(url) as resp:
                pic = await resp.read()
                if resp.status != 200:
                    await ctx.send(
                        "Fail", file=disnake.File(BytesIO(pic), filename="meme.png")
                    )
                    return
        await ctx.send(file=disnake.File(BytesIO(pic), filename="meme.png"))


def setup(client):
    client.add_cog(Meme(client))
