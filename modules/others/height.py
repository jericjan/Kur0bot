import math
import re
from decimal import Decimal, getcontext
from typing import Any

from disnake.ext import commands


class Height(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        getcontext().prec = 30

    @commands.command()
    async def height(self, ctx: commands.Context[Any], *, arg: str):
        def is_foot_inch(x: str):
            return re.match(r"\d+'\d+\.?\d*\"", x)

        def get_foot_inch(x: str) -> tuple[str, str]:
            return re.search(r"(\d+)'(\d+\.?\d*)\"", x).groups()  # type: ignore

        def is_cm(x: str):
            return re.match(r"(\d+\.?\d+|\d)cm", x)

        def get_cm(x: str) -> str:
            return re.search(r"(\d+\.?\d+|\d)cm", x).group(1)  # type: ignore

        if is_foot_inch(arg):
            feet, inches = get_foot_inch(arg)
            cm = Decimal(feet) * Decimal("30.48") + Decimal(inches) * Decimal("2.54")
            await ctx.send(f"{cm.quantize(Decimal('1.00')).normalize()}cm")
        elif is_cm(arg):
            cm = get_cm(arg)
            feet = math.floor(Decimal(cm) / Decimal("30.48"))
            inches = (Decimal(cm) - (Decimal(feet) * Decimal("30.48"))) * (
                Decimal(1) / Decimal("2.54")
            )
            await ctx.send(f"{feet}'{inches.quantize(Decimal('1.00')).normalize()}\"")
        else:
            await ctx.send(
                "You must send either a height in foot-inches (ex. 5'3\") or cm (ex. 159cm)"
            )


def setup(client: commands.Bot):
    client.add_cog(Height(client))
