import urllib.parse

import aiohttp
import disnake
import openai
from disnake.ext import commands


class OpenAI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gpt(self, ctx, *, msg):

        url = "amongus.com"
        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Host": "joebiden.its.not.joever.yet",
            "X-RapidAPI-Key": "deeznuts123",
        }
        data = {"query": msg}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response_data = await response.json()
                await ctx.send(response_data["response"])


def setup(client):
    client.add_cog(OpenAI(client))
