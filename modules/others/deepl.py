import disnake
import translators as ts
from disnake.ext import commands
from jisho_api.word import Word

from modules.paginator import ButtonPaginator
from myfunctions.async_wrapper import async_wrap
from typing import Any

class DeepL_commands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["japanese"])
    async def nihongo(self, ctx: commands.Context[Any], *, text=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return
        result = await self.google_translate(text, "ja")
        await ctx.send(result)

    @commands.message_command(name="Nihongo")
    async def msg_nihongo(self, inter, msg: disnake.Message):
        result = await self.google_translate(msg.content, "ja")
        await inter.response.send_message(result)

    @commands.command(aliases=["english", "tr"])
    async def eigo(self, ctx: commands.Context[Any], *, text=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return
        result = await self.google_translate(text, "en")
        await ctx.send(result)

    @commands.message_command(name="Eigo")
    async def msg_eigo(self, inter, msg: disnake.Message):
        result = await self.google_translate(msg.content, "en")
        await inter.response.send_message(result)

    @async_wrap
    def google_translate(self, text, to_language):
        try:
            return ts.google(text, to_language=to_language)
        except TypeError:
            return "I failed lmao"

    @commands.command(aliases=["german"])
    async def doitsu(self, ctx: commands.Context[Any], *, text=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return

        result = await self.google_translate(text, "de")
        await ctx.send(result)

    @commands.message_command(name="Doitsu")
    async def msg_doitsu(self, inter, msg: disnake.Message):
        result = await self.google_translate(msg.content, "de")
        await inter.response.send_message(result)

    @async_wrap
    def jisho_word(self, word):
        return Word.request(word)

    @commands.command()
    async def jisho(self, ctx: commands.Context[Any], query=None):
        if query is None:
            replied_msg = ctx.message.reference
            if replied_msg is not None:  # message is replying
                query = replied_msg.resolved.content
            else:
                await ctx.send("I got nothin to jisho. L.")
                return
        r = await self.jisho_word(query)
        if r is None:
            await ctx.send(f"Could not find anything for `{query}`. Sorry")
            return
        datas = r.dict()["data"]
        embed_list = []
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
    async def say(self, ctx: commands.Context[Any], *, text=None):
        await ctx.message.delete()
        if text:
            await ctx.send(text)
        else:
            await ctx.send("There's no text!")


def setup(client: commands.Bot):
    client.add_cog(DeepL_commands(client))
