import random
from typing import Any, cast, TYPE_CHECKING

import disnake
from disnake.ext import commands
import numpy
from pathlib import Path

if TYPE_CHECKING:
    from modules.stats import Stats

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

    @commands.command(aliases=["rps"])
    async def rockpaperscissors(self, ctx: commands.Context[Any], *, player_choice: str):
        player_choice = player_choice.lower()
        choices = ["rock", "paper", "scissors"]
        if player_choice not in choices:
            await ctx.send(f"bruhg. there's no {player_choice} in rock paper scissors dummy 😠")
            return
        bot_choice = random.choice(choices)
     
        if player_choice == bot_choice:
            await ctx.send(f"I chose {bot_choice}. It's a tie!")
            return

        win_conditions = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

        if win_conditions[player_choice] == bot_choice:
            await ctx.send(f"I chose {bot_choice}. You win!")
        else:
            await ctx.send(f"I chose {bot_choice}. You lose!")

    @commands.command()
    async def gamble(self, ctx: commands.Context[Any]):

        imgs = [
            Path("images/hampter") / x
            for x in [
                "hampter.png",
                "silver.png",
                "gold.png",
                "phantom.png",
                "cosmic.png",
            ]
        ]

        basic_hampters = [
            Path("images/hampter") / x
            for x in [
                "hampter.png",
                "BOMBACLAT_HNEK.png",
                "BOMPTER.png",
                "DONER_MACHT_SCHONER.png",
                "hamber_LEAN.png",
                "sesompter.png"
            ]            
        ]

        names = [
            "Basic",
            "Silver",
            "Gold",
            "Phantom",
            "Cosmic",
        ]

        basic_names = [
            "Original",
            "BOMBACLAT Hampter with a HNEK",
            "Bompter",
            "Hampter with Döner",
            "Hampter with LEAN",
            "Boblox Hampter"
        ]

        chances = [
            0.549450549,
            0.274725275,
            0.10989011,
            0.054945055,
            0.010989011
        ]

        selected_idx: int = numpy.random.choice(
                len(names), p=chances # type: ignore
        )
        stats_cog = cast("Stats", self.client.get_cog("Stats"))
        # VV This runs get_cog for MotorDbManager twice now
        user_stat = stats_cog.get_user(ctx.guild.id if ctx.guild else ctx.author.id, ctx.author.id)        
        await user_stat.increment(f"Hampter Gamble.{names[selected_idx]}", 1)

        if names[selected_idx] == "Basic":
            basic_idx = numpy.random.choice(len(basic_hampters))
            filename = basic_hampters[basic_idx]
            basic_variant = f" (Variant: {basic_names[basic_idx]})"
        else:
            filename = imgs[selected_idx]
            basic_variant = ""

        await ctx.send(
            f"You won {names[selected_idx]} Hampter{basic_variant}",
            file=disnake.File(str(filename))
        )
        
def setup(client: commands.Bot):
    client.add_cog(Coinflip(client))
