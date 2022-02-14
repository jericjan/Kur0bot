from disnake.ext import commands
import disnake
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os
import uuid
import asyncio
from arsenic import get_session, keys, browsers, services
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
from pilmoji import Pilmoji
import textwrap

class Superchat(commands.Cog):
    def __init__(self, client):
        self.client = client
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

    @commands.command(aliases=["akasupa", "supacha"])
    async def superchat(self, ctx, amount, *, message):    
      await ctx.message.delete()
      cur_uuid  = uuid.uuid4()
      bgnMessage = await ctx.send(f"{ctx.author.name} is sending a superchat... <a:ameroll:941314708022128640>")
      message = re.sub(r'<a?(:.+:).+>',r'\1',message)
      service = services.Geckodriver()      
      prefs = {"browser.download.folderList":2,"browser.download.manager.showWhenStarting":False,"browser.download.dir":f'/home/runner/Kur0bot/supers/{cur_uuid}/',"browser.helperApps.neverAsk.saveToDisk":"'image/png","browser.display.use_document_fonts":1}
      browser =  browsers.Firefox(**{"moz:firefoxOptions":{
       'args': ['-headless'],'prefs':prefs,'log':{"level": "trace"}
        # 'prefs':prefs,'log':{"level": "trace"}
    }})
      async with get_session(service, browser) as session:
        await session.get('https://ytsc.leko.moe/')
        await session.set_window_size(800,900)
        select_box = await session.get_element('#color')
        await select_box.select_by_value('red')
        name = await session.get_element('#input-name')
        await name.send_keys(ctx.author.name)
        # screen = await session.get_screenshot()
        # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))
        price = await session.get_element('#input-price')
        await price.send_keys(amount)
        # screen = await session.get_screenshot()
        # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))        
        msg = await session.get_element('#input-text')
        await msg.send_keys(message)
        # screen = await session.get_screenshot()
        # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))        
        img = await session.get_element('#input-avartar')
        await img.send_keys(ctx.author.display_avatar.url)
        await img.send_keys(keys.ENTER) 
        # screen = await session.get_screenshot()
        # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))        
        final = await session.get_element('#superchat')
        await final.click()
        # screen = await session.get_screenshot()
        # await ctx.send(file=disnake.File(screen,filename='screenshot.png'))
        
        while not os.path.exists(f'supers/{cur_uuid}/superchat.png'):
          await asyncio.sleep(1)
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        await webhook.send(file=disnake.File(f'supers/{cur_uuid}/superchat.png'),
            username=ctx.message.author.name,
            avatar_url=ctx.message.author.display_avatar.url,
        )
        #await session.close() closes automatically
        await bgnMessage.delete()
        await webhook.delete()
        os.remove(f'supers/{cur_uuid}/superchat.png')
        os.rmdir(f'supers/{cur_uuid}/')

    @commands.command(aliases=["akasupa2", "supacha2"])
    async def superchat2(self, ctx, amount, *, message):  
      await ctx.message.delete()
      ###TOP BAR
      img = Image.new('RGBA', (1760, 240), color = (208,0,0,255))

      blank = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
      draw = ImageDraw.Draw(blank)
      fnt = ImageFont.truetype("fonts/Roboto-Medium.ttf", 57)
      draw.text((287, 40),ctx.author.name,font=fnt, fill=(255, 255, 255, 179))

      blank2 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
      draw2 = ImageDraw.Draw(blank2)
      fnt2 = ImageFont.truetype("fonts/Roboto-Medium.ttf", 60)
      draw2.text((288, 124),amount,font=fnt2, fill=(255, 255, 255, 255))


      out = Image.alpha_composite(img, blank)
      out = Image.alpha_composite(out, blank2)

      mask = Image.open('masks/circle-mask.png').convert('L')
      response = requests.get(ctx.message.author.display_avatar.url)
      byteio = io.BytesIO(response.content)
      im = Image.open(byteio)      
      imgoutput = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
      byteio.close()
      imgoutput.putalpha(mask)
      blank3 = Image.new("RGBA", (1760, 240), (255, 255, 255, 0))
      blank3.paste(imgoutput, (64, 33))
      out = Image.alpha_composite(out, blank3)

      # byteio = io.BytesIO()
      # byteio.seek(0)
      # out.save(byteio,format='PNG')
      # byteio.seek(0)
      # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
      # byteio.close()
      ###BOTTOM BAR
      msg_split = textwrap.wrap(message,width=57)
      #await ctx.send(f"Splti msgs is: {msg_split}")
      if len(msg_split) == 1:
        supa_height = 152
        print("one line")
      else:
        supa_height = 152  
        print("more than one line")
      # img = Image.new('RGBA', (1760, 152), color = (230,33,23,255))
      img = Image.new('RGBA', (1760, supa_height), color = (230,33,23,255))
      draw = ImageDraw.Draw(img)
      fnt = ImageFont.truetype("fonts/merged.ttf", 60)
      #draw.text((64, 40),message,font=fnt, fill=(255, 255, 255, 255))
      text_size = draw.textsize('\n'.join(msg_split), font=fnt,spacing=28)
      await ctx.send(f"Text size is: {text_size}")
      txt_height = int(re.search(r'(?<=, )\d+',str(text_size)).group())
      txt_width = int(re.search(r'\d+(?=, \d+\))',str(text_size)).group())
      print(f"text heigh: {txt_height}")
      img = img.resize((1760,txt_height+62))
      draw = ImageDraw.Draw(img)
      draw.rectangle([(64, 31), (64+txt_width,31+txt_height)],outline ="black")

      draw.multiline_text((64, 31), '\n'.join(msg_split), fill=(255, 255, 255, 255), font=fnt,spacing=28)

      # with Pilmoji(img) as pilmoji:
      #   pilmoji.text((64, 31), '\n'.join(msg_split), fill=(255, 255, 255, 255), font=fnt,spacing=28)

      # byteio = io.BytesIO()
      # byteio.seek(0)
      # img.save(byteio,format='PNG')
      # byteio.seek(0)
      # await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
      # byteio.close()

      dst = Image.new('RGB', (out.width, out.height + img.height))
      dst.paste(out, (0, 0))
      dst.paste(img, (0, out.height))
      byteio = io.BytesIO()
      byteio.seek(0)
      dst.save(byteio,format='PNG')
      byteio.seek(0)
      await ctx.send(file=disnake.File(byteio,filename='superchat.png'))
      byteio.close()
def setup(client):
    client.add_cog(Superchat(client))
