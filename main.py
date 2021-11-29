import discord
from discord.ext import commands
import os
import json
from keep_alive import keep_alive
import random
import asyncio
import aiohttp
import subprocess
from gtts import gTTS
from datetime import datetime, timedelta, timezone
from shlex import quote
from shlex import join as shjoin
import schedule
import threading
import time
import io
import math
import re

#client = discord.Client()
intents = discord.Intents().default()
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix='k.',intents=intents)
client.remove_command("help")
sus_words = [
  "amongus", 
  "аmongus",
  "among us", 
  "аmong us",
  "sus", 
  "sussy", 
  "suspicious", 
  "amogus",
  "аmogus",
  "imposter",
  "impostor"
  ]

sus_replies = [
  "that's pretty sus, bro",
  "sus",
  "you sussy baka",
  "AMOGUS!!! SO SUS!!",
  "sus gaming"
]

pass_words = [
  "password",
  "pass word"
]  

sugma_replies = [
 "sugma balls!! hahahaaaaa",
 "sugma.... sugma balls!!!!!!!"
]

sugoma_replies = [
 "sugoma balls!! hahahaaaaa",
 "sugoma.... sugoma balls!!!!!!!"
]

custom_words = [
 "amgus",
 "amogus",
 "sushi",
 "pog"
]

may_sounds = [
"sounds/totsugeki_7UWR0L4.mp3",
  "sounds/totsugeki-may-2.mp3"
]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="sus gaming | k.help"))
    avi_guild = client.get_guild(603147860225032192)
    while avi_guild == None:
      avi_guild = client.get_guild(603147860225032192)
    else:  
      print(avi_guild)
      avibot = avi_guild.get_member(855897776125640704)
      while avibot == None:
        avibot = avi_guild.get_member(855897776125640704)
      else:  
        if avibot.status is discord.Status.offline:
          print('avibot ded')
         # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
         # msg_id = 887707057808085042
          #msg = await channel.fetch_message(msg_id)
          vc = client.get_guild(603147860225032192).get_channel(887717074191937667)
          #await msg.edit(content="avi bot dead temporarily. password no work. so tell them that as well.")
         # staffch = client.get_guild(603147860225032192).get_channel(812666568613167125)
          await vc.edit(name='AviBot: dead')
         # await staffch.send('<@97122523086340096> bot ded')
        if avibot.status is discord.Status.online:  
          print('avi bot bac')
         # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
         # msg_id = 887707057808085042
         # msg = await channel.fetch_message(msg_id)
          vc = client.get_guild(603147860225032192).get_channel(887717074191937667)
         # await msg.edit(content="AviBot is online. (ignore this)")    
          await vc.edit(name='AviBot: alive')


client.sus_on = False

@client.event
async def on_member_update(before, after):
    if before.status is discord.Status.online and after.status is discord.Status.offline and after.guild == client.get_guild(603147860225032192):
      if after.id == 855897776125640704:
        print(after.id)
        print('avi bot ded')
       # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
      #  msg_id = 887707057808085042
       # msg = await channel.fetch_message(msg_id)
        vc = client.get_guild(603147860225032192).get_channel(887717074191937667)
       # await msg.edit(content="avi bot dead temporarily. password no work. so tell them that as well.")
       # staffch = client.get_guild(603147860225032192).get_channel(812666568613167125)
        await vc.edit(name='AviBot: dead')
        #await staffch.send('<@97122523086340096> bot ded')
    elif before.status is discord.Status.offline and after.status is discord.Status.online:
      if after.id == 855897776125640704:
        print(after.id)
        print('avi bot bac')
       # channel = client.get_guild(603147860225032192).get_channel(836222286432043018)  # notification channel
       # msg_id = 887707057808085042
       # msg = await channel.fetch_message(msg_id)
        vc = client.get_guild(603147860225032192).get_channel(887717074191937667)
       # await msg.edit(content="AviBot is online. (ignore this)")    
        await vc.edit(name='AviBot: alive')
    

@client.listen('on_message')
async def sus(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
   # if message.channel.id == 836222286432043018: #verification
   #   if message.content.startswith('+verify'):
   #    if not message.content.startswith('+verify poggus'):
   #      if any(word in msg for word in pass_words):
   #       await message.delete()
   #       nono = await message.channel.send('Booba! The password is not password!')   
   #       await asyncio.sleep(3)
   #       await nono.delete()
   #      else:
   #       await message.delete()
   #       nono = await message.channel.send#('https://media.tenor.com/images/e2791267b28c9e57b6966bacb65578e9/tenor.gif')
   #       await asyncio.sleep(2)
   #       await nono.delete()
   #    else:
   #     await message.delete()
   #   else:   
   #     await asyncio.sleep(1)
   #     print(message.channel.id)
  #      await message.delete()
    if message.channel.id == 850380119646142504:  #sus-town
      if any(word in msg for word in sus_words):
        for x in range(3):
          await message.channel.send(random.choice(sus_replies))
    else:  
      if not any(word in msg for word in custom_words):
        if any(word in msg for word in sus_words):
          if client.sus_on== False:
            await message.channel.send(random.choice(sus_replies), delete_after=3.0)
          if client.sus_on:
            await message.channel.send(random.choice(sus_replies))
      else:      
        if "amgus" in msg:
          await message.channel.send(random.choice(sugma_replies), delete_after=3.0)
        if "amogus" in msg:
          await message.channel.send(random.choice(sugoma_replies), delete_after=3.0)
        if "sushi" in msg:
          await message.channel.send('remove the hi from sushi. what do you get? <:sus:850628234746920971>', delete_after=3.0)
        if "pog" in msg:
          await message.channel.send('poggusus', delete_after=3.0)  
        
@client.listen('on_message')
async def sus2(message):
    if message.author == client.user:
        return
    msg = message.content.lower()        
    if "twitter.com" in msg:
      print("twitter link!")
      args = ["youtube-dl","-j",msg]
      print(args)
      proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
      stdout_value = proc.stdout.read() + proc.stderr.read()
      json_list = json.loads(stdout_value)
      ext = json_list['ext']
      webpageurl = json_list["webpage_url"]
      print(ext)
      if ext == 'mp4' and 'twitter.com' in webpageurl:
        m1 = await message.channel.send("Beep boop! That is a twitter video!")
        await asyncio.sleep(.1)
        m2 = await message.channel.send('Imma give direct video link...')
        args = ["youtube-dl","--get-url",msg]
        print(args)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()
        await message.channel.send(stdout_value.decode("utf-8"))
        await m1.delete()
        await m2.delete()
          #json_list = json.loads(mixed_Slist[0])
          #title = json_list['ext']
          #print(title)
          
@client.listen('on_message')
async def sus3(message):
    if message.author == client.user:
        return
    msg = message.content.lower()        
    if msg.startswith('] '):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg)
        with open('sounds/tts.mp3', 'wb') as f:
              tts.write_to_fp(f)  
        voice = discord.utils.get(client.voice_clients, guild=message.guild)          
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
              vc = await voice_channel.connect()
              vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 
            else:
              voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith('] '):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg[3:], lang='en', tld='com.au')
        with open('sounds/tts.mp3', 'wb') as f:
              tts.write_to_fp(f)  
        voice = discord.utils.get(client.voice_clients, guild=message.guild)          
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
              vc = await voice_channel.connect()
              vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 
            else:
              voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))            
    if msg.startswith(']uk '):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg[3:], lang='en', tld='co.uk')
        with open('sounds/tts.mp3', 'wb') as f:
              tts.write_to_fp(f)  
        voice = discord.utils.get(client.voice_clients, guild=message.guild)          
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
              vc = await voice_channel.connect()
              vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 
            else:
              voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))
    if msg.startswith(']in '):
        voice_channel = message.author.voice.channel
        channel = None
        tts = gTTS(msg[3:], lang='en', tld='co.in')
        with open('sounds/tts.mp3', 'wb') as f:
              tts.write_to_fp(f)  
        voice = discord.utils.get(client.voice_clients, guild=message.guild)          
        if voice_channel != None:
            channel = voice_channel.name
            if voice == None:
              vc = await voice_channel.connect()
              vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 
            else:
              voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))  
                               
@client.command()
async def bulk(ctx, number):
  print(ctx.channel.id)
  if ctx.channel.id == 850380119646142504:
    for x in range(int(number)):
      await ctx.send(random.choice(sus_replies))
  else:
    await ctx.send("Only usable in <#850380119646142504> <:sus:850628234746920971>")

@client.command()
async def on(ctx):
    client.sus_on = True
    await ctx.send('Permanent Sus enabled!')

@client.command()
async def off(ctx):
    client.sus_on = False
    await ctx.send('Permanent Sus disabled!')

@client.command()
async def glasses(ctx):
  await ctx.send('Glasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist\'s glasses and putting them on like, "Haha, got your glasses!" That\'s just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it\'s amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It\'s actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It\'s like you\'re enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don\'t. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?')  

@client.command()
async def nene(ctx):
  await ctx.send('Super Hyper Ultra Ultimate Deluxe Perfect Amazing Shining God 東方不敗 Master Ginga Victory Strong Cute Beautiful Galaxy Baby 無限 無敵 無双 NENECHI')

@client.command()
async def nenelong(ctx):
  await ctx.send('Super Hyper Ultra Ultimate Deluxe Perfect Amazing Shining God 東方不敗 Master Ginga Victory Strong Cute Beautiful Galaxy Baby 無限 無敵 無双 Nenechi, with 5 Hololive auditions, 43 wives, 400k husbands, neverending IQ (π), Perfect Japanglish, and Spanish, and Portuguese, running on a 3080x Asacoco Antenna and wearing the new ultra rare 5-Star Isekai Princess skin, cofounder of world-famous Polka Hologram Circus, with infinite source of water and surprising gaming skills while able to sing La Lion and set herself on fire in Craftopia after having become the eternal CEO of Nenepro who punches and kicks every employee, after having disconnected while singing Connect with Kiara, as well as having her name flipped into ƎИƎИ and turned into a 3D cardboard decoy, unlocked the power of God from absorbing Matsuri’s snot on her body while I wearing a sexy bikini and having eaten Haachama\'s tarantula-spicy-noodles while convincing Ame to trast her and having mastered singing Shiny Smiley Story in 11 different languages at the same time, right after marathoning iCarly and VICTORIOUS twice in a row, great Idol, the Ina-perishable, ƎNƎN, The Great CEO of ƎNƎN, CEO of CEOs, Opener of the Nether, Wielder of the Divine Lava, Punisher of Chat, The Great Unifier, Commander of the Golden Dumpling, Sacred of Appearance, Bringer of Light, O\'Riend of Chicken, Builder of Cities, Protector of the Two Streams, Keeper of the Hours, Chosen of Aloe, High Stewardess of the Horizon, Sailor of the Great Sea, Sentinel of the Holo Servers, The Undisputed, Begetter of the Begat, Scourge of the Matsuriless, Kusotori-feeder, First of the Mariokart, Rider of the Sacred Chariot, Vanquisher of Hachaama food, Champion of the Stream, Mighty Botan of the Infinite Desert, Emperor of the Shishiron, She Who Holds The Sceptre, Great Hawk Of The Heavens, Arch-Lady of Atalan, Waker of the Shubangelion, Queen Regent of the Sky, Majestic Empress of the Shifting Sands, Champion of the Desert Matsuris, Breaker of the Oni Clans,')
  await ctx.send('Builder of the Great Trap, Terror of the Villager, Master of the Never-Ending Horizon, Master of the Pekodam, Taker of Souls, Tyrant to the Foolish, Bearer of Polka\'s Holy Instrument, Scion of Matsuri, Scion of Nenechi, The (Dis)Connected, Chaser of Nightmares, Keeper of the Smile, Founder of the Nenechi Cult, Banisher of the Grand Horny, High Lady Admiral of the Houshou Pirates, Guardian of the La-Lion Pass, Tamer of the Tako Queen, Living Dumpling Lady, Dismisser of the Foxburger, Charioteer of the Matsuris, She Who Does Not Serve, Slayer off Reddittras, Apex Purger, Favoured of Lamy, Player of the Great Game, Liberator of Life, Lady Sand, Wrangler of Fennecs, Empress of the Dunes, Eternal Sovereign of Husbands Legions, Seneschal of the Great Sandy Desert, Curserer of the 300k Vtuber, Queen Regent of the Pineapple Pizza, Warden of the Eternal Nenepolis, Herald of all Heralds, Caller of the Bitter Win, Matsuri-Tamer, CEO of the Karaoke Stream, Guardian of the Deadbeats, Great Keeper of the Gyoza, Husband of the Tako Princess, Belated of Wakers, General of the Mighty Frame, Summoner of Subscribers, Wife of all Husbands, Princess of Desk-kun, Tyrant of Minecraft, Purger of the Phantom, Killer of the False Matsuri\'s Champions, Tyrant of the Golden Dumpling, Golden Dumpling Lady, Forgotten of the Left4Dead2, Kusotori Mistress, Eternal Warden of ƎNƎN\'s Lands, Breaker of Haachama\'s Bonds, Lord of The NENEngine, Everconductor of The Momotaro Nenechi.')

