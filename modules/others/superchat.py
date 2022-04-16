from disnake.ext import commands
import disnake

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
import os
import uuid
import asyncio
from arsenic import get_session, keys, browsers, services
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
from pilmoji import Pilmoji

from tqdm import tqdm
import functools
from aiolimiter import AsyncLimiter
import shlex

limiter = AsyncLimiter(1, 1)


class Superchat(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pbar_list = []

    ##################OLD SELENIUM VER########################
    # @commands.command(aliases=["akasupa", "supacha"])
    # async def superchat(self, ctx, amount, *, message):
    #     await ctx.message.delete()
    #     cur_uuid  = uuid.uuid4()
    #     bgnMessage = await ctx.send(f"{ctx.author.name} is sending a superchat...")
    #     chrome_options = Options()
    #     chrome_options.add_argument('--no-sandbox')
    #   #  chrome_options.add_argument('--headless')
    #     prefs = {"profile.default_content_settings.popups": 0,
    #                 "download.default_directory":
    #                             f'/home/runner/Kur0bot/supers/{cur_uuid}',#IMPORTANT - ENDING SLASH V IMPORTANT
    #                 "directory_upgrade": True}
    #     chrome_options.add_experimental_option("prefs", prefs)
    #     driver = webdriver.Chrome(options=chrome_options,executable_path='chromedriver')
    #     driver.get("https://ytsc.leko.moe/")
    #     select = Select(driver.find_element_by_class_name('custom-select'))
    #     select.select_by_value('red')

    #     name = driver.find_element_by_id('input-name')
    #     name.send_keys(ctx.author.name)
    #     price = driver.find_element_by_id('input-price')
    #     price.send_keys(amount)
    #     msg = driver.find_element_by_id('input-text')
    #     msg.send_keys(message)
    #     img = driver.find_element_by_id('input-avartar')
    #     img.send_keys(ctx.author.display_avatar.url)
    #     driver.find_element_by_id('superchat').click()
    #     driver.close()
    #     while not os.path.exists(f'supers/{cur_uuid}/superchat.png'):
    #       pass
    #     webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    #     await webhook.send(file=disnake.File(f'supers/{cur_uuid}/superchat.png'),
    #         username=ctx.message.author.name,
    #         avatar_url=ctx.message.author.display_avatar.url,
    #     )
    #     await bgnMessage.delete()
    #     await webhook.delete()
    #     os.remove(f'supers/{cur_uuid}/superchat.png')
    #     os.rmdir(f'supers/{cur_uuid}/')

    ################CHROME ASYNC VER###################
    # @commands.command(aliases=["akasupa", "supacha"])
    # async def superchat(self, ctx, amount, *, message):
    #   await ctx.message.delete()
    #   cur_uuid  = uuid.uuid4()
    #   bgnMessage = await ctx.send(f"{ctx.author.name} is sending a superchat... <a:ameroll:941314708022128640>")
    #   message = re.sub(r'<a?(:.+:).+>',r'\1',message)
    #   service = services.Chromedriver()
    #   prefs = {"profile.default_content_settings.popups": 0,
    #                 "download.default_directory":
    #                             f'/home/runner/Kur0bot/supers/{cur_uuid}',#IMPORTANT - ENDING SLASH V IMPORTANT
    #                 "directory_upgrade": True}
    #   browser = browsers.Chrome(**{"goog:chromeOptions":{
    #     'args': [ '--disable-gpu','--no-sandbox'],'prefs':prefs
    # }})
    #   async with get_session(service, browser) as session:
    #     await session.get('https://ytsc.leko.moe/')
    #     await session.set_window_size(800,900)
    #     select_box = await session.get_element('#color')
    #     await select_box.select_by_value('red')
    #     name = await session.get_element('#input-name')
    #     await name.send_keys(ctx.author.name)
    #     price = await session.get_element('#input-price')
    #     await price.send_keys(amount)
    #     msg = await session.get_element('#input-text')
    #     await msg.send_keys(message)
    #     img = await session.get_element('#input-avartar')
    #     await img.send_keys(ctx.author.display_avatar.url)
    #     await img.send_keys(keys.ENTER)
    #     final = await session.get_element('#superchat')
    #     await final.click()
    #     # screen = await session.get_screenshot()
    #     # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))

    #     while not os.path.exists(f'supers/{cur_uuid}/superchat.png'):
    #       pass
    #     webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    #     await webhook.send(file=disnake.File(f'supers/{cur_uuid}/superchat.png'),
    #         username=ctx.message.author.name,
    #         avatar_url=ctx.message.author.display_avatar.url,
    #     )
    #     await session.close()
    #     await bgnMessage.delete()
    #     await webhook.delete()
    #     os.remove(f'supers/{cur_uuid}/superchat.png')
    #     os.rmdir(f'supers/{cur_uuid}/')

    @commands.command(aliases=["oldakasupa", "oldsupacha"])
    async def oldsuperchat(self, ctx, amount, *, message):

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
                    "log": {"level": "trace"}
                    # 'prefs':prefs,'log':{"level": "trace"}
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
            # screen = await session.get_screenshot()
            # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))
            price = await session.get_element("#input-price")
            await price.send_keys(amount)
            # screen = await session.get_screenshot()
            # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))
            msg = await session.get_element("#input-text")
            await msg.send_keys(message)
            # screen = await session.get_screenshot()
            # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))
            img = await session.get_element("#input-avartar")
            await img.send_keys(ctx.author.display_avatar.url)
            await img.send_keys(keys.ENTER)
            # screen = await session.get_screenshot()
            # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))
            final = await session.get_element("#superchat")
            await final.click()
            # screen = await session.get_screenshot()
            # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))

            while not os.path.exists(f"supers/{cur_uuid}/superchat.png"):
                await asyncio.sleep(1)
            webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
            await webhook.send(
                file=disnake.File(f"supers/{cur_uuid}/superchat.png"),
                username=ctx.message.author.name,
                avatar_url=ctx.message.author.display_avatar.url,
            )
            # await session.close() closes automatically
            await bgnMessage.delete()
            await webhook.delete()
            os.remove(f"supers/{cur_uuid}/superchat.png")
            os.rmdir(f"supers/{cur_uuid}/")

    #######OLD PILLOW VER
    # @commands.command(aliases=["akasupa2", "supacha2"])
    # async def superchat2(self, ctx, amount, *, message):
    #   await ctx.message.delete()
    #   ###TOP BAR
    #   img = Image.new('RGBA', (1760, 240), color = (208,0,0,255))

    #   blank = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
    #   draw = ImageDraw.Draw(blank)
    #   fnt = ImageFont.truetype("fonts/Roboto-Medium.ttf", 57)
    #   draw.text((287, 40),ctx.author.name,font=fnt, fill=(255, 255, 255, 179))

    #   blank2 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
    #   draw2 = ImageDraw.Draw(blank2)
    #   fnt2 = ImageFont.truetype("fonts/Roboto-Medium.ttf", 60)
    #   draw2.text((288, 124),amount,font=fnt2, fill=(255, 255, 255, 255))

    #   out = Image.alpha_composite(img, blank)
    #   out = Image.alpha_composite(out, blank2)

    #   mask = Image.open('masks/circle-mask.png').convert('L')
    #   response = requests.get(ctx.message.author.display_avatar.url)
    #   byteio = io.BytesIO(response.content)
    #   im = Image.open(byteio)
    #   imgoutput = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    #   byteio.close()
    #   imgoutput.putalpha(mask)
    #   blank3 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
    #   blank3.paste(imgoutput, (64, 33))
    #   out = Image.alpha_composite(out, blank3)

    #   # byteio = io.BytesIO()
    #   # byteio.seek(0)
    #   # out.save(byteio,format='PNG')
    #   # byteio.seek(0)
    #   # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
    #   # byteio.close()
    #   ###BOTTOM BAR
    #   msg_split = textwrap.wrap(message,width=61)
    #   #await ctx.send(f"Splti msgs is: {msg_split}")

    #   # img = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
    #   img = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
    #   draw = ImageDraw.Draw(img)
    #   fnt = ImageFont.truetype("fonts/merged.ttf", 60)
    #   #draw.text((64, 40),message,font=fnt, fill=(255, 255, 255, 255))
    #   text_size = draw.textsize('\n'.join(msg_split), font=fnt,spacing=28)
    #   #await ctx.send(f"Text size is: {text_size}")
    #   txt_height = int(re.search(r'(?<=, )\d+',str(text_size)).group())
    #   txt_width = int(re.search(r'\d+(?=, \d+\))',str(text_size)).group())
    #   print(f"text heigh: {txt_height}")
    #   if len(msg_split) == 1:
    #     print("one line")
    #   else:
    #     print("more than one line")
    #     img = img.resize((1760,txt_height+62))
    #   draw = ImageDraw.Draw(img)
    #   draw.rectangle([(64, 31), (64+txt_width,31+txt_height)],outline ="black")

    #   # draw.multiline_text((64, 31), '\n'.join(msg_split), fill=(255, 255, 255, 255), font=fnt,spacing=28)

    #   with Pilmoji(img) as pilmoji:
    #     pilmoji.text((64, 31), '\n'.join(msg_split), fill=(255, 255, 255, 255), font=fnt,spacing=28)

    #   # byteio = io.BytesIO()
    #   # byteio.seek(0)
    #   # img.save(byteio,format='PNG')
    #   # byteio.seek(0)
    #   # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
    #   # byteio.close()

    #   dst = Image.new('RGB', (out.width, out.height + img.height))
    #   dst.paste(out, (0, 0))
    #   dst.paste(img, (0, out.height))
    #   byteio = io.BytesIO()
    #   byteio.seek(0)
    #   dst.save(byteio,format='PNG')
    #   byteio.seek(0)
    #   await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
    #   byteio.close()

    ######################WE"RE GETTING THERE###########################
    # async def updatebar(self, ctx,msg,content):
    #   try:
    #     await asyncio.wait_for(msg.edit(
    #         content=content
    #     ), timeout=0.2)
    #   except Exception as e:
    #     print(f"timeout!\n{e}")

    # @commands.command(aliases=["akasupa2", "supacha2"])
    # async def superchat2(self, ctx, amount, *, message):
    #   await ctx.message.delete()
    #   bgnMessage = await ctx.send(f"{ctx.author.name} is sending a superchat...")
    #   ###TOP BAR
    #   img = Image.new('RGBA', (1760, 240), color = (208,0,0,255))

    #   blank = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
    #   draw = ImageDraw.Draw(blank)
    #   fnt = ImageFont.truetype("fonts/Roboto-Medium.ttf", 57)
    #   draw.text((287, 40),ctx.author.name,font=fnt, fill=(255, 255, 255, 179))

    #   blank2 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
    #   draw2 = ImageDraw.Draw(blank2)
    #   fnt2 = ImageFont.truetype("fonts/Roboto-Medium.ttf", 60)
    #   draw2.text((288, 124),amount,font=fnt2, fill=(255, 255, 255, 255))

    #   out = Image.alpha_composite(img, blank)
    #   out = Image.alpha_composite(out, blank2)

    #   mask = Image.open('masks/circle-mask.png').convert('L')
    #   response = requests.get(ctx.message.author.display_avatar.url)
    #   byteio = io.BytesIO(response.content)
    #   im = Image.open(byteio)
    #   imgoutput = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    #   byteio.close()
    #   imgoutput.putalpha(mask)
    #   blank3 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
    #   blank3.paste(imgoutput, (64, 33))
    #   out = Image.alpha_composite(out, blank3)

    #   # byteio = io.BytesIO()
    #   # byteio.seek(0)
    #   # out.save(byteio,format='PNG')
    #   # byteio.seek(0)
    #   # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
    #   # byteio.close()
    #   ###BOTTOM BAR
    #   msg_words = message.split(" ")
    #   msg_split = ''
    #   img0 = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
    #   draw0 = ImageDraw.Draw(img0)
    #   fnt0 = ImageFont.truetype("fonts/merged.ttf", 60)
    #   output = io.StringIO()
    #   pbar = tqdm(total=len(msg_words), file=output, ascii=False)

    #   for index,i in enumerate(msg_words):
    #     percentage = (index/len(msg_words))*100
    #     pbar.update(1)
    #     final = output.getvalue()

    #     final1 = final.splitlines()[-1]
    #     print(final1)
    #     aaa = re.findall(
    #         r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1
    #     )[0]

    #     # await bgnMessage.edit(
    #     #     content=f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
    #     # )
    #     try:
    #         asyncio.ensure_future(self.updatebar(ctx,bgnMessage,f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"))
    #         # await bgnMessage.edit(content=f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>")
    #     except:
    #       pass
    #     if index == 0:
    #       temp_str = i
    #     else:
    #       temp_str = f"{msg_split} {i}"

    #     #draw.text((64, 40),message,font=fnt, fill=(255, 255, 255, 255))
    #     text_size = draw0.textsize(temp_str, font=fnt0,spacing=28)
    #     # await ctx.send(f"Text size is: {type(text_size)}")
    #     txt_width = int(text_size[0])
    #     # print(f"width is: {txt_width}")
    #     if int(txt_width) <= 1632:
    #       if index == 0:
    #         msg_split += i
    #       else:
    #         msg_split += f" {i}"
    #     else:
    #       msg_split += f"\n{i}"

    #   pbar.close()
    #   output.close()
    #   #await ctx.send(msg_split)
    #   #await ctx.send(f"Splti msgs is: {msg_split}")

    #   # img = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
    #   img = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
    #   draw = ImageDraw.Draw(img)
    #   fnt = ImageFont.truetype("fonts/merged.ttf", 60)
    #   #draw.text((64, 40),message,font=fnt, fill=(255, 255, 255, 255))
    #   text_size = draw.textsize(msg_split, font=fnt,spacing=28)
    #   #await ctx.send(f"Text size is: {text_size}")
    #   txt_height = int(re.search(r'(?<=, )\d+',str(text_size)).group())
    #   txt_width = int(re.search(r'\d+(?=, \d+\))',str(text_size)).group())
    #   print(f"text heigh: {txt_height}")
    #   if len(msg_split.split('\n')) == 1:
    #     print("one line")
    #   else:
    #     print("more than one line")
    #     img = img.resize((1760,txt_height+62))

    #   ###rectangle
    #   # draw = ImageDraw.Draw(img)
    #   # draw.rectangle([(64, 31), (64+txt_width,31+txt_height)],outline ="black")

    #   # draw.multiline_text((64, 31), '\n'.join(msg_split), fill=(255, 255, 255, 255), font=fnt,spacing=28)

    #   with Pilmoji(img) as pilmoji:
    #     pilmoji.text((64, 31), msg_split, fill=(255, 255, 255, 255), font=fnt,spacing=28)

    #   # byteio = io.BytesIO()
    #   # byteio.seek(0)
    #   # img.save(byteio,format='PNG')
    #   # byteio.seek(0)
    #   # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
    #   # byteio.close()

    #   dst = Image.new('RGB', (out.width, out.height + img.height))
    #   dst.paste(out, (0, 0))
    #   dst.paste(img, (0, out.height))
    #   byteio = io.BytesIO()
    #   byteio.seek(0)
    #   dst.save(byteio,format='PNG')
    #   byteio.seek(0)
    #   await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
    #   byteio.close()
    #   await bgnMessage.delete()
    async def updatebar(self, msg):
        # print("Updating bar...")
        try:

            async with limiter:
                await asyncio.wait_for(msg.edit(content=self.pbar_list[-1]), timeout=1)
                # print("\033[92m SUCCESS! \033[0m")
        except Exception as e:
            if str(e).startswith("404 Not Found"):
                pass
            else:
                # print(f"\033[91m timeout!\n{e} \033[0m")
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
        response = requests.get(pfp)
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
        # byteio = io.BytesIO()
        # byteio.seek(0)
        # out.save(byteio,format='PNG')
        # byteio.seek(0)
        # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
        # byteio.close()
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

        # await bgnMessage.edit(
        #     content=f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
        # )

        temp_str = temp_str.split("\n")[-1]
        # draw.text((64, 40),message,font=fnt, fill=(255, 255, 255, 255))
        text_size = draw0.textsize(temp_str, font=fnt0, spacing=28)
        # await ctx.send(f"Text size is: {type(text_size)}")
        txt_width = int(text_size[0])
        # print(f"width is: {txt_width}")
        return txt_width

    # await ctx.send(msg_split)
    # await ctx.send(f"Splti msgs is: {msg_split}")

    # img = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
    def legacy_blocking_function3(self, msg_split, out):
        spacing = 30
        img = Image.new("RGBA", (1760, 152), color=(230, 33, 23, 255))
        # draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("fonts/merged.ttf", 60)
        # draw.text((64, 40),message,font=fnt, fill=(255, 255, 255, 255))
        with Pilmoji(img) as pilmoji:
            text_size = pilmoji.getsize(text=msg_split, font=fnt, spacing=spacing)
        # await ctx.send(f"Text size is: {text_size}")
        txt_height = int(text_size[1])
        # txt_width = int(re.search(r'\d+(?=, \d+\))',str(text_size)).group())
        # print(f"text heigh: {txt_height}")
        if len(msg_split.split("\n")) == 1:
            # print("one line")
            pass
        else:
            # print("more than one line")
            img = img.resize((1760, txt_height + 92))

        ###rectangle
        # draw = ImageDraw.Draw(img)
        # draw.rectangle([(64, 31), (64+txt_width,31+txt_height)],outline ="black")

        # draw.multiline_text((64, 31), '\n'.join(msg_split), fill=(255, 255, 255, 255), font=fnt,spacing=28)

        with Pilmoji(img) as pilmoji:
            pilmoji.text(
                (64, 31),
                msg_split,
                fill=(255, 255, 255, 255),
                font=fnt,
                spacing=spacing,
            )

        # byteio = io.BytesIO()
        # byteio.seek(0)
        # img.save(byteio,format='PNG')
        # byteio.seek(0)
        # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
        # byteio.close()

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
    async def superchat(self, ctx, amount=None, *, message=None):
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
            # print(final1)
            aaa = re.findall(r"(?<=\d\%)\|.+\| (?=\d+|\d+.\d+/\d+|\d+.\d+)", final1)[0]
            try:
                self.pbar_list.append(
                    f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>"
                )
                asyncio.ensure_future(self.updatebar(bgnMessage))

                # await bgnMessage.edit(content=f"{ctx.author.name} is sending a superchat...\n{round(percentage, 2)}% complete...\n`{aaa}`<a:ameroll:941314708022128640>")
            except:
                pass
        pbar.close()
        output.close()
        bruh = await self.foo3(msg_split, out)
        bruh.seek(0)
        await ctx.send(file=disnake.File(bruh, filename="superchat.png"))
        bruh.close()
        await bgnMessage.delete()


def setup(client):
    client.add_cog(Superchat(client))
