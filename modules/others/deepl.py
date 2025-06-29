from typing import Any, Optional, cast

import disnake
import translators as ts  # type: ignore
from disnake.ext import commands
from jisho_api.word import Word  # type: ignore

from modules.paginator import ButtonPaginator
from myfunctions.async_wrapper import async_wrap


class DeepL_commands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["japanese"])
    async def nihongo(self, ctx: commands.Context[Any], *, text: Optional[str]=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                if id is None:
                    await ctx.send("I can't find the message to translate. Try again.")
                    return
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return
        result = await self.google_translate(text, "ja")
        await ctx.send(result)

    @commands.message_command(name="Nihongo")  # pyright: ignore[reportUnknownMemberType]
    async def msg_nihongo(self, inter: disnake.ApplicationCommandInteraction[Any], msg: disnake.Message):
        result = await self.google_translate(msg.content, "ja")
        await inter.response.send_message(result)

    @commands.command(aliases=["english", "tr"])
    async def eigo(self, ctx: commands.Context[Any], *, text: Optional[str]=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                if id is None:
                    await ctx.send("I can't find the message to translate. Try again.")
                    return                
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return
        result = await self.google_translate(text, "en")
        await ctx.send(result)

    @commands.message_command(name="Eigo")  # pyright: ignore[reportUnknownMemberType]
    async def msg_eigo(self, inter: disnake.ApplicationCommandInteraction[Any], msg: disnake.Message):
        result = await self.google_translate(msg.content, "en")
        await inter.response.send_message(result)

    @async_wrap
    def google_translate(self, text: str, to_language: str) -> str:
        try:
            res = cast(str, ts.google(text, to_language=to_language))  # pyright: ignore[reportUnknownMemberType]
            return res
        except TypeError:
            return "I failed lmao"

    @commands.command(aliases=["german"])
    async def doitsu(self, ctx: commands.Context[Any], *, text: Optional[str]=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                if id is None:
                    await ctx.send("I can't find the message to translate. Try again.")
                    return                
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return

        result = await self.google_translate(text, "de")
        await ctx.send(result)

    @commands.message_command(name="Doitsu")  # pyright: ignore[reportUnknownMemberType]
    async def msg_doitsu(self, inter: disnake.ApplicationCommandInteraction[Any], msg: disnake.Message):
        result = await self.google_translate(msg.content, "de")
        await inter.response.send_message(result)

    @async_wrap
    def jisho_word(self, word: str):
        return Word.request(word)  # pyright: ignore[reportUnknownMemberType]

    @commands.command()
    async def jisho(self, ctx: commands.Context[Any], query: Optional[str]=None):
        if query is None:
            replied_msg = ctx.message.reference
            if replied_msg is not None:  # message is replying
                if resolved := replied_msg.resolved:
                    if isinstance(resolved, disnake.Message):
                        query = resolved.content
            else:
                await ctx.send("I got nothin to jisho. L.")
                return
        if query is None:
            await ctx.send("I got nothin to jisho. L.")
            return
        
        r = await self.jisho_word(query)
        if r is None:
            await ctx.send(f"Could not find anything for `{query}`. Sorry")
            return
        datas = r.dict()["data"]
        embed_list: list[disnake.Embed] = []
        for data in datas:
            japanese = data["japanese"]
            desc = ""
            for x in japanese:
                word = x["word"]
                if word is None:
                    word = ""
                reading = x["reading"]
                desc += f"**{word} ({reading})**\n"
            senses = data["senses"]
            for idx, x in enumerate(senses):
                eng_def = x["english_definitions"]
                parts_of_speech = x["parts_of_speech"]
                if "Wikipedia definition" in parts_of_speech:
                    if idx == 0:
                        parts_of_speech = ""
                    else:
                        continue
                else:
                    parts_of_speech = f"__{', '.join(parts_of_speech)}__"
                desc += f"{parts_of_speech}\n➤{', '.join(eng_def)}\n"
            embed_list.append(
                disnake.Embed(
                    title=f"You searched for '{query}'",
                    description=desc,
                )
            )
        paginator = ButtonPaginator(segments=embed_list)
        await paginator.send(ctx)

    @commands.command()
    async def say(self, ctx: commands.Context[Any], *, text: Optional[str]=None):
        await ctx.message.delete()
        if text:
            await ctx.send(text)
        else:
            await ctx.send("There's no text!")


def setup(client: commands.Bot):
    client.add_cog(DeepL_commands(client))
