from disnake.ext import commands
import disnake


class Reactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def fmega(self, ctx):
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                "https://thumbs.gfycat.com/BleakAdorableLangur-size_restricted.gif",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )
            await webhook.send(
                "https://thumbs.gfycat.com/BleakAdorableLangur-size_restricted.gif",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )

        await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def kotowaru(self, ctx):
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                "https://cdn.discordapp.com/attachments/812666547520667669/852875900731392010/"
                "tenor.gif",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )
            await webhook.send(
                "https://cdn.discordapp.com/attachments/812666547520667669/"
                "852875900731392010/tenor.gif",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )

        await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def ascend(self, ctx):
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                "https://tenor.com/view/bruno-bucciarati-jojo-jjba-death-gif-14981833",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )
            await webhook.send(
                "https://tenor.com/view/bruno-bucciarati-jojo-jjba-death-gif-14981833",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )

        await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def jizz(self, ctx):
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                "https://pbs.twimg.com/media/E3oLqt8VUAQpRiL?format=jpg&name=900x900",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )
            await webhook.send(
                "https://pbs.twimg.com/media/E3oLqt8VUAQpRiL?format=jpg&name=900x900",
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )

        await webhook.delete()
        await ctx.message.delete()


def setup(client):
    client.add_cog(Reactions(client))
