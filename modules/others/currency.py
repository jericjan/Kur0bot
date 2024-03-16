import json
import re
from decimal import Decimal

import aiohttp
import disnake
from disnake.ext import commands


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["convert"])
    async def currency(self, ctx, conv_from, conv_to, value):
        async def currency_exists(currency):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
                ) as resp:
                    available_currencies = await resp.json()
            return currency in available_currencies

        if conv_from == conv_to:
            await ctx.send("You can't convert to the same currency!")
            return

        if not await currency_exists(conv_from) or not await currency_exists(conv_to):
            await ctx.send(
                "You've given me a currency that doesn't exist. Please check [here](https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json) for what currencies I support."
            )
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{conv_from}.json"
            ) as resp:
                text = await resp.text()
                currency_dict = json.loads(text, parse_float=lambda x: Decimal(str(x)))
                rate = currency_dict[conv_from][conv_to]
                result = Decimal(value) * rate
                result = result.quantize(Decimal("1.00")).normalize()

        await ctx.send(f"{value} {conv_from.upper()} is {result} {conv_to.upper()}")


def setup(client):
    client.add_cog(Currency(client))
