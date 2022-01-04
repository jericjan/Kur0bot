from petpetgif import petpet
import requests
from io import BytesIO
from discord.ext import commands
import discord


class Pet(commands.Cog):
    @commands.command()
    async def pet(self, ctx, url):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                pfp = requests.get(user.display_avatar.url)
                source = BytesIO(
                    pfp.content
                )  # file-like container to hold the emoji in memory
                source.seek(0)
                dest = BytesIO()  # container to store the petpet gif in memory
                petpet.make(source, dest)
                dest.seek(0)
                webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
                await webhook.send(
                    file=discord.File(dest, filename=f"petpet.gif"),
                    username=ctx.message.author.name,
                    avatar_url=ctx.message.author.display_avatar.url,
                )

                webhooks = await ctx.channel.webhooks()
                for webhook in webhooks:
                    await webhook.delete()
        elif url.startswith("http"):
            pfp = requests.get(url)
            source = BytesIO(
                pfp.content
            )  # file-like container to hold the emoji in memory
            source.seek(0)
            dest = BytesIO()  # container to store the petpet gif in memory
            petpet.make(source, dest)
            dest.seek(0)
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                file=discord.File(dest, filename=f"petpet.gif"),
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )

            webhooks = await ctx.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()


def setup(client):
    client.add_cog(Pet(client))
