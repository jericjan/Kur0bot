import asyncio
from typing import Any, Literal

import disnake
from disnake.ext import commands


class Badapple(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def getemote(self, ctx: commands.Context[Any], name: str):
        return disnake.utils.get(self.client.emojis, name=name)

    @commands.command()
    @commands.cooldown(1, 60.0, commands.BucketType.guild)
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def badapple(self, ctx: commands.Context[Any]):

        lists: list[list[disnake.Emoji | str]] = [[], [], [], []]

        webhook = None
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        elif isinstance(ctx.channel, disnake.Thread):
            if ctx.channel.parent is None:
                await ctx.send("This thread has no parent channel. Please use a normal channel.")
                return
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )

        if webhook is None:
            await ctx.send("Failed to create a webhook. Please try again.")
            return

        for i in range(80):
            nth_msg, nth_emote = divmod(i, 20)
            emote = self.getemote(ctx, f"b{i}")
            if emote is None:
                await ctx.send(f"Emote b{i} not found. Please check the emote name.")
                await webhook.delete()
                return
            
            if nth_emote == 9:
                emote = f"{emote}\n"
            lists[nth_msg].append(emote)
        

        kwargs: dict[Literal['thread'], disnake.abc.Snowflake] = {}
        if isinstance(ctx.channel, disnake.Thread):
            kwargs["thread"] = ctx.channel
        
        for li in lists:
            await webhook.send(
                f"{''.join([str(i) for i in li])}",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                **kwargs
            )
            await asyncio.sleep(0.5)

        await webhook.delete()
        await ctx.message.delete()


def setup(client: commands.Bot):
    client.add_cog(Badapple(client))