@client.command()
async def megasus(ctx):
  await ctx.send("I can\'t fucking believe this. Pink from \'Among Us\' ruined my marriage.\n\nA couple months ago, my wife said she was going out for a ladies\' night. She asked me to take care of my son, so I immediately obliged. \"Yes Ma\'am,\" I told her. After a while of waiting, she finally left and I could play my favourite game, Among Us. I hopped on my laptop, booted it up and my desktop loaded, complete with the \'Red Sus\' background and all my Among Us Impostor fan-art. I was shaking in excitement. I slowly dragged my finger across the track pad, and watched the cursor as it glided over to the Among Us icon. Among Us. My absolute favourite game of all time and quite possibly the best and most well-made game in the entire world. As I clicked the button my body twitched with joy at the thought of being the impostor again. My fingers drummed impatiently on my desk as the Innersloth logo faded in, and then out. Then the main title appeared. I immediately looked at pink as she slowly floated across the screen. Oh, how I wish I could feel those luscious, soft asscheeks. Pink is my queen. The real woman in my life. My wife could never be as sexy as Pink is; her soft footfalls in electrical as I peek at her curvy form from inside a vent, waiting for the right time to strike. I could never get close to Pink, however, as if she had some kind of sixth sense, she would always leave before I could reveal myself to her as the impostor. I press Practice, to warm up my fingers before my first intense game of Among Us. I hit Blue in Comms, then cross the hall and vent to Specimen, murdering Green in cold blood. The thrill of killing an animated character in an online game has never been such a rush. I then move towards Reactor, stabbing Yellow in the back and then running down the corridor to the right to access Decontamination. I move quietly through the halls, like a snake about to strike its prey, and I see- Oh no. It\'s Pink. Standing there motionlessly as I face her directly. Her vis")
  await ctx.send("or shows no emotion. But she knows. I can feel it in the air. I can\'t kill her. She is too beautiful, too angelic, the light reflecting off of her pink bodysuit, like stars on a voided sky. She doesn\'t run. I am moved to tears as I caress the screen, kissing it tenderly. \"Goodbye, Pink. See you soon. It will all be okay,\" I whisper in a soft, reassuring voice. Then as my cursor hovers over the kill button, I hesitate. Thoughts of love go through my head. Red having reddish-pink sus children with Pink. But I have to. As the impostor, it is my duty to kill. I press the \'Kill\' button and watch as my character beheads Pink silently. All I hear is the spurt of blood. There is no rush. There is only Red, standing by himself in Fuel. Pink\'s lifeless body laying on the floor beside him. I feel nothing at first, then immense sadness, like I\'m at a loved one\'s funeral. My son knocks on the door, interrupting my brief moment of mourning. He asks, \"Dad? Are you going to make me a snack?\" I tell him to shut up, and my voice cracks. I break down sobbing. I killed her. I killed my one true love. God, forgive me. I open the door to my son, and he has a confused look on his face. I say nothing, and walk to the kitchen to make him a sandwich. Tears roll off my face into the bread as I lay it onto the counter. Lettuce, cheese and meat, followed by a sad swirl of mustard on top. My son is quiet. He sits on the couch, and stares at the floor. There is a depressing air around us. I serve him the sandwich and walk back to my room, contemplating life. If I killed Pink, how am I to be trusted around my family? I cry for hours, and finally my wife comes back. She sees me bawling on the bed like a child who dropped his ice cream. She then asks me why I\'m crying and mutter, \"I killed her. I killed my only love, Pink, in Among Us.\" She is filled with rage and slaps me across my face. I feel numb. She asks for a divorce. I don\'t reply. Instead, I take my laptop and get into my car")
  await ctx.send(", driving to a nearby hotel. Fast forward a few months to the divorce. It was quick and painless. After court, I ask my former wife to take me back.\n\n​\n\n\"I can\'t take you back. You\'ve always been this way. I was sus of you from the start.\"")

@client.command()
async def stopamongus(ctx):
  await ctx.send("STOP POSTING ABOUT AMONG US! I\'M TIRED OF SEEING IT! MY FRIENDS ON TIKTOK SEND ME MEMES, ON DISCORD IT\'S FUCKING MEMES! I was in a server, right? and ALL OF THE CHANNELS were just among us stuff. I-I showed my champion underwear to my girlfriend and t-the logo I flipped it and I said \"hey babe, when the underwear is sus HAHA DING DING DING DING DING DING DING DI DI DING\" I fucking looked at a trashcan and said \"THAT\'S A BIT SUSSY\" I looked at my penis I think of an astronauts helmet and I go \"PENIS? MORE LIKE PENSUS\" AAAAAAAAAAAAAAHGESFG")

@client.command()
async def confession(ctx):
  await ctx.send('Fubuki! Fubuki FUBUKI FUBUKIIIIiiiiIIIIIIiiiiaaAAAaaAAa!!! UhUUUHHHHhhHHH! Unh! Uhhhhhh! FUBUKI FUBUKI FUBUKIIIIiiiiiaaaAAAuuUUUuh!!! Ah-Kunkakunka! Kunkakunka! Suu-HA! Suu-HA! Suu-HA! SUU-HAaa! Fubuki smells so good! Nyunhahahuh! Ahun! I want to smell the white tail of Fubuki! Kun-kun! Ahh! No! I want to rub her fur! Mofmof-mofmof-mofmof-mofmof! Fubuki doing self-intro was so cute! Ahh ahh ahhHHUUUHH! It\'s great you got so many gifts on your birthday, Fubukiii! Ahh-you\'re so cute, Fubuki! Kawaii-AAAHHHHH! Congrats on getting selling your own merch! aaaaiiiYYYYYAAAAAaaaaaaa! Nyahhhhhhhh-GUEEEEHH-AAAAAA! What? VTubers are not real? Hmmm, so Matsuri and Shion aren\'t either... f u b u k i i s n o t r e a l...? GyaaaaAAAAaaaAAAAAaaa! WhyyYYYYyyyYYYyy! HOLOLIVE-EEEHHHH! You bastard! Goodbye! Goodbye to this goddamn world! Huh? She\'s looking? Fubuki on the poster is looking at Matsuri! FUBUKI ON THE POSTER IS LOOKING AT MATSURI!! Fubuki is looking at Matsuri! FUBUKI ON YOUTUBE IS LOOKING AT MATSURI!!! Fubuki on Twitter is talking with Matsuri! Thank God! The world hasn\'t left me! YaHOOOooo! Fubuki is still with me! I did it! I can do it! Twitter\'s Fubuking-YYAAAAAAAAaaaa!!!! Uuhhuhh! Haato-sama! Aki Aki! Melu melu! Roboco-senpaiiiiaaaaii!! Send Matsuri\'s love to Fubuki! To Fubuki from Hololive!')
  
