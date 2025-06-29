import asyncio
import uuid
from typing import TYPE_CHECKING, Any, cast

# from modules.others import emote_sticker
import aiohttp
import disnake
from disnake.ext import commands

if TYPE_CHECKING:
    from modules.others.emote_sticker import EmoteSticker

class Kill(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["ill"])
    async def kill(self, ctx: commands.Context[Any], *, target_user: disnake.Member):

        if ctx.author.id == target_user.id:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/809247468084133898/1219308259455012935/3d8.jpg"
            )
            return

        if target_user == self.client.user:
            await ctx.send("You DARE kill me??? FUCK YOU!")
            if not isinstance(ctx.author, disnake.Member):
                await ctx.send("You aren't a member! I can't kill you GRRRRR!")
                return
            target_user = ctx.author            

        kur0_server = await self.client.fetch_guild(1034100571667447860)  # TODO: make this a variable so users can actually change it lmao
        temp_emoji_name = uuid.uuid4()
        target_pfp = target_user.avatar
        if target_pfp is None:
            await ctx.send("Can't find bro's PFP grrrr")
            return
        
        async with aiohttp.ClientSession() as session:
            async with session.get(target_pfp.url) as response:
                img = await response.read()

        emote_sticker = cast(
            "EmoteSticker",
            self.client.get_cog("EmoteSticker")
        )
        file, _width, _height = await emote_sticker.emote_resize(img)

        
        file = file.read()

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

    @kill.error  # type: ignore
    async def mem_error(self, ctx: commands.Context[Any], error: disnake.DiscordException):
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
            ctx._ignore_me_ = True  # type: ignore (gets ignored in event.py's error handler)


def setup(client: commands.Bot):
    client.add_cog(Kill(client))
