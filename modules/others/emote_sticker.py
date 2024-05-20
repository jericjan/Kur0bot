from disnake.ext import commands
import disnake
import asyncio
import aiohttp
import functools
import requests
import io
import re
from PIL import Image
from myfunctions import msg_link_grabber


class EmoteSticker(commands.Cog):
    def __init__(self, client):
        self.client = client

    def has_guild_exp_perms(self, ctx):
        has_expr_perms = ctx.channel.permissions_for(
            ctx.author
        ).manage_guild_expressions
        return has_expr_perms

    @commands.command(aliases=["e"])
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def emote(self, ctx, *message):
        if len(message) == 0:
            await ctx.send("Give an emoji name.")
            return
        emoji_list = []
        if isinstance(ctx.channel, disnake.TextChannel):
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        elif isinstance(ctx.channel, disnake.Thread):
            webhook = await ctx.channel.parent.create_webhook(
                name=ctx.message.author.name
            )
        print(type(message))
        for i in range(len(message)):
            emoji = disnake.utils.get(self.client.emojis, name=message[i])
            emojistr = str(emoji)
            emoji_list.append(emojistr)
        if emoji is None:
            oof = await ctx.send("Invalid emoji name.")
            await asyncio.sleep(3)
            await oof.delete()
            await ctx.message.delete()
            return
        if isinstance(ctx.channel, disnake.TextChannel):
            await webhook.send(
                "".join(emoji_list),
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
        elif isinstance(ctx.channel, disnake.Thread):
            await webhook.send(
                "".join(emoji_list),
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
                thread=ctx.channel,
            )
        await webhook.delete()
        await ctx.message.delete()

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
    @commands.bot_has_permissions(
        embed_links=True,
        use_external_emojis=True,
    )
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
                        embed.title = re.sub(r"(?<=\w)\w", "█", guild.name)
                    else:
                        embed.title = ""
                    embed.description = "".join(message)
                    await ctx.send(embed=embed)
            else:
                print("bad apple server")

    def run_in_executor(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: f(*args, **kwargs))

        return inner

    @run_in_executor
    def emote_resize(self, link, format_type="PNG"):  # Your wrapper for async use
        byteio = io.BytesIO(link)
        im = Image.open(byteio)
        width, height = im.size
        new_width = 128
        new_height = new_width * height / width
        newsize = (int(new_width), int(new_height))
        im = im.resize(newsize)
        byteio.close()
        byteio2 = io.BytesIO()
        byteio2.seek(0)
        im.save(byteio2, format=format_type)
        byteio2.seek(0)
        return byteio2, new_width, new_height

    @commands.command(aliases=["uploademoji", "ue"])
    @commands.bot_has_permissions(manage_emojis=True, manage_messages=True)
    async def uploademote(
        self, ctx, title, *, link=None
    ):  # upload emoji from emoji url
        limit = ctx.guild.emoji_limit
        emoji_list = ctx.guild.emojis
        normal_count = 0
        animated_count = 0
        for i in emoji_list:
            if i.animated:
                animated_count += 1
            else:
                normal_count += 1
        normal_free_slots = limit - normal_count
        animated_free_slots = limit - animated_count
        if normal_free_slots == 0:
            await ctx.send("No more free normal slots :(")
        else:
            await ctx.send(f"{normal_free_slots} normal slots left :)")
        if animated_free_slots == 0:
            await ctx.send("No more free animated slots :(")
        else:
            await ctx.send(f"{animated_free_slots} animated slots left :)")

        if self.has_guild_exp_perms(ctx):
            link = await msg_link_grabber.grab_link(ctx, link)
            print(link)
            if re.match(r"https:\/\/cdn.discordapp.com\/emojis\/\d+", link):
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        re.findall(r"https:\/\/cdn.discordapp.com\/emojis\/\d+", link)[
                            0
                        ]
                    ) as response:
                        img = await response.read()
            elif re.match(r"\d+", link):
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://cdn.discordapp.com/emojis/{link}"
                    ) as response:
                        img = await response.read()
            elif link.startswith("http"):
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as response:
                        img = await response.read()
            else:
                await ctx.send("Invalid link.")
                return
            # now img contains the bytes of the image, let's create the emoji
            if link.split("?")[0].endswith("gif"):
                print("a gif")
                # file = img
                file, width, height = await self.emote_resize(img, "GIF")
                await ctx.send(f"New GIF size is: {width}x{height}", delete_after=3.0)
            else:
                print("not a gif")
                file, width, height = await self.emote_resize(img)
                await ctx.send(f"New image size is: {width}x{height}", delete_after=3.0)
            try:
                file = file.read()
            except:
                pass
            try:
                print(f"file is a {type(file)}")
                await ctx.guild.create_custom_emoji(name=title, image=file)

                await ctx.send("Emoji uploaded!", delete_after=3.0)

                emoji = disnake.utils.get(self.client.emojis, name=title)

                await ctx.send(str(emoji))

            except Exception as e:
                await ctx.send(f"Something failed. Oof.\n{e}")
                raise e
        else:
            await ctx.send("Only Admins/Mods can use this command")

    @commands.command(aliases=["re"])
    @commands.bot_has_permissions(manage_emojis=True, manage_messages=True)
    async def removeemote(self, ctx, emote: disnake.Emoji):

        if emote.guild.id != ctx.guild.id:
            raise commands.EmojiNotFound(emote.name)

        if self.has_guild_exp_perms(ctx):
            await ctx.send(f"Deleting {str(emote)}... Goodbye old friend! 😢")
            await emote.delete()
        else:
            await ctx.send("No can do. You ain't got the perms fo' that!")

    @commands.command(aliases=["rs"])
    @commands.bot_has_permissions(manage_emojis=True, manage_messages=True)
    async def removesticker(self, ctx, sticker: disnake.GuildSticker):

        if sticker.guild.id != ctx.guild.id:
            raise commands.GuildStickerNotFound(sticker.name)

        if self.has_guild_exp_perms(ctx):
            await ctx.send(
                f"Deleting this sticker... One last look before you go. Goodbye old friend! 😢"
            )
            await ctx.send(stickers=[sticker])
            await sticker.delete()
        else:
            await ctx.send("No can do. You ain't got the perms fo' that!")

    @removeemote.error
    @removesticker.error
    async def removeemote_error(self, ctx, error):
        name = error.argument
        ctx._ignore_me_ = True
        if isinstance(error, commands.EmojiNotFound):
            await ctx.send(
                f"dang, i can't find the {name} emoji, pardner. can't delete that which ain't exist. truth."
            )
        elif isinstance(error, commands.GuildStickerNotFound):
            await ctx.send(
                f"dang, i can't find the {name} sticker, pardner. can't delete that which ain't exist. truth."
            )

    @run_in_executor
    def sticker_resize(self, link):  # Your wrapper for async use
        response = requests.get(link)  # threaded
        byteio = io.BytesIO(response.content)
        im = Image.open(byteio)
        width, height = im.size
        new_width = 320
        new_height = new_width * height / width
        newsize = (int(new_width), int(new_height))
        im = im.resize(newsize)
        byteio.close()
        byteio2 = io.BytesIO()
        byteio2.seek(0)
        im.save(byteio2, format="PNG")
        byteio2.seek(0)
        return byteio2, new_width, new_height

    @commands.command(aliases=["us"])
    @commands.bot_has_permissions(manage_emojis=True, manage_messages=True)
    async def uploadsticker(
        self, ctx, name, emoji, link=None
    ):  # upload emoji from emoji url
        limit = ctx.guild.sticker_limit
        if limit == 0:
            await ctx.send(
                "It says here the server's sticker limit is 0 but uhhh that doesn't seem right.",
                delete_after=3.0,
            )
            limit = 5
        sticker_count = len(ctx.guild.stickers)
        print(f"sticker_count {sticker_count}")
        print(f"limit {limit}")
        free_slots = limit - sticker_count
        if free_slots == 0:
            await ctx.send("No more free slots :(")
        else:
            await ctx.send(f"{free_slots} slots left :)")
            if self.has_guild_exp_perms(ctx):
                link = await msg_link_grabber.grab_link(ctx, link)
                print(link)
                file, width, height = await self.sticker_resize(link)
                file.seek(0)
                await ctx.send(f"New image size is: {width}x{height}", delete_after=3.0)
                sticker = await ctx.guild.create_sticker(
                    name=name, emoji=emoji, file=disnake.File(file)
                )
                await ctx.send("Sticker uploaded!", delete_after=3.0)
                await ctx.send(stickers=[sticker])
            else:
                await ctx.send("Only Admins/Mods can use this command")


def setup(client):
    client.add_cog(EmoteSticker(client))