@client.command()
async def fortnite(ctx):
  message = await ctx.send('⠀⠀⠀⠀⣀⣤\n⠀⠀⠀⠀⣿⠿⣶\n⠀⠀⠀⠀⣿⣿⣀\n⠀⠀⠀⣶⣶⣿⠿⠛⣶\n⠤⣀⠛⣿⣿⣿⣿⣿⣿⣭⣿⣤\n⠒⠀⠀⠀⠉⣿⣿⣿⣿⠀⠀⠉⣀\n⠀⠤⣤⣤⣀⣿⣿⣿⣿⣀⠀⠀⣿\n⠀⠀⠛⣿⣿⣿⣿⣿⣿⣿⣭⣶⠉\n⠀⠀⠀⠤⣿⣿⣿⣿⣿⣿⣿\n⠀⠀⠀⣭⣿⣿⣿⠀⣿⣿⣿\n⠀⠀⠀⣉⣿⣿⠿⠀⠿⣿⣿\n⠀⠀⠀⠀⣿⣿⠀⠀⠀⣿⣿⣤\n⠀⠀⠀⣀⣿⣿⠀⠀⠀⣿⣿⣿\n⠀⠀⠀⣿⣿⣿⠀⠀⠀⣿⣿⣿\n⠀⠀⠀⣿⣿⠛⠀⠀⠀⠉⣿⣿\n⠀⠀⠀⠉⣿⠀⠀⠀⠀⠀⠛⣿\n⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⣿⣿\n⠀⠀⠀⠀⣛⠀⠀⠀⠀⠀⠀⠛⠿⠿⠿\n⠀⠀⠀⠛⠛')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⣀⣶⣀\n⠀⠀⠀⠒⣛⣭\n⠀⠀⠀⣀⠿⣿⣶\n⠀⣤⣿⠤⣭⣿⣿\n⣤⣿⣿⣿⠛⣿⣿⠀⣀\n⠀⣀⠤⣿⣿⣶⣤⣒⣛\n⠉⠀⣀⣿⣿⣿⣿⣭⠉\n⠀⠀⣭⣿⣿⠿⠿⣿\n⠀⣶⣿⣿⠛⠀⣿⣿\n⣤⣿⣿⠉⠤⣿⣿⠿\n⣿⣿⠛⠀⠿⣿⣿\n⣿⣿⣤⠀⣿⣿⠿\n⠀⣿⣿⣶⠀⣿⣿⣶\n⠀⠀⠛⣿⠀⠿⣿⣿\n⠀⠀⠀⣉⣿⠀⣿⣿\n⠀⠶⣶⠿⠛⠀⠉⣿\n⠀⠀⠀⠀⠀⠀⣀⣿\n⠀⠀⠀⠀⠀⣶⣿⠿')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⣿⠶⠀⠀⣀⣀\n⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣶⣿⣿⣿⣿⣿⣿\n⠀⠀⣀⣶⣤⣤⠿⠶⠿⠿⠿⣿⣿⣿⣉⣿⣿\n⠿⣉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣤⣿⣿⣿⣀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣶⣤\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⣿⣿⣿⠿⣛⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠛⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⣿⠿⠀⣿⣿⣿⠛\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠿⣿⠀⠀⣿⣶\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠛⠀⠀⣿⣿⣶\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⠤\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⣀\n⠀⠿⣿⣿⣀\n⠀⠉⣿⣿⣀\n⠀⠀⠛⣿⣭⣀⣀⣤\n⠀⠀⣿⣿⣿⣿⣿⠛⠿⣶⣀\n⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⣉⣶\n⠀⠀⠉⣿⣿⣿⣿⣀⠀⠀⣿⠉\n⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿\n⠀⣀⣿⣿⣿⣿⣿⣿⣿⣿⠿\n⠀⣿⣿⣿⠿⠉⣿⣿⣿⣿\n⠀⣿⣿⠿⠀⠀⣿⣿⣿⣿\n⣶⣿⣿⠀⠀⠀⠀⣿⣿⣿\n⠛⣿⣿⣀⠀⠀⠀⣿⣿⣿⣿⣶⣀\n⠀⣿⣿⠉⠀⠀⠀⠉⠉⠉⠛⠛⠿⣿⣶\n⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿\n⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉\n⣀⣶⣿⠛')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣿⣿⣿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣶⣿⣿⣿⣶⣶⣤⣶⣶⠶⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣤⣿⠿⣿⣿⣿⣿⣿⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠛⣿⣤⣤⣀⣤⠿⠉⠀⠉⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠉⠉⠉⠉⠉⠀⠀⠀⠀⠉⣿⣿⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣛⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣶⣿⣿⠛⠿⣿⣿⣿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣿⠛⠉⠀⠀⠀⠛⠿⣿⣿⣶⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠛⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⣿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠉⠉⠀⠀⠀⠀')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⠀⠀⣤⣶⣶\n⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣀⣀\n⠀⠀⠀⠀⠀⣀⣶⣿⣿⣿⣿⣿⣿\n⣤⣶⣀⠿⠶⣿⣿⣿⠿⣿⣿⣿⣿\n⠉⠿⣿⣿⠿⠛⠉⠀⣿⣿⣿⣿⣿\n⠀⠀⠉⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣤⣤\n⠀⠀⠀⠀⠀⠀⠀⣤⣶⣿⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⣀⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿\n⠀⠀⠀⠀⣀⣿⣿⣿⠿⠉⠀⠀⣿⣿⣿⣿\n⠀⠀⠀⠀⣿⣿⠿⠉⠀⠀⠀⠀⠿⣿⣿⠛\n⠀⠀⠀⠀⠛⣿⣿⣀⠀⠀⠀⠀⠀⣿⣿⣀\n⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠿⣿⣿\n⠀⠀⠀⠀⠀⠉⣿⣿⠀⠀⠀⠀⠀⠀⠉⣿\n⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⣀⣿\n⠀⠀⠀⠀⠀⠀⣀⣿⣿\n⠀⠀⠀⠀⠤⣿⠿⠿⠿')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⣀\n⠀⠀⣶⣿⠿⠀⠀⠀⣀⠀⣤⣤\n⠀⣶⣿⠀⠀⠀⠀⣿⣿⣿⠛⠛⠿⣤⣀\n⣶⣿⣤⣤⣤⣤⣤⣿⣿⣿⣀⣤⣶⣭⣿⣶⣀\n⠉⠉⠉⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⠛⠛⠿⠿\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿\n⠀⠀⠀⠀⠀⠀⠀⠿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⣭⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⣤⣿⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠿\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⠛⠿⣿⣤\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⠀⠀⠀⣿⣿⣤\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⣶⣿⠛⠉\n⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⣿⠀⠀⠉\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⠀⠀⣶⣿⣶\n⠀⠀⠀⣤⣤⣤⣿⣿⣿\n⠀⠀⣶⣿⣿⣿⣿⣿⣿⣿⣶\n⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⠀⠀⣿⣉⣿⣿⣿⣿⣉⠉⣿⣶\n⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿\n⠀⣤⣿⣿⣿⣿⣿⣿⣿⠿⠀⣿⣶\n⣤⣿⠿⣿⣿⣿⣿⣿⠿⠀⠀⣿⣿⣤\n⠉⠉⠀⣿⣿⣿⣿⣿⠀⠀⠒⠛⠿⠿⠿\n⠀⠀⠀⠉⣿⣿⣿⠀⠀⠀⠀⠀⠀⠉\n⠀⠀⠀⣿⣿⣿⣿⣿⣶\n⠀⠀⠀⠀⣿⠉⠿⣿⣿\n⠀⠀⠀⠀⣿⣤⠀⠛⣿⣿\n⠀⠀⠀⠀⣶⣿⠀⠀⠀⣿⣶\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣭⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⣤⣿⣿⠉')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣶\n⠀⠀⠀⠀⠀⣀⣀⠀⣶⣿⣿⠶\n⣶⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣤\n⠀⠉⠶⣶⣀⣿⣿⣿⣿⣿⣿⣿⠿⣿⣤⣀\n⠀⠀⠀⣿⣿⠿⠉⣿⣿⣿⣿⣭⠀⠶⠿⠿\n⠀⠀⠛⠛⠿⠀⠀⣿⣿⣿⣉⠿⣿⠶\n⠀⠀⠀⠀⠀⣤⣶⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⠒\n⠀⠀⠀⠀⣀⣿⣿⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⣿⣿⣿⠛⣭⣭⠉\n⠀⠀⠀⠀⠀⣿⣿⣭⣤⣿⠛\n⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿⣭\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⠉⠛⠿⣶⣤\n⠀⠀⠀⠀⠀⠀⣀⣿⠀⠀⣶⣶⠿⠿⠿\n⠀⠀⠀⠀⠀⠀⣿⠛\n⠀⠀⠀⠀⠀⠀⣭⣶')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿\n⠀⠀⣶⠀⠀⣀⣤⣶⣤⣉⣿⣿⣤⣀\n⠤⣤⣿⣤⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣀\n⠀⠛⠿⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⠉⠛⠿⣿⣤\n⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣿⣿⠛⠀⠀⠀⣶⠿\n⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⣿⣿⣿⣤⠀⣿⠿\n⠀⠀⠀⠀⠀⠀⠀⣶⣿⣿⣿⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠿⣿⣿⣿⣿⣿⠿⠉⠉\n⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⠿\n⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠉\n⠀⠀⠀⠀⠀⠀⠀⠀⣛⣿⣭⣶⣀\n⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠉⠛⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⣿⣿\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣉⠀⣶⠿\n⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⠿\n⠀⠀⠀⠀⠀⠀⠀⠛⠿⠛')
  await asyncio.sleep(0.3)
  await message.edit(content='⠀⠀⠀⣶⣿⣶\n⠀⠀⠀⣿⣿⣿⣀\n⠀⣀⣿⣿⣿⣿⣿⣿\n⣶⣿⠛⣭⣿⣿⣿⣿\n⠛⠛⠛⣿⣿⣿⣿⠿\n⠀⠀⠀⠀⣿⣿⣿\n⠀⠀⣀⣭⣿⣿⣿⣿⣀\n⠀⠤⣿⣿⣿⣿⣿⣿⠉\n⠀⣿⣿⣿⣿⣿⣿⠉\n⣿⣿⣿⣿⣿⣿\n⣿⣿⣶⣿⣿\n⠉⠛⣿⣿⣶⣤\n⠀⠀⠉⠿⣿⣿⣤\n⠀⠀⣀⣤⣿⣿⣿\n⠀⠒⠿⠛⠉⠿⣿\n⠀⠀⠀⠀⠀⣀⣿⣿\n⠀⠀⠀⠀⣶⠿⠿⠛')
  await asyncio.sleep(3)
  await message.delete()
  await ctx.message.delete()

@client.command(aliases=['e'])
async def emote(ctx, *message):


                
        emoji_list = []
        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        print(message)
        for i in range(len(message)):
          emoji = discord.utils.get(client.emojis, name=message[i])
          emojistr = str(emoji)
          emoji_list.append(emojistr)
        if emoji == None:
                oof = await ctx.send(f'Invalid emoji name.')
                await asyncio.sleep(3)
                await oof.delete()
                await ctx.message.delete()
                return
        await webhook.send(
            "".join(emoji_list), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()
        await ctx.message.delete()

@client.command(aliases=['s'])
async def sticker(ctx, msgID: int):
  msg = await ctx.fetch_message(msgID)
  await ctx.send(msg.stickers)

def paginate(lines, chars=2000):
    size = 0
    message = []
    for line in lines:
        if len(line) + size > chars:
            yield message
            message = []
            size = 0
        message.append(line)
        size += len(line)
    yield message

@client.command(aliases=['ge'])
async def getemotes(ctx):
  server = ctx.message.guild
  emojis = [str(x) for x in server.emojis]
  message = ""
  embed = discord.Embed()
  for guild in client.guilds:
    if guild.id != 856415893305950228 and guild.id !=856412098459860993:
      print(guild.id)
      #await ctx.send(guild.name)
      emojis = [str(x) for x in guild.emojis]
      for index,message in enumerate(paginate(emojis)):
        if index==0:
          embed.title=guild.name
        else:
          embed.title=''  
        embed.description = ''.join(message)
        await ctx.send(embed=embed)
    else:
      print('bad apple server')  

@client.command()
async def id(ctx, title, *, message=None):
  if 'cdn.discordapp.com' in message:
    async with aiohttp.ClientSession() as session:
      async with session.get('https://cdn.discordapp.com/emojis/' + message.split('/')[4].split('.')[0]) as response:
        img = await response.read()
  else:      
    async with aiohttp.ClientSession() as session:
      async with session.get('https://cdn.discordapp.com/emojis/' + message) as response:
          img = await response.read()
# now img contains the bytes of the image, let's create the emoji
  await ctx.guild.create_custom_emoji(name=title, image=img)
  await ctx.send('Emoji uploaded!')

@client.command()
async def wristworld(ctx):
  message = await ctx.send('You’ve seen Miku on stage, but what about your wrist?')
  await asyncio.sleep(1)
  message2 = await ctx.send('Wrist World is an AR game using wristbands, now featuring Hatsune Miku!')
  await asyncio.sleep(1)
  message3 = await ctx.send('Collect songs, dances, and even save the world!')
  await asyncio.sleep(1)
  message4 = await ctx.send('Do You Wrist World? ')
  await asyncio.sleep(1)
  message5 = await ctx.send('*wrist world*')
  await asyncio.sleep(3)
  await message.delete()
  await message2.delete()
  await message3.delete()
  await message4.delete()
  await message5.delete()
  await ctx.message.delete()

@client.command()
async def fmega(ctx):
  webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
  await webhook.send(
            'https://thumbs.gfycat.com/BleakAdorableLangur-size_restricted.gif', username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)
  webhooks = await ctx.channel.webhooks()
  for webhook in webhooks:
      await webhook.delete()
  await ctx.message.delete()  

@client.command()
async def kotowaru(ctx):
  webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
  await webhook.send(
            'https://cdn.discordapp.com/attachments/812666547520667669/852875900731392010/tenor.gif', username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)
  webhooks = await ctx.channel.webhooks()
  for webhook in webhooks:
      await webhook.delete()
  await ctx.message.delete()

@client.command()
async def ascend(ctx):
  webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
  await webhook.send(
            'https://tenor.com/view/bruno-bucciarati-jojo-jjba-death-gif-14981833', username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)
  webhooks = await ctx.channel.webhooks()
  for webhook in webhooks:
      await webhook.delete()
  await ctx.message.delete()    

@client.command()
async def jizz(ctx):
  webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
  await webhook.send(
            'https://pbs.twimg.com/media/E3oLqt8VUAQpRiL?format=jpg&name=900x900', username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)
  webhooks = await ctx.channel.webhooks()
  for webhook in webhooks:
      await webhook.delete()
  await ctx.message.delete()  

async def vcplay(ctx, a, loop=None): 
  voice_channel = ctx.author.voice.channel
  channel = None
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)         
  if voice_channel != None:
      channel = voice_channel.name
      if voice == None:
        vc = await voice_channel.connect()       
        if loop=="loop":
          def loop():  
            vc.play(discord.FFmpegPCMAudio(source=a), after=lambda e: loop())
          loop()
        else:
            vc.play(discord.FFmpegPCMAudio(source=a))
      else:
        if loop=="loop":
          def loop2():  
            voice.play(discord.FFmpegPCMAudio(source=a), after=lambda e: loop2())
          loop2()
        else:
            voice.play(discord.FFmpegPCMAudio(source=a))  
  else:
      await ctx.send(str(ctx.author.name) + "is not in a channel.")
  # Delete command after the audio is done playing.
  await ctx.message.delete() 

