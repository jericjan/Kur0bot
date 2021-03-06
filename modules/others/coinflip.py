from disnake.ext import commands

import random


class Coinflip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["flip"])
    async def coinflip(self, ctx, *, input):
        input1 = input.lower()
        print(f"input is {input1}")
        choices = ["heads", "tails"]
        if input1 not in choices:
            await ctx.send(f"bruhg. there's no {input1} in a coin dummy 😠")
            return
        result = random.choice(choices)
        if input1 == result:
            await ctx.send(f"It's {result}! You win!")
        else:
            await ctx.send(f"It's {result}! You lose!")


def setup(client):
    client.add_cog(Coinflip(client))
