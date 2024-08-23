import os
import urllib.parse

import aiohttp
import disnake
import g4f
import nest_asyncio
import openai
from disnake.ext import commands
from g4f.client import Client


class OpenAI(commands.Cog):
    def __init__(self, client):
        self.client = client
        nest_asyncio.apply()

    def prompt(self, msg):
        client = Client()
        response = client.chat.completions.create(
            model="meta-llama/Llama-2-70b-chat-hf",
            provider=g4f.Provider.DeepInfra,
            messages=[{"role": "user", "content": msg}],
        )
        return response.choices[0].message.content

    @commands.command()
    async def gpt(self, ctx, *, msg):

        def split_long_string(long_string, chunk_size=2000):
            return [
                long_string[i : i + chunk_size]
                for i in range(0, len(long_string), chunk_size)
            ]

        async with ctx.channel.typing():
            gpt_msg = self.prompt(msg)
            splitted = split_long_string(gpt_msg)
            for split in splitted:
                await ctx.send(split)

def setup(client):
    client.add_cog(OpenAI(client))