@client.command()
async def letsgo(ctx, loop=None):  
  await vcplay(ctx,"sounds/vibez-lets-go.mp3",loop)

@client.command()
async def vtubus(ctx, loop=None):  
  await vcplay(ctx,"sounds/vtubus.mp3",loop)

@client.command()
async def giorno(ctx, loop=None):  
  await vcplay(ctx,"sounds/giorno theme.mp3",loop)

@client.command()
async def ding(ctx, loop=None): 
  await vcplay(ctx,"sounds/DING DING DING DING DING DING DING DI DI DING.mp3",loop) 

@client.command()
async def yodayo(ctx, loop=None):  
  await vcplay(ctx,"sounds/Nakiri Ayame's yo dayo_.mp3",loop)

@client.command()
async def yodazo(ctx, loop=None):  
  await vcplay(ctx,"sounds/Yo Dazo!.mp3",loop)    

@client.command()
async def jonathan(ctx, loop=None):  
  await vcplay(ctx,"sounds/Jonathan's theme but its only the BEST part.mp3",loop)      

@client.command()
async def joseph(ctx, loop=None):  
  await vcplay(ctx,"sounds/Joseph's theme but only the good part (1).mp3",loop)        

@client.command()
async def jotaro(ctx, loop=None):  
  await vcplay(ctx,"sounds/Jotaro’s theme but it’s only the good part.mp3",loop) 

@client.command()
async def josuke(ctx, loop=None):  
  await vcplay(ctx,"sounds/Josuke theme but it's only the good part.mp3",loop)   

@client.command()
async def kira(ctx, loop=None):  
  await vcplay(ctx,"sounds/Killer (Yoshikage Kira's Theme) - Jojo's Bizarre Adventure Part 4_ Diamond Is Unbreakable.mp3",loop)        

@client.command()
async def pillarmen(ctx, loop=None): 
  await vcplay(ctx,"sounds/Jojo's Bizarre Adventure- Awaken(Pillar Men Theme).mp3",loop)     

@client.command()
async def boom(ctx, loop=None):  
  await vcplay(ctx,"sounds/boom.mp3",loop)  

@client.command(aliases=['ogei'])
async def ogey(ctx, loop=None):  
  await vcplay(ctx,"sounds/ogey.mp3",loop)    

@client.command()
async def rrat(ctx, loop=None):  
  await vcplay(ctx,"sounds/rrat.mp3",loop)       

@client.command()
async def fart(ctx, loop=None): 
  await vcplay(ctx,"sounds/fart.mp3",loop)     

@client.command()
async def mogumogu(ctx, loop=None):  
  await vcplay(ctx,"sounds/mogu.mp3",loop)   

@client.command()
async def bababooey(ctx, loop=None):  
  await vcplay(ctx,"sounds/bababooey.mp3",loop)    

@client.command()
async def dog(ctx, loop=None):  
  await vcplay(ctx,"sounds/dog.mp3",loop)     

@client.command()
async def totsugeki(ctx, loop=None):  
  await vcplay(ctx,random.choice(may_sounds),loop)     

@client.command(aliases=['bong'])
async def tacobell(ctx, loop=None):  
  await vcplay(ctx,"sounds/tacobell.mp3",loop)   

@client.command(aliases=['amogus'])
async def amongus(ctx, loop=None):  
  await vcplay(ctx,"sounds/amongus.mp3",loop)   

@client.command(aliases=['classtrial'])
async def danganronpa(ctx, loop=None): 
  await vcplay(ctx,"sounds/danganronpa.mp3",loop)    

@client.command()
async def botansneeze(ctx, loop=None):  
  await vcplay(ctx,"sounds/botansneeze.mp3",loop)   

@client.command()
async def water(ctx, loop=None):  
  await vcplay(ctx,"sounds/water.mp3",loop)   


@client.command()
async def necoarc(ctx, loop=None):  
  await vcplay(ctx,"sounds/necoarc.mp3",loop)     

@client.command()
async def vsauce(ctx, loop=None):  
  await vcplay(ctx,"sounds/vsauce.mp3",loop)   

@client.command()
async def gigachad(ctx, loop=None):  
  await vcplay(ctx,"sounds/gigachad.mp3",loop)   

@client.command()
async def leave(ctx):
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        await ctx.send('Sus bot has left the call.', delete_after=3.0)
        await asyncio.sleep(.3)
        await ctx.message.delete()
    else: # But if it isn't
        await ctx.send("I'm not in a voice channel, use the join command to make me join", delete_after=3.0)
    await ctx.message.delete()    

@client.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Sus bot has been stopped.', delete_after=3.0)
    else:
        await ctx.send("The bot is not playing anything at the moment.", delete_after=3.0)
    await ctx.message.delete()    

@client.command()
async def stoploop(ctx):
  await ctx.guild.voice_client.disconnect()
  voice_channel = ctx.author.voice.channel
  await voice_channel.connect()
  await ctx.send('The loop has been stopped.', delete_after=3.0)
  await ctx.message.delete()

@client.command()
async def speak(ctx,*, message):        
  voice_channel = ctx.author.voice.channel
  channel = None
  tts = gTTS(message)
  with open('sounds/tts.mp3', 'wb') as f:
        tts.write_to_fp(f)  
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)          
  if voice_channel != None:
      channel = voice_channel.name
      if voice == None:
       vc = await voice_channel.connect()
       vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 
      else:
        voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 

@client.command()
async def speak2(ctx,*, message):       
  voice_channel = ctx.author.voice.channel
  channel = None
  tts = gTTS(message, lang='en', tld='com.au')
  with open('sounds/tts.mp3', 'wb') as f:
        tts.write_to_fp(f)  
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)          
  if voice_channel != None:
      channel = voice_channel.name
      if voice == None:
       vc = await voice_channel.connect()
       vc.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3")) 
      else:
        voice.play(discord.FFmpegPCMAudio(source="sounds/tts.mp3"))        

@client.command()
async def join(ctx):        
  voice_channel = ctx.author.voice.channel
  await voice_channel.connect()
  await ctx.send('Sus bot has joined the call.', delete_after=3.0)
  await ctx.message.delete()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Ayo this command is on cooldown.\nWait for %.2fs to try it again.' % error.retry_after, delete_after=3.0)
        await ctx.message.delete()
    raise error  # re-raise the error so all the errors will still show up in console
    

@client.command()
@commands.cooldown(1.0, 60.0, commands.BucketType.guild)
async def badapple(ctx, *, message=None):

        webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
        for i in range(80):
          globals()[f"b{i}"]=discord.utils.get(client.emojis, name="b"+str(i))
        await webhook.send(
            str(b0)+str(b1)+str(b2)+str(b3)+str(b4)+str(b5)+str(b6)+str(b7)+str(b8)+str(b9)+"\n"+str(b10)+str(b11)+str(b12)+str(b13)+str(b14)+str(b15)+str(b16)+str(b17)+str(b18)+str(b19), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)
        await asyncio.sleep(.5)    
        await webhook.send(
            str(b20)+str(b21)+str(b22)+str(b23)+str(b24)+str(b25)+str(b26)+str(b27)+str(b28)+str(b29)+"\n"+str(b30)+str(b31)+str(b32)+str(b33)+str(b34)+str(b35)+str(b36)+str(b37)+str(b38)+str(b39), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)    
        await asyncio.sleep(.5)       
        await webhook.send(
            str(b40)+str(b41)+str(b42)+str(b43)+str(b44)+str(b45)+str(b46)+str(b47)+str(b48)+str(b49)+"\n"+str(b50)+str(b51)+str(b52)+str(b53)+str(b54)+str(b55)+str(b56)+str(b57)+str(b58)+str(b59), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)
        await asyncio.sleep(.5)       
        await webhook.send(
            str(b60)+str(b61)+str(b62)+str(b63)+str(b64)+str(b65)+str(b66)+str(b67)+str(b68)+str(b69)+"\n"+str(b70)+str(b71)+str(b72)+str(b73)+str(b74)+str(b75)+str(b76)+str(b77)+str(b78)+str(b79), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)     


        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()
        await ctx.message.delete()

