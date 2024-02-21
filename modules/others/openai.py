import os
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

        url = os.getenv("GPT_RAPIDAPI_URL")
        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Host": os.getenv("GPT_RAPIDAPI_HOST"),
            "X-RapidAPI-Key": os.getenv("GPT_RAPIDAPI_KEY"),
        }
        data = {"query": msg}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                try:
                    response_data = await response.json()
                    await ctx.send(response_data["response"])
                except Exception as e:
                    txt_data = await response.text()
                    await ctx.send(txt_data)


def setup(client):
    client.add_cog(OpenAI(client))
