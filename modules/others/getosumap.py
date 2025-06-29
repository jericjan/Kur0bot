import json
import os
import re
import urllib.parse
import html
from typing import Any

import aiohttp
import dateutil.parser as dp
import disnake
from disnake.ext import commands


class GetOsuMap(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["getmap", "getosu"])
    async def getosumap(self, ctx: commands.Context[Any], *, user: disnake.Member):
        activities = user.activities
        if activities:
            activity_count = len(activities)
            not_osu_count = 0
            for activity in activities:
                print(activity)
                if isinstance(activity, disnake.Activity) and user.bot == False:
                    try:
                        if activity.application_id == 367827983903490050:
                            name = activity.details
                            if name is None:
                                await ctx.send(
                                    "Can't get any songs from this user. Sorry dawg."
                                )
                                return
                            # await ctx.send(f"details: {name}\nstate: {activity.state}")
                            name_parsed = re.findall(
                                r"(?<=^).+?(?= - )|(?<= - ).+(?= \[)|(?<= \[).+(?=\])",
                                name,
                            )
                            if len(name_parsed) > 3:
                                await ctx.send(
                                    f"Kur0's regex fucked up. Blame him. Regex found {len(name_parsed)} items. Should be 3"
                                )
                                await ctx.send("\n".join(name_parsed))
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
                                url = (
                                    f"https://osusearch.com/query/"
                                    f"?title={map_name}&"
                                    f"artist={artist}&"
                                    f"diff_name={diff_name}&"
                                    f"offset=0"
                                )
                                print(f"link is {url}")
                                async with session.get(url) as resp:
                                    response = await resp.text()
                            json_dict = json.loads(response)
                            print(json.dumps(json_dict, indent=2))
                            res_count = json_dict["result_count"]
                            if int(res_count) == 0:
                                await ctx.send(
                                    "No results. :(\nTrying again but without searching the diff..."
                                )
                                async with aiohttp.ClientSession() as session:
                                    url = (
                                        f"https://osusearch.com/query/"
                                        f"?title={map_name}&"
                                        f"artist={artist}&"
                                        f"offset=0"
                                    )
                                    print(f"link is {url}")
                                    async with session.get(url) as resp:
                                        response = await resp.text()
                                json_dict = json.loads(response)
                                print(json.dumps(json_dict, indent=2))
                                res_count = json_dict["result_count"]
                                if int(res_count) == 0:
                                    await ctx.send("Still nothing. Sorry :(")
                                    return
                            await ctx.send(f"{res_count} results!")
                            beatmaps = json_dict["beatmaps"]
                            results: list[str] = []
                            for beatmap in beatmaps:
                                title = beatmap["title"]
                                diff = beatmap["difficulty"]
                                url = f"https://osu.ppy.sh/beatmaps/{beatmap['beatmap_id']}"
                                results.append(f"[{diff:.2f}] {title}\n{url}")
                            await ctx.send("\n".join(results))
                    except AttributeError:
                        not_osu_count += 1
                else:
                    not_osu_count += 1
            if not_osu_count == activity_count:
                await ctx.send(
                    f"{user.name} isn't playing osu or isn't showing it on their activity. :("
                )
        else:
            await ctx.send(f"{user.name} is not doing anything...")

    @commands.command(aliases=["getmap2", "getosu2"])
    async def getosumap2(self, ctx: commands.Context[Any], user: str):

        API_URL = "https://osu.ppy.sh/api/v2"
        TOKEN_URL = "https://osu.ppy.sh/oauth/token"

        OSU_ID = os.getenv("OSU_ID")
        if OSU_ID is None:
            await ctx.send(
                "OSU_ID environment variable is not set. Please set it to use this command."
            )
            return
        
        OSU_SECRET = os.getenv("OSU_SECRET")
        if OSU_SECRET is None:
            await ctx.send(
                "OSU_SECRET environment variable is not set. Please set it to use this command."
            )
            return

        data: dict[str, str] = {
            "client_id": OSU_ID,
            "client_secret": OSU_SECRET,
            "grant_type": "client_credentials",
            "scope": "public",
        }
        print("getting token")
        async with aiohttp.ClientSession() as session:
            async with session.post(TOKEN_URL, data=data) as resp:
                response = await resp.json()
        token = response["access_token"]
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        params = {"key": "username"}
        print("doing thing")
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{API_URL}/users/{user}/", params=params) as resp:
                response = await resp.json()
        user_id = response["id"]
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                f"{API_URL}/users/{user_id}/recent_activity"
            ) as resp:
                recently_played_maps = await resp.json()
        desc: list[str] = []
        for osumap in recently_played_maps:
            time = dp.parse(osumap["created_at"]).timestamp()
            timestamp = f"<t:{int(time)}:R>"
            title = osumap["beatmap"]["title"]
            url = f"https://osu.ppy.sh{osumap['beatmap']['url']}"
            rank = osumap["scoreRank"]
            formatted = f"{timestamp} [{title}]({url}) [{rank}]"
            desc.append(formatted)
        em = disnake.Embed(
            title=f"{user}'s recently played maps", description="\n".join(desc)
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["getmap3", "getosu3"])
    async def getosumap3(self, ctx: commands.Context[Any], user: str):
        url = f"https://osu.ppy.sh/u/{user}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                site_contents = await resp.text()
        # print(site_contents)
        site_contents = html.unescape(site_contents)
        maps = re.findall(r"(?<=scoresRecent).+?(?=beatmapPlaycounts)", site_contents)
        maps = re.findall(
            r'(?<="url":").+?(?=",)|(?<=title":").+?(?=",)|(?<=artist":").+?(?=",)|(?<=ended_at":").+?(?=",)|(?<=pp":).+?(?=,)|(?<=accuracy":).+?(?=,)|(?<=rank":").+?(?=",)',
            maps[0],
        )

        def chunks(xs: list[str], n: int):
            n = max(1, n)
            return [xs[i : i + n] for i in range(0, len(xs), n)]

        maps = chunks(maps, 8)
        desc: list[str] = []
        for acc, time, rank, pp, _, link, artist, song in maps:
            acc = float(acc) * 100
            acc = f"{acc:.2f}"
            time = dp.parse(time).timestamp()
            timestamp = f"<t:{int(time)}:R>"
            pp = f"{float(pp):.2f}"
            link = link.replace("\\", "")
            desc.append(
                f"{timestamp}\n[{rank}] - {acc}% - {pp}pp\n[{artist} - {song}]({link})\n"
            )
        em = disnake.Embed(
            title=f"{user}'s recently played maps", description="\n".join(desc)
        )
        await ctx.send(embed=em)


def setup(client: commands.Bot):
    client.add_cog(GetOsuMap(client))
