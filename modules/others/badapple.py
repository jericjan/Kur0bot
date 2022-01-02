from discord.ext import commands
import discord
import asyncio


class Badapple(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1.0, 60.0, commands.BucketType.guild)
    async def badapple(self, ctx, *, message=None):

        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        for i in range(80):
            globals()[f"b{i}"] = discord.utils.get(
                self.client.emojis, name="b" + str(i)
            )
        await webhook.send(
            str(b0)
            + str(b1)
            + str(b2)
            + str(b3)
            + str(b4)
            + str(b5)
            + str(b6)
            + str(b7)
            + str(b8)
            + str(b9)
            + "\n"
            + str(b10)
            + str(b11)
            + str(b12)
            + str(b13)
            + str(b14)
            + str(b15)
            + str(b16)
            + str(b17)
            + str(b18)
            + str(b19),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        await asyncio.sleep(0.5)
        await webhook.send(
            str(b20)
            + str(b21)
            + str(b22)
            + str(b23)
            + str(b24)
            + str(b25)
            + str(b26)
            + str(b27)
            + str(b28)
            + str(b29)
            + "\n"
            + str(b30)
            + str(b31)
            + str(b32)
            + str(b33)
            + str(b34)
            + str(b35)
            + str(b36)
            + str(b37)
            + str(b38)
            + str(b39),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        await asyncio.sleep(0.5)
        await webhook.send(
            str(b40)
            + str(b41)
            + str(b42)
            + str(b43)
            + str(b44)
            + str(b45)
            + str(b46)
            + str(b47)
            + str(b48)
            + str(b49)
            + "\n"
            + str(b50)
            + str(b51)
            + str(b52)
            + str(b53)
            + str(b54)
            + str(b55)
            + str(b56)
            + str(b57)
            + str(b58)
            + str(b59),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        await asyncio.sleep(0.5)
        await webhook.send(
            str(b60)
            + str(b61)
            + str(b62)
            + str(b63)
            + str(b64)
            + str(b65)
            + str(b66)
            + str(b67)
            + str(b68)
            + str(b69)
            + "\n"
            + str(b70)
            + str(b71)
            + str(b72)
            + str(b73)
            + str(b74)
            + str(b75)
            + str(b76)
            + str(b77)
            + str(b78)
            + str(b79),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()


def setup(client):
    client.add_cog(Badapple(client))
