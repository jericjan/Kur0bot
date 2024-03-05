import math
import re

import disnake
from disnake.ext import commands


class Height(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def height(self, ctx, *, arg):
        def is_foot_inch(x):
            return re.match(r"\d+'\d+\"", x)

        def get_foot_inch(x):
            return map(lambda x: int(x), re.search(r"(\d+)'(\d+)\"", x).groups())

        def is_cm(x):
            return re.match(r"\d+cm", x)

        def get_cm(x):
            return int(re.search(r"(\d+)cm", x).group(1))

        if is_foot_inch(arg):
            feet, inches = get_foot_inch(arg)
            cm = feet * 30.48 + inches * 2.54
            await ctx.send(f"{cm}cm")
        elif is_cm(arg):
            cm = get_cm(arg)
            feet = math.floor(cm / 30.48)
            inches = (cm - feet * 30.48) * (1 / 2.54)
            await ctx.send(f"{feet}'{round(inches, 2)}\"")
        else:
            await ctx.send(
                "You must send either a height in foot-inches (ex. 5'3\") or cm (ex. 159cm)"
            )


def setup(client):
    client.add_cog(Height(client))
