from disnake.ext import commands
import time
import re
import requests
import os
import asyncio
from urllib.request import urlopen

class CheckComment(commands.Cog):
    @commands.command()
    async def checkcomment(self, ctx, link):
        comment_start_time = time.time()
        comment_end_time = comment_start_time + (60 * 5)
        community_comment = False
        
        if re.search(r"https:\/\/www.youtube.com\/watch\?v=.+&lc=.+(\..+)?", link):
            id = re.search(
                r"(?<=https:\/\/www.youtube.com\/watch\?v=.{11}&lc=).+(\..+)?", link
            ).group(0)
        elif re.search(r"https://www.youtube.com/channel/.+?/community\?lc=.+?&lb=.+", link):
            id = re.search(r"(?<=lc=).+?(?=&lb)", link).group(0)
            community_comment = True
        else:
            await ctx.send("Not a YT comment link!", delete_after=3.0)
            return
        print(id)
        if not community_comment:
            params = {
                "part": "snippet",
                "key": os.getenv("YT_API_KEY"),
                "id": id,
            }
            url = "https://youtube.googleapis.com/youtube/v3/comments"
            msg = await ctx.send("Searching...")
            while time.time() < comment_end_time:
                r = requests.get(url, headers=None, params=params)
                time_passed = time.time() - comment_start_time
                if r.status_code == 200:
                    try:
                        name = r.json()["items"][0]["snippet"][
                            "authorDisplayName"
                        ]  # DON'T REMOVE
                        comment_content = r.json()["items"][0]["snippet"][
                            "textOriginal"
                        ]  # DON'T REMOVE
                        print(f"{name}: {comment_content[:15]}...")
                        await msg.edit(
                            content=f"{time_passed:.2f}s: We're good! ({r.status_code})"
                        )
                    except:
                        await msg.edit(
                            content=f"{time_passed:.2f}s: FAIL! {ctx.author.mention}"
                        )
                        return
                else:
                    await msg.edit(
                        content=f"{time_passed:.2f}s: FAIL! ({r.status_code}) {ctx.author.mention}"
                    )
                    return
                await asyncio.sleep(10)
            await msg.edit(content=f"{time_passed:.2f} seconds passed and it's still up!")
        else:     #is community comment   
            msg = await ctx.send("Searching...")
            response = urlopen(link)
            result = response.read().decode(response.headers.get_content_charset())
            index = result.find("continuationCommand")
            if index != 0:
                chunk = result[index:index+1000]
                results = re.findall(r'(?<=continuationCommand":{"token":").+?(?=")',chunk)
                if results:
                    continuation_token = results[0]
                else:
                    await ctx.send("Could not find continuation token. Sorry :((")
                    return                    
            else:
                await ctx.send("Could not find continuation token. Sorry :(")
                return        
            while time.time() < comment_end_time:            
                headers = {'content-type': 'application/json'}           
                data = {"context":{"client":{"clientName":"WEB","clientVersion":"2.2022011"}},"continuation":continuation_token}
                                                                                      #VVVVVVVVVVVV seems to be some public API key on youtube. https://stackoverflow.com/a/70793047
                r = requests.post('https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=true',headers=headers,json=data)
                found_index = r.text.find(id)
                print(f"Found? {found_index}")            
                
                time_passed = time.time() - comment_start_time
                if found_index != -1:
                    await msg.edit(
                        content=f"{time_passed:.2f}s: We're good! (Status: {r.status_code} | Index: {found_index})"
                    )
                else:
                    await msg.edit(
                        content=f"{time_passed:.2f}s: FAIL! {ctx.author.mention}"
                    )
                    return
                await asyncio.sleep(10)
            await msg.edit(content=f"{time_passed:.2f} seconds passed and it's still up!")        
        
        



def setup(client):
    client.add_cog(CheckComment(client))
