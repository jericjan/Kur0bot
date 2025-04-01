from io import BytesIO
from typing import Any

import aiohttp
import disnake
from disnake.ext import commands
from petpetgif import petpet


class Pet(commands.Cog):
    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True)
    async def pet(self, ctx: commands.Context[Any], url):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                async with aiohttp.ClientSession() as session:
                    async with session.get(user.display_avatar.url) as resp:
                        pfp = await resp.read()
                source = BytesIO(pfp)  # file-like container to hold the emoji in memory
                source.seek(0)
                dest = BytesIO()  # container to store the petpet gif in memory
                petpet.make(source, dest)
                dest.seek(0)
                if isinstance(ctx.channel, disnake.TextChannel):
                    webhook = await ctx.channel.create_webhook(
                        name=ctx.message.author.name
                    )
                    await webhook.send(
                        file=disnake.File(dest, filename="petpet.gif"),
                        username=ctx.message.author.name,
                        avatar_url=ctx.message.author.display_avatar.url,
                    )
                elif isinstance(ctx.channel, disnake.Thread):
                    webhook = await ctx.channel.parent.create_webhook(
                        name=ctx.message.author.name
                    )
                    await webhook.send(
                        file=disnake.File(dest, filename="petpet.gif"),
                        username=ctx.message.author.name,
                        avatar_url=ctx.message.author.display_avatar.url,
                        thread=ctx.channel,
                    )

                await webhook.delete()
        elif url.startswith("http"):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    pfp = await resp.read()
            source = BytesIO(pfp)  # file-like container to hold the emoji in memory
            source.seek(0)
            dest = BytesIO()  # container to store the petpet gif in memory
            petpet.make(source, dest)
            dest.seek(0)
            if isinstance(ctx.channel, disnake.TextChannel):
                webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
                await webhook.send(
                    file=disnake.File(dest, filename="petpet.gif"),
                    username=ctx.message.author.name,
                    avatar_url=ctx.message.author.display_avatar.url,
                )
            elif isinstance(ctx.channel, disnake.Thread):
                webhook = await ctx.channel.parent.create_webhook(
                    name=ctx.message.author.name
                )
                await webhook.send(
                    file=disnake.File(dest, filename="petpet.gif"),
                    username=ctx.message.author.name,
                    avatar_url=ctx.message.author.display_avatar.url,
                    thread=ctx.channel,
                )

            await webhook.delete()


def setup(client: commands.Bot):
    client.add_cog(Pet(client))
