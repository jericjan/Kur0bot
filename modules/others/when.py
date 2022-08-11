from disnake.ext import commands
import os
import requests
import dateutil.parser as dp
from myfunctions import msg_link_grabber


class When(commands.Cog):


    async def grab_msg_time(self,msg):
        time = msg.created_at
        return time.strftime("%b %-d, %Y - %I:%M:%S.%f %p %Z")

    @commands.command()
    async def when(self, ctx, link=None):
        try:
            link = await msg_link_grabber.grab_link(ctx, link)
        except:
            pass
        print(link)
        if link:
            if link.startswith("https://youtu.be"):
                idd = link.split("/")[-1].split("?")[0]
                wrong = False
            elif link.startswith("https://www.youtube.com/"):
                idd = link.split("=")[1].split("&")[0]
                wrong = False
            else:
                await ctx.send("Not a YT link!", delete_after=3.0)
                if ctx.message.reference:
                    await ctx.send("Gonna get time message was posted tho cuz yes...", delete_after=3.0)
                    time = await self.grab_msg_time(ctx.message.reference.resolved)
                    await ctx.send(time)
                return
        else:            
            if ctx.message.reference:
                await ctx.send("You replied to a message & it has no link, getting time message posted instead...", delete_after=3.0)
                time = await self.grab_msg_time(ctx.message.reference.resolved)
                await ctx.send(time)
            return
            wrong = True
        print(idd)
        if wrong != True:
            params = {
                "part": "snippet,liveStreamingDetails",
                "key": os.getenv("YT_API_KEY"),
                "id": idd,
            }
            url = "https://www.googleapis.com/youtube/v3/videos"
            r = requests.get(url, headers=None, params=params).json()
            publish_time = r["items"][0]["snippet"]["publishedAt"]
            epoch_time = dp.parse(publish_time).timestamp()
            await ctx.send(f"Video was published at <t:{epoch_time:.0f}:F>")
            if "liveStreamingDetails" in r["items"][0].keys():
                stream_start = r["items"][0]["liveStreamingDetails"]["actualStartTime"]
                epoch_stream_start = dp.parse(stream_start).timestamp()
                if "actualEndTime" in r["items"][0]["liveStreamingDetails"].keys():
                    stream_end = r["items"][0]["liveStreamingDetails"]["actualEndTime"]
                    epoch_stream_end = f"<t:{dp.parse(stream_end).timestamp():.0f}:F>"
                else:
                    epoch_stream_end = "**Not ended yet.**"
                stream_schedule = r["items"][0]["liveStreamingDetails"][
                    "scheduledStartTime"
                ]
                epoch_stream_schedule = dp.parse(stream_schedule).timestamp()
                await ctx.send(
                    f"Stream started at <t:{epoch_stream_start:.0f}:F>\nStream ended at {epoch_stream_end}\nStream was schedule to start at <t:{epoch_stream_schedule:.0f}:F>"
                )


def setup(client):
    client.add_cog(When(client))
