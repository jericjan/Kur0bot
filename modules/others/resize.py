from disnake.ext import commands
import disnake

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
import os
import uuid
import asyncio
from arsenic import get_session, keys, browsers, services
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
from pilmoji import Pilmoji

from tqdm import tqdm
import functools
from aiolimiter import AsyncLimiter
import shlex

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
        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
            if ctx.message.attachments:  # message has images
                print("is attachment")
                link = ctx.message.attachments[0].url
            elif ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                if msg.attachments:  # if replied has image
                    link = msg.attachments[0].url
                elif msg.embeds:  # if replied has link
                    link = msg.embeds[0].url

                # print("embmeds: {0}".format(msg.embeds))
                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # link= msg.attachments[0].url
                else:
                    await ctx.send("the message you replied to has no image, baka!")
            else:
                await ctx.send("you did something wrong. brug. try again.")
                return
            print(link)
        message = await ctx.send("Resizing...")
        bruh = await self.foo(link, width, height)
        bruh.seek(0)
        filename = link.split("/")[-1]
        await ctx.send(file=disnake.File(bruh, filename=filename))
        bruh.close()
        await message.delete()

    @commands.command()
    async def rs(self, ctx, link=None):
        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
            if ctx.message.attachments:  # message has images
                print("is attachment")
                link = ctx.message.attachments[0].url
            elif ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                if msg.attachments:  # if replied has image
                    link = msg.attachments[0].url
                elif msg.embeds:  # if replied has link
                    link = msg.embeds[0].url

                # print("embmeds: {0}".format(msg.embeds))
                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # link= msg.attachments[0].url
                else:
                    await ctx.send("the message you replied to has no image, baka!")
            else:
                await ctx.send("you did something wrong. brug. try again.")
                return
            print(link)
        message = await ctx.send("Resizing...")
        bruh = await self.foo(link, 1600, 720)
        bruh.seek(0)
        filename = link.split("/")[-1]
        await ctx.send(file=disnake.File(bruh, filename=filename))
        bruh.close()
        await message.delete()

def setup(client):
    client.add_cog(Resize(client))
