from discord.ext import commands



class Reactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fmega(self, ctx):
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        await webhook.send(
            "https://thumbs.gfycat.com/BleakAdorableLangur-size_restricted.gif",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    async def kotowaru(self, ctx):
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        await webhook.send(
            "https://cdn.discordapp.com/attachments/812666547520667669/852875900731392010/tenor.gif",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    async def ascend(self, ctx):
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        await webhook.send(
            "https://tenor.com/view/bruno-bucciarati-jojo-jjba-death-gif-14981833",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()

    @commands.command()
    async def jizz(self, ctx):
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        await webhook.send(
            "https://pbs.twimg.com/media/E3oLqt8VUAQpRiL?format=jpg&name=900x900",
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()


def setup(client):
    client.add_cog(Reactions(client))
