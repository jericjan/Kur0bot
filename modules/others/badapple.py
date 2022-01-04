from discord.ext import commands
import discord
import asyncio


class Badapple(commands.Cog):
    def __init__(self, client):
        self.client = client

    def getemote(self, ctx, name):
        return discord.utils.get(self.client.emojis, name=name)

    @commands.command()
    @commands.cooldown(1.0, 60.0, commands.BucketType.guild)
    async def badapple(self, ctx, *, message=None):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        for i in range(80):
            if i <= 19:
                if i == 9:
                    list1.append(f"{self.getemote(ctx,f'b{i}')}\n")
                else:
                    list1.append(self.getemote(ctx, f"b{i}"))
            elif i <= 39:
                if i == 29:
                    list2.append(f"{self.getemote(ctx,f'b{i}')}\n")
                else:
                    list2.append(self.getemote(ctx, f"b{i}"))
            elif i <= 59:
                if i == 49:
                    list3.append(f"{self.getemote(ctx,f'b{i}')}\n")
                else:
                    list3.append(self.getemote(ctx, f"b{i}"))
            elif i <= 79:
                if i == 69:
                    list4.append(f"{self.getemote(ctx,f'b{i}')}\n")
                else:
                    list4.append(self.getemote(ctx, f"b{i}"))

        await webhook.send(
            f"{''.join([str(i) for i in list1])}",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        await asyncio.sleep(0.5)
        await webhook.send(
            f"{''.join([str(i) for i in list2])}",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        await asyncio.sleep(0.5)
        await webhook.send(
            f"{''.join([str(i) for i in list3])}",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        await asyncio.sleep(0.5)
        await webhook.send(
            f"{''.join([str(i) for i in list4])}",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()


def setup(client):
    client.add_cog(Badapple(client))
