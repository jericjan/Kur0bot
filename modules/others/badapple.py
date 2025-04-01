import asyncio
from typing import Any

import disnake
from disnake.ext import commands


class Badapple(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def getemote(self, ctx: commands.Context[Any], name):
        return disnake.utils.get(self.client.emojis, name=name)

    @commands.command()
    @commands.cooldown(1.0, 60.0, commands.BucketType.guild)
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def badapple(self, ctx: commands.Context[Any], *, message=None):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        elif isinstance(ctx.channel, disnake.Thread):
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )

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

        if isinstance(ctx.channel, disnake.TextChannel):
            await webhook.send(
                f"{''.join([str(i) for i in list1])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            await webhook.send(
                f"{''.join([str(i) for i in list1])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )

        await asyncio.sleep(0.5)
        if isinstance(ctx.channel, disnake.TextChannel):
            await webhook.send(
                f"{''.join([str(i) for i in list2])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            await webhook.send(
                f"{''.join([str(i) for i in list2])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )
        await asyncio.sleep(0.5)
        if isinstance(ctx.channel, disnake.TextChannel):
            await webhook.send(
                f"{''.join([str(i) for i in list3])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            await webhook.send(
                f"{''.join([str(i) for i in list3])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )
        await asyncio.sleep(0.5)
        if isinstance(ctx.channel, disnake.TextChannel):
            await webhook.send(
                f"{''.join([str(i) for i in list4])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            await webhook.send(
                f"{''.join([str(i) for i in list4])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )

        await webhook.delete()
        await ctx.message.delete()


def setup(client: commands.Bot):
    client.add_cog(Badapple(client))
