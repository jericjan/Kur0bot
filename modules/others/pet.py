from petpetgif import petpet
import requests
from io import BytesIO
from disnake.ext import commands
import disnake


class Pet(commands.Cog):
    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True)
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
            pfp = requests.get(url)
            source = BytesIO(
                pfp.content
            )  # file-like container to hold the emoji in memory
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


def setup(client):
    client.add_cog(Pet(client))
