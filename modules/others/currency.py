import json
import re
from decimal import Decimal
from typing import TYPE_CHECKING, Any, cast

import aiohttp
import disnake
from disnake.ext import commands

if TYPE_CHECKING:
    from myfunctions.command_bridge import Bridger

class Currency(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def currency(self, thing, conv_from, conv_to, value):
        bridger = cast(
            "Bridger",
            self.client.get_cog("Bridger")
        )
        send_msg = bridger.send_msg

        conv_from = conv_from.lower()
        conv_to = conv_to.lower()
        async def currency_exists(currency):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
                ) as resp:
                    available_currencies = await resp.json()
            return currency in available_currencies

        if conv_from == conv_to:
            await send_msg(thing, "You can't convert to the same currency!")
            return

        if not await currency_exists(conv_from) or not await currency_exists(conv_to):
            await send_msg(
                thing,
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

        await send_msg(
            thing, f"{value} {conv_from.upper()} is {result} {conv_to.upper()}"
        )

    @commands.slash_command(name="currency")
    async def s_currency(self, inter, conv_from: str, conv_to: str, value: str):
        """
        Converts currency!!!

        Parameters
        ----------
        conv_from: The currency you want to convert from
        conv_to: The currency you want to convert to
        value: The value of the curreny you're converting from
        """
        await self.currency(inter, conv_from, conv_to, value)

    @commands.command(name="currency", aliases=["convert"])
    async def p_currency(self, ctx: commands.Context[Any], conv_from, conv_to, value):
        await self.currency(ctx, conv_from, conv_to, value)

def setup(client: commands.Bot):
    client.add_cog(Currency(client))
