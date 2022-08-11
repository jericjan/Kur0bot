from disnake.ext import commands
import disnake
import aiohttp
import urllib.parse
import os
import re
import json

class GetOsuMap(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["getmap","getosu"])
    async def getosumap(self, ctx, user: disnake.Member):
        activities = user.activities
        for activity in activities:
            if str(activity.type) == "ActivityType.playing" and user.bot == False:                
                if activity.application_id == 367827983903490050:
                    name = activity.details
                    if name is None:
                        await ctx.send("Can't get any songs from this user. Sorry dawg.")
                        return                    
                    #await ctx.send(f"details: {name}\nstate: {activity.state}")                    
                    name_parsed = re.findall(r"(?<=^).+?(?= - )|(?<= - ).+(?= \[)|(?<= \[).+(?=\])",name)
                    if len(name_parsed) > 3:
                        await ctx.send(f"Kur0's regex fucked up. Blame him. Regex found {len(name_parsed)} items. Should be 3")
                        await ctx.send('\n'.join(name_parsed))
                        return                       
                    artist = urllib.parse.quote(name_parsed[0])
                    map_name = urllib.parse.quote(name_parsed[1])
                    diff_name = urllib.parse.quote(name_parsed[2])                
                    # url = "https://osusearch.com/query/"
                    # data = {
                        # "title": map_name),
                        # "artist": urllib.parse.quote(artist),
                        # "diff_name":urllib.parse.quote(diff_name),
                        # "offset":"0"
                    # }
                    # headers = {
                        # "Accept": "application/json",
                        # "Content-Type": "application/json",
                    # }
                    async with aiohttp.ClientSession() as session:
                        url=f"https://osusearch.com/query/" \
                            f"?title={map_name}&" \
                            f"artist={artist}&" \
                            f"diff_name={diff_name}&" \
                            f"offset=0"
                        print(f"link is {url}")
                        async with session.get(url) as resp:
                            response = await resp.text()         
                    json_dict = json.loads(response)
                    print(json.dumps(json_dict, indent=2))
                    res_count = json_dict['result_count']                    
                    if int(res_count) == 0:
                        await ctx.send("No results. :(\nTrying again but without searching the diff...")
                        async with aiohttp.ClientSession() as session:
                            url=f"https://osusearch.com/query/" \
                                f"?title={map_name}&" \
                                f"artist={artist}&" \
                                f"offset=0"
                            print(f"link is {url}")
                            async with session.get(url) as resp:
                                response = await resp.text()         
                        json_dict = json.loads(response)
                        print(json.dumps(json_dict, indent=2))
                        res_count = json_dict['result_count']                          
                        if int(res_count) == 0:
                            await ctx.send("Still nothing. Sorry :(")
                            return
                    await ctx.send(f"{res_count} results!")
                    beatmaps = json_dict['beatmaps']
                    results = []
                    for beatmap in beatmaps:
                        title = beatmap['title']
                        diff = beatmap['difficulty']
                        url = f"https://osu.ppy.sh/beatmaps/{beatmap['beatmap_id']}"
                        results.append(f"[{diff:.2f}] {title}\n{url}")
                    await ctx.send('\n'.join(results))
                    # r=requests.get(f"https://osu.ppy.sh/api/v2/beatmaps/lookup?filename={filename}", headers={"Authorization":f"Bearer {osukey}"})
                    # r=requests.get(f"https://osu.ppy.sh/api/v2/beatmaps/lookup?filename={filename}", headers={"Authorization":f"Bearer {osukey}"})
                    # await ctx.send(f"{r.status_code}: {r.content}")

def setup(client):
    client.add_cog(GetOsuMap(client))
