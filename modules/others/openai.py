from importlib.metadata import version
from typing import Any

import g4f  # type: ignore
import nest_asyncio  # type: ignore
from disnake.ext import commands
from g4f.client import Client  # type: ignore


class OpenAI(commands.Cog):
    def __init__(self, client: commands.Bot):
        print(f"g4f version is {version('g4f')}")
        self.client = client
        nest_asyncio.apply()

    def prompt(self, msg: str) -> str:
        client = Client()
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            provider=g4f.Provider.DeepInfraChat,
            messages=[{"role": "user", "content": msg}],
        )
        return response.choices[0].message.content

    @commands.command()
    async def gpt(self, ctx: commands.Context[Any], *, msg):

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

def setup(client: commands.Bot):
    client.add_cog(OpenAI(client))
