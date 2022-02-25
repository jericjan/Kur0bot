from disnake.ext import commands
import disnake
import asyncio
import aiohttp


class EmoteSticker(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["e"])
    async def emote(self, ctx, *message):
        if len(message) == 0:
          await ctx.send("Give an emoji name.")
          return
        emoji_list = []
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        print(type(message))
        for i in range(len(message)):
            emoji = disnake.utils.get(self.client.emojis, name=message[i])
            emojistr = str(emoji)
            emoji_list.append(emojistr)
        if emoji is None:
            oof = await ctx.send(f"Invalid emoji name.")
            await asyncio.sleep(3)
            await oof.delete()
            await ctx.message.delete()
            return
        await webhook.send(
            "".join(emoji_list),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
        await ctx.message.delete()

    @commands.command(aliases=["s"])
    async def sticker(self, ctx, msgID: int):
        msg = await ctx.fetch_message(msgID)
        await ctx.send(msg.stickers)

    def paginate(self, lines, chars=2000):
        size = 0
        message = []
        for line in lines:
            if len(line) + size > chars:
                yield message
                message = []
                size = 0
            message.append(line)
            size += len(line)
        yield message

    @commands.command(aliases=["ge"])
    async def getemotes(self, ctx):
        server = ctx.message.guild
        emojis = [str(x) for x in server.emojis]
        message = ""
        embed = disnake.Embed()
        for guild in self.client.guilds:
            if guild.id != 856415893305950228 and guild.id != 856412098459860993:
                print(guild.id)
                # await ctx.send(guild.name)
                emojis = [str(x) for x in guild.emojis]
                for index, message in enumerate(self.paginate(emojis)):
                    if index == 0:
                        embed.title = guild.name
                    else:
                        embed.title = ""
                    embed.description = "".join(message)
                    await ctx.send(embed=embed)
            else:
                print("bad apple server")

    @commands.command()
    async def id(self, ctx, title, *, message=None):  # upload emoji from emoji url
        if "cdn.discordapp.com" in message:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://cdn.discordapp.com/emojis/{message.split('/')[4].split('.')[0]}"
                ) as response:
                    img = await response.read()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://cdn.discordapp.com/emojis/{message}"
                ) as response:
                    img = await response.read()
        # now img contains the bytes of the image, let's create the emoji
        await ctx.guild.create_custom_emoji(name=title, image=img)
        await ctx.send("Emoji uploaded!")


def setup(client):
    client.add_cog(EmoteSticker(client))
