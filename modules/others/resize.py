from disnake.ext import commands
import disnake


import asyncio

from PIL import Image
import io
import requests


import functools
from aiolimiter import AsyncLimiter

import myfunctions.msg_link_grabber as msg_link_grabber

limiter = AsyncLimiter(1, 1)


class Resize(commands.Cog):
    def __init__(self, client):
        self.client = client

    def run_in_executor(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: f(*args, **kwargs))

        return inner

    def bar(self, link, width, height):
        response = requests.get(link)
        byteio = io.BytesIO(response.content)
        im = Image.open(byteio)
        newsize = (int(width), int(height))
        im = im.resize(newsize)
        byteio.close()
        byteio2 = io.BytesIO()
        byteio2.seek(0)
        im.save(byteio2, format="PNG")
        byteio2.seek(0)
        return byteio2

    @run_in_executor
    def foo(self, link, width, height):  # Your wrapper for async use
        out = self.bar(link, width, height)
        return out

    @commands.command()
    async def resize(self, ctx, width, height, link=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        message = await ctx.send("Resizing...")
        bruh = await self.foo(link, width, height)
        bruh.seek(0)
        filename = link.split("/")[-1]
        await ctx.send(file=disnake.File(bruh, filename=filename))
        bruh.close()
        await message.delete()
        await ctx.message.delete()

    @commands.command()
    async def rs(self, ctx, link=None):
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)
        message = await ctx.send("Resizing...")
        bruh = await self.foo(link, 1600, 720)
        bruh.seek(0)
        filename = link.split("/")[-1]
        await ctx.send(file=disnake.File(bruh, filename=filename))
        bruh.close()
        await message.delete()
        await ctx.message.delete()


def setup(client):
    client.add_cog(Resize(client))
