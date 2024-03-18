import disnake
import translators as ts
from disnake.ext import commands
from jisho_api.word import Word

from modules.paginator import ButtonPaginator
from myfunctions.async_wrapper import async_wrap


class DeepL_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["japanese"])
    async def nihongo(self, ctx, *, text=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return
        result = ts.google(text, to_language="ja")
        await ctx.send(result)

    @commands.command(aliases=["english"])
    async def eigo(self, ctx, *, text=None):
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

    @async_wrap
    def google_translate(self, text, to_language):
        return ts.google(text, to_language=to_language)

    @commands.command(aliases=["german"])
    async def doitsu(self, ctx, *, text=None):
        if text == None:
            if ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                text = msg.content
            else:
                await ctx.send("what am i supposed to translate? try again dawg.")
                return

        result = ts.google(text, to_language="de")
        await ctx.send(result)
    @async_wrap
    def jisho_word(self, word):
        return Word.request(word)

    @commands.command()
    async def jisho(self, ctx, query=None):
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
    async def say(self, ctx, *, text=None):
        await ctx.message.delete()
        if text:
            await ctx.send(text)
        else:
            await ctx.send("There's no text!")


def setup(client):
    client.add_cog(DeepL_commands(client))
