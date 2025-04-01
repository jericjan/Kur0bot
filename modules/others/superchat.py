import asyncio
import functools
import io
import os
import re
import shlex
import uuid
from typing import Any, Optional

import disnake
import requests
from aiolimiter import AsyncLimiter
from arsenic import browsers, get_session, keys, services
from disnake.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pilmoji import Pilmoji
from tqdm import tqdm

from myfunctions import file_handler

limiter = AsyncLimiter(1, 1)


class Superchat(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.pbar_list = []

    @commands.command(aliases=["oldakasupa", "oldsupacha"])
    @commands.bot_has_permissions(manage_webhooks=True, manage_messages=True)
    async def oldsuperchat(self, ctx: commands.Context[Any], amount, *, message):

        await ctx.message.delete()

        cur_uuid = uuid.uuid4()
        bgnMessage = await ctx.send(
            f"{ctx.author.name} is sending a superchat... <a:ameroll:941314708022128640>"
        )
        message = re.sub(r"<a?(:.+:).+>", r"\1", message)
        service = services.Geckodriver()
        prefs = {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.dir": f"/home/runner/Kur0bot/supers/{cur_uuid}/",
            "browser.helperApps.neverAsk.saveToDisk": "'image/png",
            "browser.display.use_document_fonts": 1,
        }
        browser = browsers.Firefox(
            **{
                "moz:firefoxOptions": {
                    "args": ["-headless"],
                    "prefs": prefs,
                    "log": {"level": "trace"},
                }
            }
        )
        async with get_session(service, browser) as session:
            await session.get("https://ytsc.leko.moe/")
            await session.set_window_size(800, 900)
            select_box = await session.get_element("#color")
            await select_box.select_by_value("red")
            name = await session.get_element("#input-name")
            await name.send_keys(ctx.author.name)
            price = await session.get_element("#input-price")
            await price.send_keys(amount)
            msg = await session.get_element("#input-text")
            await msg.send_keys(message)
            img = await session.get_element("#input-avartar")
            await img.send_keys(ctx.author.display_avatar.url)
            await img.send_keys(keys.ENTER)
            final = await session.get_element("#superchat")
            await final.click()

            while not os.path.exists(f"supers/{cur_uuid}/superchat.png"):
                await asyncio.sleep(1)
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                file=disnake.File(f"supers/{cur_uuid}/superchat.png"),
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
            await bgnMessage.delete()
            await webhook.delete()
            file_handler.delete_file(f"supers/{cur_uuid}/superchat.png")
            os.rmdir(f"supers/{cur_uuid}/")

    async def updatebar(self, msg):

        try:

            async with limiter:
                await asyncio.wait_for(msg.edit(content=self.pbar_list[-1]), timeout=1)

        except Exception as e:
            if str(e).startswith("404 Not Found"):
                pass
            else:

                pass
            pass

    def legacy_blocking_function(self, user, amount, msg, pfp, bgnMessage):
        ###TOP BAR
        img = Image.new("RGBA", (1760, 240), color=(208, 0, 0, 255))

        blank = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
        draw = ImageDraw.Draw(blank)
        fnt = ImageFont.truetype("fonts/Roboto-Medium.ttf", 57)
        draw.text((287, 40), user, font=fnt, fill=(255, 255, 255, 179))

        blank2 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
        draw2 = ImageDraw.Draw(blank2)
        fnt2 = ImageFont.truetype("fonts/Roboto-Medium.ttf", 60)
        draw2.text((288, 124), amount, font=fnt2, fill=(255, 255, 255, 255))

        out = Image.alpha_composite(img, blank)
        out = Image.alpha_composite(out, blank2)

        mask = Image.open("masks/circle-mask.png").convert("L")
        response = requests.get(pfp)  # threaded
        byteio = io.BytesIO(response.content)
        im0 = Image.open(byteio)
        im0.seek(0)

        im = Image.new("RGBA", im0.size, (208, 0, 0, 255))
        im.paste(im0, (0, 0), im0.convert("RGBA"))
        im.seek(0)
        im.convert("RGB")
        imgoutput = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        byteio.close()
        imgoutput.putalpha(mask)
        blank3 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
        blank3.paste(imgoutput, (64, 33), imgoutput.convert("RGBA"))

        out = Image.alpha_composite(out, blank3)
        img0 = Image.new("RGBA", (1760, 152), color=(230, 33, 23, 255))
        draw0 = ImageDraw.Draw(img0)
        fnt0 = ImageFont.truetype("fonts/merged.ttf", 60)
        return draw0, fnt0, out

        ###BOTTOM BAR

    def legacy_blocking_function2(
        self,
        index,
        msg_words,
        temp_str,
        draw0,
        fnt0,
        user,
        amount,
        msg,
        pfp,
        bgnMessage,
    ):

        temp_str = temp_str.split("\n")[-1]

        text_size = draw0.textsize(temp_str, font=fnt0, spacing=28)

        txt_width = int(text_size[0])

        return txt_width

    def legacy_blocking_function3(self, msg_split, out):
        spacing = 30
        img = Image.new("RGBA", (1760, 152), color=(230, 33, 23, 255))
        fnt = ImageFont.truetype("fonts/merged.ttf", 60)
        with Pilmoji(img) as pilmoji:
            text_size = pilmoji.getsize(text=msg_split, font=fnt, spacing=spacing)
        txt_height = int(text_size[1])
        if len(msg_split.split("\n")) == 1:
            pass
        else:
            img = img.resize((1760, txt_height + 92))

        with Pilmoji(img) as pilmoji:
            pilmoji.text(
                (64, 31),
                msg_split,
                fill=(255, 255, 255, 255),
                font=fnt,
                spacing=spacing,
            )

        dst = Image.new("RGB", (out.width, out.height + img.height))
        dst.paste(out, (0, 0))
        dst.paste(img, (0, out.height))
        byteio = io.BytesIO()
        byteio.seek(0)
        dst.save(byteio, format="PNG")
        byteio.seek(0)
        return byteio

    def run_in_executor(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: f(*args, **kwargs))

        return inner

    @run_in_executor
    def foo(self, user, amount, msg, pfp, bgnMessage):  # Your wrapper for async use
        draw0, fnt0, out = self.legacy_blocking_function(
            user, amount, msg, pfp, bgnMessage
        )
        return draw0, fnt0, out

    @run_in_executor
    def foo2(
        self,
        index,
        msg_words,
        temp_str,
        draw0,
        fnt0,
        user,
        amount,
        msg,
        pfp,
        bgnMessage,
    ):  # Your wrapper for async use
        txt_width = self.legacy_blocking_function2(
            index, msg_words, temp_str, draw0, fnt0, user, amount, msg, pfp, bgnMessage
        )
        return txt_width

    @run_in_executor
    def foo3(self, msg_split, out):
        byteio = self.legacy_blocking_function3(msg_split, out)
        return byteio

    @commands.command(aliases=["akasupa", "supacha"])
    @commands.bot_has_permissions(manage_messages=True)
    async def superchat(self, ctx: commands.Context[Any], amount: Optional[str] = None, *, message: Optional[str] = None):
        if ctx.message.attachments:  # if there are attachments
            attachment_type = ctx.message.attachments[0].content_type
            print(f"attachment is {attachment_type}")
            if attachment_type == "text/plain; charset=utf-8":
                print("IS TEXT FILE!")
                content = await ctx.message.attachments[0].read()
                txt_split = shlex.split(content.decode("utf-8"))
                txt_split[1:] = [" ".join(txt_split[1:])]
                amount, message = txt_split

        elif amount is None or message is None:
            command = self.client.get_command("help superchat")
            ctx.command = command
            ctx.invoked_subcommand = command
            await self.client.invoke(ctx)
            return

        await ctx.message.delete()
        bgnMessage = await ctx.send(f"{ctx.author.name} is sending a superchat...")
        draw0, fnt0, out = await self.foo(
            ctx.author.name,
            amount,
            message,
            ctx.message.author.display_avatar.url,
            bgnMessage,
        )
        msg_words = message.split(" ")
        msg_split = ""
        output = io.StringIO()
        pbar = tqdm(total=len(msg_words), file=output, ascii=False)
        for index, i in enumerate(msg_words):

            if index == 0:
                temp_str = i
            else:
                temp_str = f"{msg_split} {i}"
            txt_width = await self.foo2(
                index,
                msg_words,
                temp_str,
                draw0,
                fnt0,
                ctx.author.name,
                amount,
                message,
                ctx.message.author.display_avatar.url,
                bgnMessage,
            )
            if int(txt_width) <= 1632:
                if index == 0:
                    msg_split += i
                else:
                    msg_split += f" {i}"
            else:
                msg_split += f"\n{i}"
            percentage = (index / len(msg_words)) * 100
            pbar.update(1)
            final = output.getvalue()

            final1 = final.splitlines()[-1]
            aaa = re.findall(r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1)[0]
            try:
                self.pbar_list.append(
                    f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                )
                asyncio.ensure_future(self.updatebar(bgnMessage))
            except:
                pass
        pbar.close()
        output.close()
        bruh = await self.foo3(msg_split, out)
        bruh.seek(0)
        await file_handler.send_file(ctx, bgnMessage, bruh, "superchat.png")
        bruh.close()


def setup(client: commands.Bot):
    client.add_cog(Superchat(client))
