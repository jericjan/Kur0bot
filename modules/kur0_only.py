import json

import aiohttp
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from lorem.text import TextLorem


class AttachmentBulker:
    def __init__(self, ctx, threshold):
        self.ctx = ctx
        self.threshold = threshold
        self.counter = 0
        self.msgs = ""

    async def send(self, msg):
        print("Method to call multiple times")
        self.counter += 1
        self.msgs += msg + "\n"
        if self.counter >= self.threshold:
            await self.ctx.send(self.msgs)
            self.msgs = ""
            self.counter = 0

    async def clean(self):
        if self.msgs != "":
            await self.ctx.send(self.msgs)
            self.msgs = ""
            self.counter = 0
class Kur0only(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.comm_list = []

    @commands.command()
    @commands.is_owner()
    async def makeembed(self, ctx, title, description):
        if description.startswith("https"):
            print("description is url")
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://quiet-sun-6d6e.cantilfrederick.workers.dev/?{description}"
                ) as response:
                    text = await response.text()
            embed = disnake.Embed(title=title, description=text)
            await ctx.send(embed=embed)
            await ctx.message.delete()
        else:
            print("description is text")
            embed = disnake.Embed(title=title, description=description)
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def editembed(self, ctx, msg_id: int, title, description):
        if description.startswith("https"):
            print("description is url")
            msg = await ctx.fetch_message(msg_id)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://quiet-sun-6d6e.cantilfrederick.workers.dev/?{description}"
                ) as response:
                    text = await response.text()
            embed = disnake.Embed(title=title, description=text)
            await msg.edit(embed=embed)
            await ctx.message.delete()
        else:
            print("description is text")
            msg = await ctx.fetch_message(msg_id)
            embed = disnake.Embed(title=title, description=description)
            await msg.edit(embed=embed)
            await ctx.message.delete()

    def get_public_commands(self):
        with open("modules/commands.json", encoding="utf-8") as f:
            data = json.load(f)

        hidden_commands = data["hidden"]
        self.comm_list = []  # list of public commands IN commands.json
        for i in data:
            if i == "hidden":
                pass
            else:
                self.comm_list += data[i]

        return [
            c.name for c in self.client.commands if c.name not in hidden_commands
        ]  # list of public commands IN the bot

    @commands.command()
    @commands.is_owner()
    async def checkhelp(self, ctx):
        public_commandss = self.get_public_commands()
        diffcomms = [c for c in public_commandss if c not in self.comm_list]
        diffcomms_joined = "\n".join(diffcomms)
        await ctx.send(f"Commands missing in help command are:\n{diffcomms_joined}")
        commands_with_help_msg = [
            c.name for c in self.client.get_command("help").commands
        ]
        aliases = [
            a
            for c in self.client.get_command("help").commands
            if c.aliases
            for a in c.aliases
        ]
        print(aliases)
        diffcomms2 = [
            c
            for c in self.comm_list
            if c not in commands_with_help_msg and c not in aliases
        ]
        diffcomms2_joined = "\n".join(diffcomms2)
        await ctx.send(f"Commands without help commands are:\n{diffcomms2_joined}")

    @commands.command()
    @commands.is_owner()
    async def ytbypass(self, ctx, text):
        letters = list(text)
        count = len(letters)
        lorem = TextLorem(wsep=" ", srange=(count, count))
        lorem_list = lorem.sentence().split(" ")
        lorem_list = [f"{x} ({letters[i]})" for i, x in enumerate(lorem_list)]
        lorem_list = " ".join(lorem_list)
        await ctx.send(lorem_list)

    @commands.command()
    @commands.is_owner()
    async def dotenv(self, ctx):
        load_dotenv(override=True)
        await ctx.send("env variables reloaded!")

    @commands.command()
    @commands.is_owner()
    async def editmsg(self, ctx, msg_id: disnake.Message, *, msg):
        await msg_id.edit(content=msg)
        await ctx.send("Done!")

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, ch_id: disnake.TextChannel, *, msg):
        await ch_id.send(msg)
        await ctx.send("Done!")

    @commands.command()
    @commands.is_owner()
    async def attachments(self, ctx, start=0):
        count = 0
        att_bulker = AttachmentBulker(ctx, 5)
        with open("paci_media_2.txt", encoding="utf-8") as f:
            for line in f:
                count += 1
                if count < start:
                    continue
                await att_bulker.send(f"Part 2 #{count}: {line.split('?')[0]}")
            await att_bulker.clean()

def setup(client):
    client.add_cog(Kur0only(client))
