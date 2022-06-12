from disnake.ext import commands
import disnake
import asyncio
import aiohttp
import functools
import requests 
import io
import re
from PIL import Image

class EmoteSticker(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["e"])
    async def emote(self, ctx, *message):
        if len(message) == 0:
            await ctx.send("Give an emoji name.")
            return
        emoji_list = []
        if isinstance(ctx.channel, disnake.TextChannel):        
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        elif isinstance(ctx.channel, disnake.Thread):      
            webhook = await ctx.channel.parent.create_webhook(name=ctx.message.author.name)        
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
                avatar_url=ctx.message.author.display_avatar.url,thread=ctx.channel
            )        
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

    def run_in_executor(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: f(*args, **kwargs))
        return inner

    @run_in_executor
    def emote_resize(self, link):  # Your wrapper for async use      
        byteio = io.BytesIO(link)
        im = Image.open(byteio)
        width, height = im.size
        new_width  = 128
        new_height = new_width * height / width            
        newsize = (int(new_width), int(new_height))
        im = im.resize(newsize)
        byteio.close()
        byteio2 = io.BytesIO()
        byteio2.seek(0)
        im.save(byteio2, format="PNG")
        byteio2.seek(0)
        return byteio2, new_width, new_height
      
    @commands.command(aliases=["uploademoji","ue"])
    async def uploademote(self, ctx, title, *, link=None):  # upload emoji from emoji url
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
        avi_guild = self.client.get_guild(603147860225032192)
        while avi_guild == None:
            pass
        admin = disnake.utils.get(avi_guild.roles, name="Admin")
        moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
        avilon = disnake.utils.get(avi_guild.roles, name="Avilon")
        roles = [admin, moderator, avilon]
        if (
            any(role in roles for role in ctx.author.roles)
        ):            
            if link == None:
                print(ctx.message.attachments)  # a list
                print(ctx.message.reference)
                if ctx.message.attachments:  # message has images
                    print("is attachment")
                    link = ctx.message.attachments[0].url
                elif ctx.message.reference is not None:  # message is replying
                    print("is reply")
                    id = ctx.message.reference.message_id
                    msg = await ctx.channel.fetch_message(id)
                    if msg.attachments:  # if replied has image
                        link = msg.attachments[0].url
                    elif msg.embeds:  # if replied has link
                        link = msg.embeds[0].url

                    # print("embmeds: {0}".format(msg.embeds))
                    # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                    #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                    # link= msg.attachments[0].url
                    else:
                        await ctx.send("the message you replied to has no image, baka!")
                else:
                    await ctx.send("you did something wrong. brug. try again.")
                    return
                print(link)               
            if re.match(r"https:\/\/cdn.discordapp.com\/emojis\/\d+",link):
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        re.findall(r"https:\/\/cdn.discordapp.com\/emojis\/\d+",link)[0]
                    ) as response:
                        img = await response.read()
            elif re.match(r"\d+",link):
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
            file, width, height = await self.emote_resize(img)
            await ctx.send(f"New image size is: {width}x{height}",delete_after=3.0)
            try:
                await ctx.guild.create_custom_emoji(name=title, image=img)
                await ctx.send("Emoji uploaded!",delete_after=3.0)
                emoji = disnake.utils.get(self.client.emojis, name=title)
                await ctx.send(str(emoji))
            except:
                await ctx.send("Something failed. Oof.")
        else:
            await ctx.send("Only Avi/Admins/Mods can use this command")     


    @run_in_executor
    def sticker_resize(self, link):  # Your wrapper for async use
        response = requests.get(link)
        byteio = io.BytesIO(response.content)
        im = Image.open(byteio)
        width, height = im.size
        new_width  = 320
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
    async def uploadsticker(self, ctx, name, emoji, link=None):  # upload emoji from emoji url
        limit = ctx.guild.sticker_limit
        sticker_count = len(ctx.guild.stickers)
        free_slots = limit - sticker_count
        if free_slots == 0:
            await ctx.send("No more free slots :(")
        else:    
            await ctx.send(f"{free_slots} slots left :)")
            avi_guild = self.client.get_guild(603147860225032192)
            while avi_guild == None:
                pass
            else:
                admin = disnake.utils.get(avi_guild.roles, name="Admin")
                moderator = disnake.utils.get(avi_guild.roles, name="Moderator")
                avilon = disnake.utils.get(avi_guild.roles, name="Avilon")
            roles = [admin, moderator, avilon]
            if (
                any(role in roles for role in ctx.author.roles)
            ):    
            
                if link == None:
                    print(ctx.message.attachments)  # a list
                    print(ctx.message.reference)
                    if ctx.message.attachments:  # message has images
                        print("is attachment")
                        link = ctx.message.attachments[0].url
                    elif ctx.message.reference is not None:  # message is replying
                        print("is reply")
                        id = ctx.message.reference.message_id
                        msg = await ctx.channel.fetch_message(id)
                        if msg.attachments:  # if replied has image
                            link = msg.attachments[0].url
                        elif msg.embeds:  # if replied has link
                            link = msg.embeds[0].url

                        # print("embmeds: {0}".format(msg.embeds))
                        # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                        #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                        # link= msg.attachments[0].url
                        else:
                            await ctx.send("the message you replied to has no image, baka!")
                    else:
                        await ctx.send("you did something wrong. brug. try again.")
                        return
                    print(link)             
                file, width, height = await self.sticker_resize(link)
                file.seek(0)       
                await ctx.send(f"New image size is: {width}x{height}",delete_after=3.0)
                sticker = await ctx.guild.create_sticker(name=name, emoji=emoji,file=disnake.File(file))
                await ctx.send("Sticker uploaded!",delete_after=3.0)
                await ctx.send(stickers=[sticker])
            else:
                await ctx.send("Only Avi/Admins/Mods can use this command")            
            
def setup(client):
    client.add_cog(EmoteSticker(client))