@client.command()
async def clip(ctx,link,start,end,filename):

  if re.match("\d{2}:\d{2}:\d{2}",start) != None and re.match("\d{2}:\d{2}:\d{2}",end) != None:
    print('good timestamps!')
  else:
    print('bad timestamps!')
    await ctx.send('Timestamps are wrong. Please provide it in HH:MM:SS')
    return

  if os.path.isfile(filename+".mkv"):
    os.remove(filename+".mkv")
  if os.path.isfile(filename+".mp4"):
    os.remove(filename+".mp4")  
  message = await ctx.send('Fetching url...')
  coms = ['yt-dlp', '-g', '-f','best','--youtube-skip-dash-manifest', link]
  print(shjoin(coms))
  startsplit = start.split(":")
  shour = startsplit[0]
  sminute=startsplit[1]
  ssecond=startsplit[2]
  date_time = datetime.strptime(start, "%H:%M:%S")
  a_timedelta = date_time - datetime(1900, 1, 1)
  seconds = a_timedelta.total_seconds()
  print(seconds)
  if seconds < 30:
    print('less than 30 seconds!')
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  else:
    print('it is at least 30 seconds.')  
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) - timedelta(seconds=30)
  endsplit = end.split(":")
  ehour = endsplit[0]
  eminute=endsplit[1]
  esecond=endsplit[2]
  result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond)) - timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  out = await asyncio.create_subprocess_exec(*coms, 
           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout, stderr = await out.communicate()
  dirlinks = stdout.decode('utf-8').split("\n")
  vid = dirlinks[0]
  aud = dirlinks[1] 
  if seconds < 30:
    coms = ['ffmpeg', '-ss', str(result1), '-i',  vid, '-t', str(result2), '-c:v', 'libx264', '-c:a', 'copy', filename+".mkv"]  
  else:
    coms = ['ffmpeg', '-ss', str(result1), '-i',  vid, '-ss', '30', '-t', str(result2), '-c:v', 'libx264', '-c:a', 'copy', filename+".mkv"]  
  print(shjoin(coms))
  await message.edit(content='Downloading... This will take a while...')
  try:
    process = await asyncio.create_subprocess_exec(*coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in process.stdout:
      #print(line)
    #process.communicate()
    while process.returncode is None:
        #await asyncio.sleep(1)
        
        line =await process.stdout.read(100)
        if not line:
            break
        #print(line.decode('utf-8'))
        linedec = line.decode('utf-8')
        
        if "frame=" in linedec:
          if not "00:00:00.00" in linedec.split('=')[5].split(' ')[0]:
            strpcurr = datetime.strptime(linedec.split('=')[5].split(' ')[0], '%H:%M:%S.%f')
            currtime = timedelta(hours=strpcurr.hour,minutes=strpcurr.minute,seconds=strpcurr.second,microseconds=strpcurr.microsecond)
            print(linedec)
            percentage = (currtime.total_seconds() / result2.total_seconds())*100
            print(str(percentage) + "% complete...")
            await message.edit(content=str(round(percentage,2)) + "% complete...")    
    os.rename(filename+".mkv",filename+".mp4")  
    await ctx.send(file=discord.File(filename+".mp4"))
    #await ctx.send(ctx.message.author.mention)
    os.remove(filename+".mp4")
    await message.delete()      
  except ValueError:
    await message.edit(content='An error occured... Uh, try it again.')

@client.command()
async def fastclip3(ctx,link,start,end,filename):
  message = await ctx.send('Fetching url...')
  coms = ['yt-dlp', '-g', '-f','best','--youtube-skip-dash-manifest', link]
  print(shjoin(coms))
  startsplit = start.split(":")
  shour = startsplit[0]
  sminute=startsplit[1]
  ssecond=startsplit[2]
  date_time = datetime.strptime(start, "%H:%M:%S")
  a_timedelta = date_time - datetime(1900, 1, 1)
  seconds = a_timedelta.total_seconds()
  print(seconds)
  if seconds < 30:
    print('less than 30 seconds!')
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  else:
    print('it is at least 30 seconds.')  
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) - timedelta(seconds=30)
  
  endsplit = end.split(":")
  ehour = endsplit[0]
  eminute=endsplit[1]
  esecond=endsplit[2]
  result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond)) - timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  out = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await out.communicate()
  print(stdout)
  print(stderr)
  dirlinks = stdout.decode('utf-8').split("\n")
  vid = dirlinks[0]
  aud = dirlinks[1] 
  if seconds < 30:
    coms = ['ffmpeg', '-ss', str(result1), '-i',  vid, '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename+".mp4"]
  else:
    coms = ['ffmpeg', '-ss', str(result1), '-i',  vid, '-ss', '30', '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename + ".mp4"]
  print(shjoin(coms))
  await message.edit(content='Downloading... This will take a while...')
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr.decode('utf-8'))
  #os.rename(filename+".mkv",filename+".mp4")  
  try:
    await ctx.send(file=discord.File(filename+".mp4"))
  except Exception:
     await message.edit(content='I failed.')
  await ctx.send(ctx.message.author.mention)
  os.remove(filename+".mp4")
  await message.delete()

@client.command()
async def fastclip2(ctx,link,start,end,filename):
  message = await ctx.send('Fetching url...')
  coms = ['yt-dlp', '-g', '-f','best','--youtube-skip-dash-manifest', link]
  print(shjoin(coms))
  startsplit = start.split(":")
  shour = startsplit[0]
  sminute=startsplit[1]
  ssecond=startsplit[2]  
  result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  endsplit = end.split(":")
  ehour = endsplit[0]
  eminute=endsplit[1]
  esecond=endsplit[2]
  result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond)) - timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  out = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await out.communicate()
  print(stdout)
  print(stderr)
  dirlinks = stdout.decode('utf-8').split("\n")
  vid = dirlinks[0]
  aud = dirlinks[1] 
  coms = ['ffmpeg','-ss', str(result1), '-i',  vid, '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename+".mp4"]
  
  print(shjoin(coms))
  await message.edit(content='Downloading... This will take a while...')
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  #stdout, stderr = await process.communicate()
  while process.returncode is None:
    line = await process.stdout.read(100)
    if not line:
            break
    #await message.edit(content=line.decode('utf-8'))
    await ctx.send(line.decode('utf-8'))
    await asyncio.sleep(1)
  if process.returncode != 0:
      await ctx.send('return code is not 0. i give up')
      return
  #print(stdout)
  #print(stderr)
  #os.rename(filename+".mkv",filename+".mp4")  
  try:
    await ctx.send(file=discord.File(filename+".mp4"))
  except Exception:
     await message.edit(content='I failed.')
  await ctx.send(ctx.message.author.mention)
  os.remove(filename+".mp4")
  await message.delete()


@client.command()
async def fastclip(ctx,link,start,end,filename):

  if re.match("\d{2}:\d{2}:\d{2}",start) != None and re.match("\d{2}:\d{2}:\d{2}",end) != None:
    print('good timestamps!')
  else:
    print('bad timestamps!')
    await ctx.send('Timestamps are wrong. Please provide it in HH:MM:SS')
    return

  message = await ctx.send('Fetching url...')
  coms = ['yt-dlp', '-g', '-f','best','--youtube-skip-dash-manifest', link]
  print(shjoin(coms))
  startsplit = start.split(":")
  shour = startsplit[0]
  sminute=startsplit[1]
  ssecond=startsplit[2]
  date_time = datetime.strptime(start, "%H:%M:%S")
  a_timedelta = date_time - datetime(1900, 1, 1)
  seconds = a_timedelta.total_seconds()
  print(seconds)
  if seconds < 30:
    print('less than 30 seconds!')
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  else:
    print('it is at least 30 seconds.')  
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) - timedelta(seconds=30)
  
  endsplit = end.split(":")
  ehour = endsplit[0]
  eminute=endsplit[1]
  esecond=endsplit[2]
  if seconds < 30:  
    result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond))
  else:  
    result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond)) - timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) + timedelta(seconds=30)
  out = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await out.communicate()
  print(stdout)
  print(stderr)
  dirlinks = stdout.decode('utf-8').split("\n")
  vid = dirlinks[0]
  aud = dirlinks[1] 
  if seconds < 30:
    coms = ['ffmpeg', '-i',  vid, '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename+"_temp.mp4"]
  else:
    coms = ['ffmpeg','-noaccurate_seek','-ss', str(result1), '-i',  vid, '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename + "_temp.mp4"]
  print(shjoin(coms))
  await message.edit(content='Downloading... This will take a while...')
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)

  # while process.returncode is None:
  #     line = await process.stdout.readline()
  #     if not line:
  #             break
  #     await ctx.send(line.decode('utf-8'))


  stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr.decode('utf-8'))
  #os.rename(filename+".mkv",filename+".mp4")  

  def max_le(seq, val):
    """
    Same as max_lt(), but items in seq equal to val apply as well.

    >>> max_le([2, 3, 7, 11], 10)
    7
    >>> max_le((1, 3, 6, 11), 6)
    6
    """

    idx = len(seq)-1
    while idx >= 0:
        if seq[idx] <= val:
            return seq[idx]
        idx -= 1

    return None

  def min_gt(seq, val):
    """
    Return smallest item in seq for which item > val applies.
    None is returned if seq was empty or all items in seq were <= val.

    >>> min_gt([1, 3, 6, 7], 4)
    6
    >>> min_gt([2, 4, 7, 11], 5)
    7
    """

    for v in seq:
        if v > val:
            return v
    return None

  def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

  coms = ['ffprobe', '-v', 'error', '-skip_frame', 'nokey', '-show_entries', "frame=pkt_pts_time", "-select_streams", "v", "-of", "csv=p=0", filename + "_temp.mp4"]
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stderr)
  print(stdout.decode('utf-8'))
  timelist_str = stdout.decode('utf-8').strip().split("\n")
  print(timelist_str)
  timelist_float = [float(i) for i in timelist_str]
  print(timelist_float)

  round_number = 1
  round_frames = False
  

  if seconds < 30:
    if round_frames == True:
      keyframe = round_down(max_le(timelist_float, seconds), round_number)
    else:
      prev_keyframe = max_le(timelist_float, seconds) 
      next_keyframe = min_gt(timelist_float, seconds)   
      print('after '+ str(prev_keyframe))
      print('before ' + str(next_keyframe))
      if next_keyframe == None:
        print('no next keyframe!')
        keyframe = prev_keyframe
      else:  
        keyframe= (prev_keyframe + next_keyframe) / 2   
    print('keyframe is '+"{:.6f}".format(keyframe))
    if round_down(seconds-prev_keyframe,round_number) == 0:
      await ctx.send("<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe.")
    else:  
      await ctx.send("Clipping "+ str(round_down(seconds-prev_keyframe,round_number))+ " seconds earlier to nearest keyframe...")
  
    
  else:  
    if round_frames == True:
      keyframe = round_down(max_le(timelist_float, 30), round_number)
    else:
      prev_keyframe = max_le(timelist_float, 30)
      next_keyframe = min_gt(timelist_float, 30)
      if next_keyframe == None:
        print('no next keyframe!')
        keyframe = prev_keyframe
      else:  
        keyframe= (prev_keyframe + next_keyframe) / 2 
    print('keyframe is '+str(keyframe))
    if round_down(30-prev_keyframe,round_number) == 0:
      await ctx.send("<:callipog:850365252637032479> Poggers. No need to clip to nearest keyframe.")
    else:  
      await ctx.send("Clipping "+ str(round_down(30-prev_keyframe,round_number))+ " seconds earlier to nearest keyframe...")

  coms = ['ffmpeg','-noaccurate_seek', '-ss', "{:.6f}".format(keyframe),'-i',  filename + "_temp.mp4", '-c:v', 'copy', '-c:a', 'copy','-avoid_negative_ts','make_zero', filename + ".mp4"]
  print(shjoin(coms))
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr.decode('utf-8'))

  coms = ['ffprobe', '-v', 'error', '-skip_frame', 'nokey', '-show_entries', "frame=pkt_pts_time", "-select_streams", "v", "-of", "csv=p=0", filename + ".mp4"]
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stderr)
  print('final keyframes:')
  print(stdout.decode('utf-8'))


  try:
    
    await ctx.send(file=discord.File(filename + ".mp4"))
  except Exception:
     await message.edit(content='I failed.')
  await ctx.send(ctx.message.author.mention)
  os.remove(filename+".mp4")
  os.remove(filename+"_temp.mp4")
  await message.delete()

@client.command()
async def idclip(ctx,link,start,end,filename,id,id2):

  if re.match("\d{2}:\d{2}:\d{2}",start) != None and re.match("\d{2}:\d{2}:\d{2}",end) != None:
    print('good timestamps!')
  else:
    print('bad timestamps!')
    await ctx.send('Timestamps are wrong. Please provide it in HH:MM:SS')
    return

  message = await ctx.send('Fetching url...')
  coms = ['yt-dlp', '-g', '-f',id+"+"+id2, link]
  print(shjoin(coms))
  startsplit = start.split(":")
  shour = startsplit[0]
  sminute=startsplit[1]
  ssecond=startsplit[2]
  date_time = datetime.strptime(start, "%H:%M:%S")
  a_timedelta = date_time - datetime(1900, 1, 1)
  seconds = a_timedelta.total_seconds()
  print(seconds)
  if seconds < 30:
    print('less than 30 seconds!')
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  else:
    print('it is at least 30 seconds.')  
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) - timedelta(seconds=30)
  
  endsplit = end.split(":")
  ehour = endsplit[0]
  eminute=endsplit[1]
  esecond=endsplit[2]
  if seconds < 30:  
    result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond))
  else:  
    result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond)) - timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) + timedelta(seconds=30)
  out = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await out.communicate()
  print(stdout)
  print(stderr)
  dirlinks = stdout.decode('utf-8').split("\n")
  vid = dirlinks[0]
  aud = dirlinks[1] 
  if seconds < 30:
    coms = ['ffmpeg', '-i',  vid, '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename+"_temp.mp4"]
  else:
    coms = ['ffmpeg','-noaccurate_seek','-ss', str(result1), '-i',  vid, '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename + "_temp.mp4"]
  print(shjoin(coms))
  await message.edit(content='Downloading... This will take a while...')
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)

  while process.returncode is None:
      line = await process.stdout.readline()
      if not line:
              break
      #await message.edit(content=line.decode('utf-8'))
      await ctx.send(line.decode('utf-8'))
      #await asyncio.sleep(1)

  #stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr.decode('utf-8'))
  #os.rename(filename+".mkv",filename+".mp4")  

  def max_le(seq, val):
    """
    Same as max_lt(), but items in seq equal to val apply as well.

    >>> max_le([2, 3, 7, 11], 10)
    7
    >>> max_le((1, 3, 6, 11), 6)
    6
    """

    idx = len(seq)-1
    while idx >= 0:
        if seq[idx] <= val:
            return seq[idx]
        idx -= 1

    return None

  def min_gt(seq, val):
    """
    Return smallest item in seq for which item > val applies.
    None is returned if seq was empty or all items in seq were <= val.

    >>> min_gt([1, 3, 6, 7], 4)
    6
    >>> min_gt([2, 4, 7, 11], 5)
    7
    """

    for v in seq:
        if v > val:
            return v
    return None

  def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

  coms = ['ffprobe', '-v', 'error', '-skip_frame', 'nokey', '-show_entries', "frame=pkt_pts_time", "-select_streams", "v", "-of", "csv=p=0", filename + "_temp.mp4"]
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stderr)
  print(stdout.decode('utf-8'))
  timelist_str = stdout.decode('utf-8').strip().split("\n")
  print(timelist_str)
  timelist_float = [float(i) for i in timelist_str]
  print(timelist_float)

  round_number = 1
  round_frames = False
  

  if seconds < 30:
    if round_frames == True:
      keyframe = round_down(max_le(timelist_float, seconds), round_number)
    else:
      prev_keyframe = max_le(timelist_float, seconds) 
      next_keyframe = min_gt(timelist_float, seconds)   
      print('after '+ str(prev_keyframe))
      print('before ' + str(next_keyframe))
      if next_keyframe == None:
        print('no next keyframe!')
        keyframe = prev_keyframe
      else:  
        keyframe= (prev_keyframe + next_keyframe) / 2   
    print('keyframe is '+"{:.6f}".format(keyframe))
    await ctx.send("Clipping "+ str(round_down(seconds-prev_keyframe,round_number))+ " seconds earlier to nearest keyframe...")
  
    
  else:  
    if round_frames == True:
      keyframe = round_down(max_le(timelist_float, 30), round_number)
    else:
      prev_keyframe = max_le(timelist_float, 30)
      next_keyframe = min_gt(timelist_float, 30)
      keyframe= (prev_keyframe + next_keyframe) / 2 
    print('keyframe is '+str(keyframe))
    await ctx.send("Clipping "+ str(round_down(30-prev_keyframe,round_number))+ " seconds earlier to nearest keyframe...")

  coms = ['ffmpeg','-noaccurate_seek', '-ss', "{:.6f}".format(keyframe),'-i',  filename + "_temp.mp4", '-c:v', 'copy', '-c:a', 'copy','-avoid_negative_ts','make_zero', filename + ".mp4"]
  print(shjoin(coms))
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr.decode('utf-8'))

  coms = ['ffprobe', '-v', 'error', '-skip_frame', 'nokey', '-show_entries', "frame=pkt_pts_time", "-select_streams", "v", "-of", "csv=p=0", filename + ".mp4"]
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stderr)
  print('final keyframes:')
  print(stdout.decode('utf-8'))


  try:
    
    await ctx.send(file=discord.File(filename + ".mp4"))
  except Exception:
     await message.edit(content='I failed.')
  await ctx.send(ctx.message.author.mention)
  os.remove(filename+".mp4")
  os.remove(filename+"_temp.mp4")
  await message.delete()


