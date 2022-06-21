from disnake.ext import commands
import disnake
import translators as ts

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
        result = ts.google(text,to_language='ja')
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
        result = ts.google(text,to_language='en')
        await ctx.send(result)
def setup(client):
    client.add_cog(DeepL_commands(client))
