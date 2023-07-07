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
            try:
                async with session.get(
                    f"http://jericjan.jprq.live/?msg={urllib.parse.quote(msg)}"
                ) as r:  # lt -p 1235  -s kur0gpt
                    if r.status == 200:
                        # json_body = await r.json()
                        json_body = await r.text()
                        await ctx.message.reply(json_body)
                    else:
                        await ctx.message.reply(
                            f"le fail. kur0 pc off maybe. Error: {r.status}"
                        )
            except:
                await ctx.message.reply("le fail. kur0 pc off maybe..")

    # gpt_response = json_body['choices'][0]['message']
    # await ctx.message.reply(gpt_response)


def setup(client):
    client.add_cog(OpenAI(client))
