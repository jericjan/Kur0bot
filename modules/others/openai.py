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

        async with aiohttp.ClientSession() as session:
            url = "https://free-gpt-4-api.meet508.tech/"
            params = {"text": msg}
            async with session.get(url, params=params) as response:
                response_text = await response.text()
                await ctx.send(response_text)


def setup(client):
    client.add_cog(OpenAI(client))
