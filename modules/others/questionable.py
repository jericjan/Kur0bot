import random

import disnake
from disnake.ext import commands


class Questionable(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dashboard_db = self.client.get_cog("MotorDbManager").motor_client[
            "dashboard"
        ]

    @commands.user_command(name="Segg")
    async def user_sex(self, inter, user: disnake.User):
        if user == self.client.user:
            channel = (
                inter.channel.mention
                if isinstance(inter.channel, disnake.TextChannel)
                else "DMs"
            )
            desc = f"Like rn? in {channel}? Here? Actually? I mean ok???"
        elif user == inter.author:
            desc = f"Bro is fucking himself <:brois:1315502264038854657>"
        else:
            desc = f"{inter.author.mention} just sexerized {user.mention} 😳"

        em = disnake.Embed(title="Sex", description=desc)
        gif = (
            await self.dashboard_db["sex-gifs"]
            .aggregate([{"$sample": {"size": 1}}])
            .to_list(1)
        )
        gif = gif[0]["url"]
        # gifs = [
        # "https://cdn.discordapp.com/attachments/1210367093338415164/1315511944563920947/seg.gif",
        # "https://cdn.discordapp.com/attachments/1210367093338415164/1315516035645837444/seg2.gif",
        # "https://media1.tenor.com/m/1SdB5UVe998AAAAC/kissing.gif",
        # "https://media1.tenor.com/m/hKR4tj_FaGkAAAAC/kiss.gif",
        # "https://media1.tenor.com/m/JmeXszjYcfAAAAAC/huh-fate.gif",
        # ]
        em.set_image(url=gif)
        await inter.response.send_message(embed=em)

    @commands.command()
    async def sex(self, ctx, user: disnake.User):
        # gifs = [
        # "|| https://cdn.discordapp.com/attachments/1210367093338415164/1315511944563920947/seg.gif ||",
        # "|| https://cdn.discordapp.com/attachments/1210367093338415164/1315516035645837444/seg2.gif ||",
        # "|| https://tenor.com/view/kissing-gif-20150608 ||",
        # "https://tenor.com/view/kiss-gif-5739144",
        # "https://tenor.com/view/huh-fate-kaleid-liner-prisma-gif-5739132",
        # ]

        gif = (
            await self.dashboard_db["sex-gifs"]
            .aggregate([{"$sample": {"size": 1}}])
            .to_list(1)
        )
        gif = gif[0]["url"]
        await ctx.send(f"|| {gif} ||")

        if user == self.client.user:
            await ctx.send(
                f"Like rn? in {ctx.channel.mention}? Here? Actually? I mean ok???"
            )
        elif user == ctx.author:
            await ctx.send(f"Bro is fucking himself <:brois:1315502264038854657>")
        else:
            await ctx.send(f"{ctx.author.mention} just sexerized {user.mention} 😳")

    @commands.user_command(name="Footjob")
    async def user_footjob(self, inter, user: disnake.User):
        if user == self.client.user:
            desc = f"{inter.author.mention} IS GIVING ME A FOOTJOB??? HELLO HUMAN RESOURCES?? WTFFF??????"
        elif user == inter.author:
            desc = "Bro is giving himself a footjob <:brois:1315502264038854657>"
        else:
            desc = f"{inter.author.mention} gave {user.mention} a footjob!"

        em = disnake.Embed(title="Footjob", description=desc)
        # gifs = [
        # "https://cdn.discordapp.com/attachments/1201051292198518846/1315505967470870568/SPOILER_toga-giving-a-footjob.gif",
        # "https://cdn.discordapp.com/attachments/1201051292198518846/1315513265517760592/SPOILER_mafuyu.gif",
        # ]
        gif = (
            await self.dashboard_db["footjob-gifs"]
            .aggregate([{"$sample": {"size": 1}}])
            .to_list(1)
        )
        gif = gif[0]["url"]
        em.set_image(url=gif)
        await inter.response.send_message(embed=em)

    @commands.command()
    async def footjob(self, ctx, user: disnake.User):
        # gifs = [
        # "https://cdn.discordapp.com/attachments/1201051292198518846/1315505967470870568/SPOILER_toga-giving-a-footjob.gif",
        # "https://cdn.discordapp.com/attachments/1201051292198518846/1315513265517760592/SPOILER_mafuyu.gif",
        # ]

        gif = (
            await self.dashboard_db["footjob-gifs"]
            .aggregate([{"$sample": {"size": 1}}])
            .to_list(1)
        )
        gif = gif[0]["url"]

        await ctx.send(f"|| {gif} ||")
        if user == self.client.user:
            await ctx.send(
                f"{ctx.author.mention} IS GIVING ME A FOOTJOB??? HELLO HUMAN RESOURCES?? WTFFF??????"
            )
        elif user == ctx.author:
            await ctx.send(
                "Bro is giving himself a footjob <:brois:1315502264038854657>"
            )
        else:
            await ctx.send(f"{ctx.author.mention} gave {user.mention} a footjob!")


def setup(client):
    client.add_cog(Questionable(client))
