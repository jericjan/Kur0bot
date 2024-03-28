import asyncio
import uuid

# from modules.others import emote_sticker
import aiohttp
import disnake
from disnake.ext import commands


class Kill(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ill"])
    async def kill(self, ctx, *, target_user: disnake.Member):

        if ctx.author.id == target_user.id:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/809247468084133898/1219308259455012935/3d8.jpg"
            )
            return

        if target_user == self.client.user:
            await ctx.send("You DARE kill me??? FUCK YOU!")
            target_user = ctx.author

        kur0_server = await self.client.fetch_guild(1034100571667447860)
        temp_emoji_name = uuid.uuid4()
        target_pfp = target_user.avatar

        async with aiohttp.ClientSession() as session:
            async with session.get(target_pfp.url) as response:
                img = await response.read()

        emote_sticker = self.client.get_cog("EmoteSticker")
        file, width, height = await emote_sticker.emote_resize(img)

        try:
            file = file.read()
        except:
            pass

        temp_emoji = await kur0_server.create_custom_emoji(
            name=str(temp_emoji_name).replace("-", "_")[0:32], image=file
        )
        try:
            msg = await ctx.send(f"{str(temp_emoji)}<:inagun:1219294516415172641>")
            await asyncio.sleep(3)
            await msg.edit(content="💥<:inagun:1219294516415172641>")
            await asyncio.sleep(1)
            await ctx.send(f"{target_user.display_name} is now kil.")
        finally:
            await temp_emoji.delete()

    @kill.error
    async def mem_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            name = error.argument

            if name == "myself" or name == "me":
                await ctx.send(
                    "https://cdn.discordapp.com/attachments/809247468084133898/1219308259455012935/3d8.jpg"
                )
            else:
                await ctx.send(
                    f'Who is this "{name}" person!? I can\'t kill em <:Grr:1199865079672352838>'
                )
            ctx._ignore_me_ = True


def setup(client):
    client.add_cog(Kill(client))