@client.command()
async def clipaudio(ctx,link,start,end,filename, filetype=None):
  if filetype not in ['mp3','wav','ogg']:
    await ctx.send('Missing or no filetype provided. I can do mp3, wav, and ogg.')
    return

  
  if re.match("\d{2}:\d{2}:\d{2}",start) != None and re.match("\d{2}:\d{2}:\d{2}",end) != None:
    print('good timestamps!')
  else:
    print('bad timestamps!')
    await ctx.send('Timestamps are wrong. Please provide it in HH:MM:SS')
    return

  message = await ctx.send('Fetching url...')
  coms = ['yt-dlp', '-g', '-f','251', link]
  print(shjoin(coms))
  startsplit = start.split(":")
  shour = startsplit[0]
  sminute=startsplit[1]
  ssecond=startsplit[2]
  date_time = datetime.strptime(start, "%H:%M:%S")
  a_timedelta = date_time - datetime(1900, 1, 1)
  seconds = a_timedelta.total_seconds()
  print(seconds)
  if seconds < 30:
    print('less than 30 seconds!')
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  else:
    print('it is at least 30 seconds.')  
    result1 = timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond)) - timedelta(seconds=30)
  
  endsplit = end.split(":")
  ehour = endsplit[0]
  eminute=endsplit[1]
  esecond=endsplit[2]
  result2 = timedelta(hours=int(ehour),minutes=int(eminute),seconds=int(esecond)) - timedelta(hours=int(shour),minutes=int(sminute),seconds=int(ssecond))
  out = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await out.communicate()
  print(stdout)
  print(stderr)
  dirlinks = stdout.decode('utf-8').split("\n")
  vid = dirlinks[0]
  aud = dirlinks[1] 
  if seconds < 30:
    coms = ['ffmpeg', '-i',  vid, '-ss', str(result1),'-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename+".ogg"]
  else:
    coms = ['ffmpeg', '-ss', str(result1), '-i',  vid, '-ss', '30', '-t', str(result2), '-c:v', 'copy', '-c:a', 'copy', filename + ".ogg"]
  print(shjoin(coms))
  await message.edit(content='Downloading... This will take a while...')
  process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await process.communicate()
  print(stdout)
  print(stderr.decode('utf-8'))


  if filetype == 'ogg':
    pass
  elif filetype == 'mp3':
    coms = ['ffmpeg', '-i',filename + ".ogg",'-codec:a','libmp3lame','-q:a','0', filename + ".mp3"]
    print(shjoin(coms))
    await message.edit(content='Using libmp3lame to convert to VBR 0 MP3...')
    process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    print(stdout)
    print(stderr.decode('utf-8'))
  elif filetype == 'wav':
    coms = ['ffmpeg', '-i',filename + ".ogg", filename + ".wav"]
    print(shjoin(coms))
    process = await asyncio.create_subprocess_exec(*coms, stdout=asyncio.subprocess.PIPE,                      stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    print(stdout)
    print(stderr.decode('utf-8'))

  #os.rename(filename+".mkv",filename+".mp4")  
  try:
    await ctx.send(file=discord.File(filename+"."+ filetype.lower()))
  except Exception:
     await message.edit(content='I failed.')
  await ctx.send(ctx.message.author.mention)
  os.remove(filename+".ogg")
  os.remove(filename+"."+filetype.lower())
  await message.delete()



@client.command()
async def download(ctx,link):
  import codecs
  if "reddit.com" in link:
    message = await ctx.send('Downloading...')
    coms = ['yt-dlp', '-f','bestvideo+bestaudio',"--cookies","cookies (17).txt",link]
    coms2 = ['yt-dlp', '--get-filename',"--cookies","cookies (17).txt",link]
    print(shjoin(coms))
    print(shjoin(coms2))
    proc = await asyncio.create_subprocess_exec(*coms, 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout, stderr = await proc.communicate()
    while proc.returncode is None:
      line = await proc.stdout.read(100)
      if not line:
              break
      #await message.edit(content=line.decode('utf-8'))
      await ctx.send(line.decode('utf-8'))
      await asyncio.sleep(1)
    if proc.returncode != 0:
      await ctx.send('return code is not 0. trying something else')
      coms = ['yt-dlp',"--cookies","cookies (17).txt",link]
      print(shjoin(coms))
      proc = await asyncio.create_subprocess_exec(*coms, 
              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      #stdout, stderr = await proc.communicate()
      while proc.returncode is None:
        line = await proc.stdout.read(100)
        if not line:
                break
        await message.edit(content=line.decode('utf-8'))
        #await ctx.send(line.decode('utf-8'))
        await asyncio.sleep(1)  
      if proc.returncode != 0:
        await ctx.send('return code is not 0. i give up')
        return
    await message.edit(content="Almost there...")  
    out2 = await asyncio.create_subprocess_exec(*coms2, 
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    while out2.returncode is None:
      await message.edit(content="A little more...")  
    else:  
      try:
        thing = await out2.stdout.read()
        filename = thing.decode('utf-8').split("\n")[0]
        await message.edit(content="Sending video...")  
        try:
          await ctx.send(file=discord.File(filename))
        except Exception as e:
         await ctx.send(e)   
      except discord.HTTPException:  
        await ctx.send('File too large, broski <:towashrug:853606191711649812>')
    os.remove(filename)
    await message.delete()  
  elif "facebook.com" in link:
    message = await ctx.send('Downloading...')
    cookiecoms = ['gpg','--pinentry-mode=loopback','--passphrase',os.getenv('FBPASSPHRASE'),"cookies (15).txt.gpg"]
    cookieproc = await asyncio.create_subprocess_exec(*cookiecoms, 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = await cookieproc.communicate()  
    # res = stdout.decode('UTF-8').split('\n')[2:]
    # fin = '\n'.join(res)
    # print(fin)
    # return_data = io.BytesIO()
    # return_data.write(fin.encode())
    # return_data.seek(0)
    coms = ['yt-dlp', '-f','best','--cookies','cookies (15).txt',link]
    coms2 = ['yt-dlp', '-f','best', '--get-filename','--cookies','cookies (15).txt',link]
    print(shjoin(coms))
    print(shjoin(coms2))
    proc = await asyncio.create_subprocess_exec(*coms, 
             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 
    while proc.returncode is None:
      line = await proc.stdout.read(100)
      if not line:
              break
      await message.edit(content=line.decode('utf-8'))
      await asyncio.sleep(1)
    await message.edit(content="Almost there...")  
    out2 = await asyncio.create_subprocess_exec(*coms2, 
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    while out2.returncode is None:
      await message.edit(content="A little more...")  
  elif "instagram.com" in link:
    message = await ctx.send('Downloading...')
    cookiecoms = ['gpg','--pinentry-mode=loopback','--passphrase',os.getenv('FBPASSPHRASE'),"instacook.txt.gpg"]
    cookieproc = await asyncio.create_subprocess_exec(*cookiecoms, 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = await cookieproc.communicate()  
    # res = stdout.decode('UTF-8').split('\n')[2:]
    # fin = '\n'.join(res)
    # print(fin)
    # return_data = io.BytesIO()
    # return_data.write(fin.encode())
    # return_data.seek(0)
    coms = ['yt-dlp', '-f','best','--cookies','instacook.txt',link]
    coms2 = ['yt-dlp', '-f','best', '--get-filename','--cookies','instacook.txt',link]
    print(shjoin(coms))
    print(shjoin(coms2))
    proc = await asyncio.create_subprocess_exec(*coms, 
             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 
    while proc.returncode is None:
      line = await proc.stdout.read(100)
      if not line:
              break
      await message.edit(content=line.decode('utf-8'))
      await asyncio.sleep(1)
    await message.edit(content="Almost there...")  
    out2 = await asyncio.create_subprocess_exec(*coms2, 
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    while out2.returncode is None:
      await message.edit(content="A little more...")        
    else:  
      os.remove('instacook.txt')
      try:
        thing = await out2.stdout.read()
        filename = thing.decode('utf-8').split("\n")[-2]
        print(thing.decode('utf-8'))
        await message.edit(content="Sending video...")  
        try:
          await ctx.send(file=discord.File(filename))
        except Exception as e:
         await ctx.send(e)   
      except discord.HTTPException:  
        await ctx.send('File too large, broski <:towashrug:853606191711649812>')
      except Exception as e:  
        await message.edit(content=e)  
    os.remove(filename)
    
    await message.delete() 


     #await ctx.send('I can\'t do Facebook links, unfortunately. It should work but idk why it don\'t')
  else:
    message = await ctx.send('Downloading...')
    coms = ['yt-dlp', '-f','best',link]
    coms2 = ['yt-dlp', '-f','best', '--get-filename',link]
    print(shjoin(coms))
    print(shjoin(coms2))
    proc = await asyncio.create_subprocess_exec(*coms, 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout, stderr = await proc.communicate()
    while proc.returncode is None:
      line = await proc.stdout.read(100)
      if not line:
              break
      await message.edit(content=line.decode('utf-8'))
      await asyncio.sleep(1)
    await message.edit(content="Almost there...")  
    out2 = await asyncio.create_subprocess_exec(*coms2, 
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    while out2.returncode is None:
      await message.edit(content="A little more...")  
    else:  
      try:
        thing = await out2.stdout.read()
        filename = thing.decode('utf-8').split("\n")[0]
        await message.edit(content="Sending video...")  
        try:
          await ctx.send(file=discord.File(filename))
        except Exception as e:
         await ctx.send(e)   
      except discord.HTTPException:  
        await ctx.send('File too large, broski <:towashrug:853606191711649812>')
      except Exception as e:  
        await message.edit(content=e)  
    os.remove(filename)
    await message.delete()                       

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests 
import dateutil.parser as dp

from discord import Webhook, AsyncWebhookAdapter
import aiohttp

@client.command()
async def stream(ctx,link,noembed=None):
  if link.startswith('https://youtu.be'):
    idd = link.split('/')[-1].split('?')[0]
  elif link.startswith('https://www.youtube.com/'):
    idd = link.split('=')[1].split('&')[0]   
  else:
    await ctx.send('Not a YT link!', delete_after=3.0) 
    wrong=True
  wrong=False
  print(idd)
  if wrong!=True:
    params = {'part': 'liveStreamingDetails,snippet',
            'key': os.getenv('YT_API_KEY'),
            'id': idd,
            }
    
    url = 'https://www.googleapis.com/youtube/v3/videos'
    r = requests.get(url, headers=None, params=params).json()
    isotime = r['items'][0]['liveStreamingDetails']["scheduledStartTime"]
    title = r['items'][0]['snippet']['title']
    author = r['items'][0]['snippet']['channelTitle']
    #resos = ['maxres','standard','high','medium','default']
    try:
      thumbnail = r['items'][0]['snippet']['thumbnails']['maxres']['url']
    except Exception:
      try:
        thumbnail = r['items'][0]['snippet']['thumbnails']['standard']['url']  
      except Exception:
        try:
         thumbnail = r['items'][0]['snippet']['thumbnails']['high']['url']    
        except Exception:
          try:  
            thumbnail = r['items'][0]['snippet']['thumbnails']['medium']['url']    
          except Exception:
            thumbnail = r['items'][0]['snippet']['thumbnails']['default']['url']   
    channelid = r['items'][0]['snippet']['channelId']
    parsed_t = dp.parse(isotime)
    t_in_seconds = parsed_t.timestamp()
    dsctime = "<t:"+str(t_in_seconds).split('.')[0]+":F>"
    reltime = "<t:"+str(t_in_seconds).split('.')[0]+":R>"
    dttime= datetime.strptime(isotime, "%Y-%m-%dT%H:%M:%S%z")
    dayofweek = parsed_t.weekday()

    f = open("list.txt", "a")          #add stream url and time to list.txt
    f.write(link+" "+parsed_t.strftime('%a %b %d %Y %H:%M:%S')+"\n")
    f.close()
    a_file = open("list.txt", "r")        #reads list.txt
    lines = a_file.read().splitlines()
    a_file.close()

    params2 = {'part': 'snippet',
            'key': os.getenv('YT_API_KEY'),
            'id': channelid,
            }
    
    url = 'https://www.googleapis.com/youtube/v3/channels'
    r2 = requests.get(url, headers=None, params=params2).json()
    pfp = r2['items'][0]['snippet']['thumbnails']['default']['url']
    e = discord.Embed(title=title,timestamp=dttime,description=reltime,url=link)
    e.set_author(name=author, icon_url=pfp,url="https://www.youtube.com/channel/"+channelid)
    e.set_image(url=thumbnail)
    if noembed!='noembed':
      async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('https://discord.com/api/webhooks/880667610323234877/oc31FGZ3SPfu7BCru4iOd2ULJAvyOdMi1SOaqNF58sHKBknFbdhK5zfqSZhxS4NZF9pU', adapter=AsyncWebhookAdapter(session))
        await webhook.send(embed = e)
    else:
      async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('https://discord.com/api/webhooks/880667610323234877/oc31FGZ3SPfu7BCru4iOd2ULJAvyOdMi1SOaqNF58sHKBknFbdhK5zfqSZhxS4NZF9pU', adapter=AsyncWebhookAdapter(session))
        await webhook.send(reltime +" **"+author+"** - ["+title+"](<"+link+">)")      
    await ctx.message.delete()
    try:
      client.loop.create_task(run_at(parsed_t.replace(tzinfo=None),open_url(link),link))
    except Exception as e:
      await ctx.send('Error: '+e)  

async def clear_list():
  a_file = open("list.txt", "r")        
  lines = a_file.read().splitlines()
  a_file.close()
  with open("list.txt", "w+") as r:    
    for i in lines:
        if i.split(' ')[0] != url:
            r.write(i+"\n")    

async def open_url(url):
  print(str(url)+ " is starting!")
  f = open("log.txt", "a")      
  f.write("open_url running "+url+"\n")
  f.close()
  
  avi_guild = client.get_guild(603147860225032192)
  while avi_guild == None:
    avi_guild = client.get_guild(603147860225032192)
    await asyncio.sleep(1)
  else:  
    print('got guild!')
    sched_ch = avi_guild.get_channel(879702977898741770)
    print('got channel!')
    messages = await sched_ch.history(limit=200).flatten()
    print('got messages')
  
  count = 0
  for msg in messages:
    #print(msg)
    if msg.reference is not None and not msg.is_system(): 
      
      
      msg_id = int(msg.reference.message_id)
      msgg = await sched_ch.fetch_message(msg_id)
      for i in msgg.embeds:
        if i.url == url:
          print(i.url)
          count += 1
  print(str(count) + ' times')    

  if count == 0:
    for msg in messages:
      for i in msg.embeds:
      #  print(i.url)
        if i.url == url: 
          print('found specific message')
          print(msg.jump_url.split('/')[-1])
          msg_id = int(msg.jump_url.split('/')[-1])
          msg = await sched_ch.fetch_message(msg_id)
          await msg.reply('<@&888794254837706804> Starting!')
          #await msg.reply('test')
  await clear_list()  
  
       



from petpetgif import petpet  
import requests
from io import BytesIO

@client.command()
async def pet(ctx,url):
  if (ctx.message.mentions.__len__()>0):
    for user in ctx.message.mentions:
      pfp =requests.get(user.avatar_url)
      source = BytesIO(pfp.content) # file-like container to hold the emoji in memory
      source.seek(0)
      dest = BytesIO() # container to store the petpet gif in memory
      petpet.make(source, dest)
      dest.seek(0)
      webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
      await webhook.send(
            file=discord.File(dest, filename=f"petpet.gif"), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)

      webhooks = await ctx.channel.webhooks()
      for webhook in webhooks:
              await webhook.delete()
  elif url.startswith('http'):
    pfp =requests.get(url)
    source = BytesIO(pfp.content) # file-like container to hold the emoji in memory
    source.seek(0)
    dest = BytesIO() # container to store the petpet gif in memory
    petpet.make(source, dest)
    dest.seek(0)
    webhook = await ctx.channel.create_webhook(name=ctx.message.author.name)
    await webhook.send(
          file=discord.File(dest, filename=f"petpet.gif"), username=ctx.message.author.name, avatar_url=ctx.message.author.avatar_url)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
            await webhook.delete()

@client.command()
async def sched(ctx,url):
  sched_ch = client.get_guild(603147860225032192).get_channel(879702977898741770)
  messages = await sched_ch.history(limit=200).flatten()
  #print(messages)
  count = 0
  for msg in messages:
    #print(msg)
    if msg.reference is not None and not msg.is_system(): 
      
      
      msg_id = int(msg.reference.message_id)
      msgg = await sched_ch.fetch_message(msg_id)
      for i in msgg.embeds:
        if i.url == url:
          print(i.url)
          count += 1
  print(str(count) + ' times')        

        
         


@client.command()
async def tasks(ctx):
  # tasks = client.loop.all_tasks()
  # for i in tasks:
  #   await ctx.send(i.get_coro())
  #   await ctx.send(i.get_name())
 client.loop.set_debug(True)

@client.command()
async def ping(ctx):
    await ctx.send(f'My ping is {round (client.latency * 1000)}ms!')


@client.command()
async def makeembed(ctx, title, description):
  embed=discord.Embed(title=title, description=description)
  await ctx.send(embed=embed)
  await ctx.message.delete()  

@client.command()
async def editembed(ctx, id: int, title, description): 
  msg = await ctx.fetch_message(id)
  embed=discord.Embed(title=title, description=description)
  await msg.edit(embed=embed)
  await ctx.message.delete()  
# ----------------------------------------------------
# HELP
@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Commands",   description = 'Here are my sussy commands!\nUse __**k.help <command>**__ for more info on that command.')
  em.add_field(name="copypasta", value="glasses\nnene\nnenelong\nstopamongus\nconfession\nwristworld")
  em.add_field(name="sus", value="on\noff\nmegasus\nbulk")
  em.add_field(name="why", value="fortnite")
  em.add_field(name="others", value="emote\ngetemotes\nbadapple\nclip\nfastclip\nclipaudio\ndownload\nstream\npet")
  em.add_field(name="reactions",value="fmega\nkotowaru\nascend\njizz")
  em.add_field(name="vc",value="join\nstop\nstoploop\nleave\nletsgo\nvtubus\nding\nyodayo\nyodazo\njonathan\njoseph\njotaro\njosuke\ngiorno\nkira\npillarmen\nbotansneeze\nboom\nogey\nrrat\nfart\nmogumogu\nbababooey\ndog\ntotsugeki\ntacobell\namongus\ndanganronpa\nwater\nnecoarc\nvsauce")
  em.add_field(name="TTS",value=" just do ] while in VC (\"k.help tts\" for more info)")
  await ctx.send(embed = em)


@help.command()
async def glasses(ctx):
  em = discord.Embed(title = "Glasses",   description = 'Gives the entire fubuki glasses copypasta')
  await ctx.send(embed = em)

@help.command()
async def nene(ctx):
  em = discord.Embed(title = "Nene",   description = 'Gives Nenechi\'s full title')
  await ctx.send(embed = em)
@help.command()
async def nenelong(ctx):
  em = discord.Embed(title = "Nene",   description = 'Gives Nenechi\'s LONGER full title')
  await ctx.send(embed = em)
@help.command()
async def on(ctx):
  em = discord.Embed(title = "On",   description = 'Enables permanent sus mode. Sus replies do not get deleted within 3 seconds.')
  await ctx.send(embed = em)
@help.command()
async def off(ctx):
  em = discord.Embed(title = "Off",   description = 'Disables permanent sus mode. Sus replies get deleted within 3 seconds.')
  await ctx.send(embed = em)
@help.command()
async def megasus(ctx):
  em = discord.Embed(title = "Megasus",   description = 'Gives some random amongus copypasta I found on reddit.')
  await ctx.send(embed = em)
@help.command()
async def bulk(ctx):
  em = discord.Embed(title = "Bulk",   description = 'Sends sus messages in bulk.')
  em.add_field(name="**Syntax**", value="k.bulk <number>")
  await ctx.send(embed = em)

@help.command()
async def stopamongus(ctx):
  em = discord.Embed(title = "Stop posting about Among Us!",   description = 'Sends the stop posting about among us copypasta')
  await ctx.send(embed = em)
@help.command()
async def confession(ctx):
  em = discord.Embed(title = "Matsuri's Confession",   description = 'Sends Matsuri\'s confession to Fubuki')
  await ctx.send(embed = em)
@help.command()
async def fortnite(ctx):
  em = discord.Embed(title = "Fortnite",   description = 'Sends the fortnite dance in text')
  await ctx.send(embed = em)
@help.command()
async def emote(ctx):
  em = discord.Embed(title = "Emote",   description = 'Sends an animated emote from any server that this bot is in.')
  em.add_field(name="**Syntax**", value="k.emote <emotename>")
  em.add_field(name="**Aliases**", value="e")
  await ctx.send(embed = em)
@help.command()
async def getemotes(ctx):
  em = discord.Embed(title = "Get Emotes!",   description = 'Sends all emotes that this bot has. It has emotes for all servers it\'s in.')
  em.add_field(name="**Aliases**", value="ge")
  await ctx.send(embed = em)  
@help.command()
async def wristworld(ctx):
  em = discord.Embed(title = "Wristworld",   description = 'Sends the wristworld miku copypasta.')
  await ctx.send(embed = em)  
@help.command()
async def fmega(ctx):
  em = discord.Embed(title = "F Mega!",   description = 'Sends the F MEGA gif from Jojo\'s.')
  await ctx.send(embed = em)  
@help.command()
async def kotowaru(ctx):
  em = discord.Embed(title = "Daga kotowaru!",   description = 'Use this to refuse someone\'s offer')
  await ctx.send(embed = em)    
@help.command()
async def ascend(ctx):
  em = discord.Embed(title = "Ascend to Heaven!",   description = 'Use this to to ascend when something glorious occurs.')
  await ctx.send(embed = em)     

@help.command()
async def jizz(ctx):
  em = discord.Embed(title = "Jizz",   description = 'Use this to jizz.')
  await ctx.send(embed = em)

@help.command()
async def letsgo(ctx):
  em = discord.Embed(title = "Let's go!",   description = 'Playus \'Let\'s gooo\' in vc')
  await ctx.send(embed = em)  

@help.command()
async def vtubus(ctx):
  em = discord.Embed(title = "Vtubus",   description = 'vtubus')
  await ctx.send(embed = em)     

@help.command()
async def ding(ctx):
  em = discord.Embed(title = "Ding ding ding ding ding ddi di ding",   description = 'amongus')
  await ctx.send(embed = em)  

@help.command()
async def yodayo(ctx):
  em = discord.Embed(title = "Yo dayo!",   description = 'Plays Ayame\'s \'Yo dayo!\' in VC')
  await ctx.send(embed = em)  

@help.command()
async def yodazo(ctx):
  em = discord.Embed(title = "Yo dazo!",   description = 'Plays Ayame\'s \'Yo dazo!\' in VC')
  await ctx.send(embed = em)       

@help.command()
async def jonathan(ctx):
  em = discord.Embed(title = "Jonathan's theme",   description = 'Plays Jonathan\'s theme in VC')
  await ctx.send(embed = em)      

@help.command()
async def joseph(ctx):
  em = discord.Embed(title = "Joseph's theme",   description = 'Plays Joseph\'s theme in VC')
  await ctx.send(embed = em)      

@help.command()
async def jotaro(ctx):
  em = discord.Embed(title = "Jotaro's theme",   description = 'Plays Jotaro\'s theme in VC')
  await ctx.send(embed = em)      

@help.command()
async def josuke(ctx):
  em = discord.Embed(title = "Josuke's theme",   description = 'Plays Josuke\'s theme in VC')
  await ctx.send(embed = em)      

@help.command()
async def giorno(ctx):
  em = discord.Embed(title = "Giorno's theme",   description = 'Plays Giorno\'s theme in VC')
  await ctx.send(embed = em)        

@help.command()
async def kira(ctx):
  em = discord.Embed(title = "Yoshikage Kira's theme",   description = 'Plays Yoshikage Kira\'s theme in VC')
  await ctx.send(embed = em)   

@help.command()
async def pillarmen(ctx):
  em = discord.Embed(title = "Pillar Men Theme",   description = 'Plays the Pillar Men Theme in VC')
  await ctx.send(embed = em)     

@help.command()
async def tts(ctx):
  em = discord.Embed(title = "Text to speech",   description = 'Send a TTS message in VC')
  em.add_field(name="**Syntax**", value="] <message>")
  em.add_field(name="**Accents**", value="] (US default)\n]au (Australia)\n]uk (United Kingdom)\n]in (India)")
  await ctx.send(embed = em)               

@help.command()
async def badapple(ctx):
  em = discord.Embed(title = "Bad Apple but in custom emotes",   description = 'Sends 80 animated emotes that all make up the Bad Apple PV (Only works on PC)')
  em.add_field(name="**Emotes by:**", value="https://github.com/gohjoseph")
  await ctx.send(embed = em) 

@help.command()
async def clip(ctx):
  em = discord.Embed(title = "Clip a YT Video",   description = 'clips a YouTube video given the start and end times (HH:MM:SS)\n**SLOWER** than `fastclip` but accurate')
  em.add_field(name="**Syntax**", value="k.clip <url> <start time> <end time> <filename>")
  em.add_field(name="**Example**", value="k.clip https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 filename")
  await ctx.send(embed = em)

@help.command()
async def fastclip(ctx):
  em = discord.Embed(title = "Quickly clip a YT Video",   description = 'clips a YouTube video given the start and end times (HH:MM:SS)\n**FASTER** than `clip` but will start at the nearest keyframe, so it\'ll start a couple seconds earlier than the given timestamp')
  em.add_field(name="**Syntax**", value="k.clip <url> <start time> <end time> <filename>")
  em.add_field(name="**Example**", value="k.fastclip https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:52 00:01:05 filename")
  await ctx.send(embed = em)

@help.command()
async def download(ctx):
  em = discord.Embed(title = "Download a YT Video",   description = 'Download a YouTube of your choice')
  em.add_field(name="**Syntax**", value="k.download <url>")
  await ctx.send(embed = em)

@help.command()
async def botansneeze(ctx):
  em = discord.Embed(title = "Botan Sneeze",   description = 'because fuck you, have a botan sneeze')
  em.add_field(name="**Syntax**", value="k.botansneeze [loop]")
  await ctx.send(embed = em)  

@help.command()
async def boom(ctx):
  em = discord.Embed(title = "Vine Boom SFX",   description = 'plays the funni boom sfx in vc')
  await ctx.send(embed = em)  

@help.command()
async def ogey(ctx):
  em = discord.Embed(title = "Ogey...",   description = 'Plays Pekora\'s ogey in VC.')
  em.add_field(name="**Aliases**", value="ogei")
  await ctx.send(embed = em)

@help.command()
async def rrat(ctx):
  em = discord.Embed(title = "Rrat!",   description = 'Plays Pekora\'s rrat in VC.')
  await ctx.send(embed = em)    

@help.command()
async def fart(ctx):
  em = discord.Embed(title = "Reverb fart sfx",   description = 'Plays funni fart sound in VC.')
  await ctx.send(embed = em)   

@help.command()
async def mogumogu(ctx):
  em = discord.Embed(title = "Mogu mogu!",   description = 'Plays okayu\'s mogu mogu in VC.')
  await ctx.send(embed = em)     

@help.command()
async def bababooey(ctx):
  em = discord.Embed(title = "Bababooey!",   description = 'Plays bababooey in VC.')
  await ctx.send(embed = em) 

@help.command()
async def dog(ctx):
  em = discord.Embed(title = "What the dog doin?",   description = 'Plays \'what da dog doin\' in VC.')
  await ctx.send(embed = em)      

@help.command()
async def totsugeki(ctx):
  em = discord.Embed(title = "TOTSUGEKI!!!",   description = 'Plays May\'s Totsugeki in VC.')
  await ctx.send(embed = em) 

@help.command()
async def tacobell(ctx):
  em = discord.Embed(title = "Taco Bell bong sfx",   description = 'Plays the funny taco bell sound effect in VC.')
  em.add_field(name="**Aliases**", value="bong")
  await ctx.send(embed = em) 

@help.command()
async def amongus(ctx):
  em = discord.Embed(title = "AMONGUS!",   description = 'Plays the guy yelling amongus in VC.')
  em.add_field(name="**Aliases**", value="amogus")
  await ctx.send(embed = em) 

@help.command()
async def danganronpa(ctx):
  em = discord.Embed(title = "Class trial time!",   description = 'Plays \'議論 -HEAT UP-\' from Danganronpa in VC.')
  em.add_field(name="**Aliases**", value="classtrial")
  await ctx.send(embed = em) 

@help.command()
async def join(ctx):
  em = discord.Embed(title = "Join VC",   description = 'Sus bot will enter the VC.')
  await ctx.send(embed = em) 

@help.command()
async def stop(ctx):
  em = discord.Embed(title = "STOP!",   description = 'Sus bot will stop playing if it\'s playing something in VC.')
  await ctx.send(embed = em) 

@help.command()
async def stoploop(ctx):
  em = discord.Embed(title = "STOP THE LOOP!",   description = 'Sus bot will stop playing if it\'s playing something in VC that has loop mode enabled.')
  em.add_field(name="**How loop???**", value="k.commandname loop")
  await ctx.send(embed = em) 

@help.command()
async def leave(ctx):
  em = discord.Embed(title = "Sayonara...",   description = 'Sus bot will leave the VC.')
  await ctx.send(embed = em) 

@help.command()
async def stream(ctx):
  em = discord.Embed(title = "YouTube Stream Time Embed",   description = 'Sends an embed of a YouTube stream with its start time.')
  em.add_field(name="**Syntax**", value="k.stream https://youtu.be/wNMW87foNAI")
  await ctx.send(embed = em) 

@help.command()
async def water(ctx):
  em = discord.Embed(title = "Water and Water and Water Water",   description = 'Plays \'Water and Water and Water Water\'in VC.')
  await ctx.send(embed = em) 

@help.command()
async def necoarc(ctx):
  em = discord.Embed(title = "Neco arc",   description = 'Plays neco arc in VC.')
  await ctx.send(embed = em) 

@help.command()
async def vsauce(ctx):
  em = discord.Embed(title = "Vsauce music",   description = 'Plays the vsauce music in VC.')
  await ctx.send(embed = em)   

@help.command()
async def gigachad(ctx):
  em = discord.Embed(title = "Gigachad",   description = 'Plays a bit of \'Can You Feel My Heart\' in VC.')
  await ctx.send(embed = em)  

@help.command()
async def pet(ctx):
  em = discord.Embed(title = "Pet user",   description = 'Sends a gif of the mentioned user being petted.')
  em.add_field(name="**Syntax**", value="k.pet <mentioned user>\nk.pet <image url>")
  await ctx.send(embed = em) 

@help.command()
async def clipaudio(ctx):
  em = discord.Embed(title = "Clip Audio",   description = 'Clips the audio of a given YouTube video')
  em.add_field(name="**Syntax**", value="k.clipaudio <url> <start time> <end time> <filename> <filetype>")
  em.add_field(name="**Filetypes**", value="mp3\nwav\nogg")
  em.add_field(name="**Example**", value="k.clipaudio https://www.youtube.com/watch?v=UIp6_0kct_U 00:00:56 00:01:05 poger mp3")
  await ctx.send(embed = em)  

async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.now()
    await asyncio.sleep((dt - now).total_seconds())

async def run_at(dt, coro, url):
    now = datetime.now()
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
    print(url + " is scheduled!")
    f = open("log.txt", "a")      
    f.write(url +" - scheduled at "+nowstr+"\n")
    f.close()
    await wait_until(dt)
    f = open("log.txt", "a")      
    f.write(url +" starting!"+"\n")
    f.close()
    return await coro

def precheck():
    
    if not os.path.isfile('list.txt'):
        file = open("list.txt", "w") #creates txt if doesn't exist
        file.close() 
    a_file = open("list.txt", "r")        #reads the txt
    lines = a_file.read().splitlines()
    a_file.close()
    #print(lines)
    with open("list.txt", "w+") as r:    
     for i in lines:
         later = datetime.strptime(i.split(' ', 1)[1], '%a %b %d %Y %H:%M:%S')
         now  = datetime.now()
         
         if later > now:
             r.write(i+"\n")
         url = i.split(' ')[0]    
         day = i.split(' ')[1]
         timee = i.split(' ')[5]    
         if later > now + timedelta(days=6):
                 print('more than 1 week')
         else:   
          # loop = asyncio.new_event_loop()
          # asyncio.set_event_loop(loop)

          # loop.run_until_complete()
          # loop.close()
          client.loop.create_task(run_at(later,open_url(url),url))
            



tcheck = threading.Thread(target=precheck) 
tcheck.start() 
print('schedules checked!')
keep_alive()
client.run(os.getenv('TOKEN'))





# if __name__ == '__main__':
    # run app in debug mode on port 5000
    #schedule.clear()
