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
        headers = {"Content-Type": "application/json"}

        data = {"text": msg}
        print(f"Received '{msg}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:9875", headers=headers, json=data
            ) as response:
                gpt_response = await response.text()
                if response.status == 200:
                    await ctx.send(gpt_response)
                    # Handle successful response here
                else:
                    print("response not 200")
                    print(gpt_response)
                    await ctx.send(f"ERROR: {gpt_response}")
                    # Handle error response here
                    pass


def setup(client):
    client.add_cog(OpenAI(client))
