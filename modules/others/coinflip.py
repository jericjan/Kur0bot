import random
from typing import Any

from disnake.ext import commands


class Coinflip(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["flip"])
    async def coinflip(self, ctx: commands.Context[Any], *, input: str):
        input = input.lower()
        print(f"input is {input}")
        choices = ["heads", "tails"]
        if input not in choices:
            await ctx.send(f"bruhg. there's no {input} in a coin dummy 😠")
            return
        result = random.choice(choices)
        if input == result:
            await ctx.send(f"It's {result}! You win!")
        else:
            await ctx.send(f"It's {result}! You lose!")


def setup(client: commands.Bot):
    client.add_cog(Coinflip(client))
