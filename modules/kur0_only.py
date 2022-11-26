from disnake.ext import commands
import disnake
import os
import glob
import json
from lorem.text import TextLorem
import aiohttp
from dotenv import load_dotenv
from myfunctions import subprocess_runner
import asyncio


class Kur0only(commands.Cog):
    def __init__(self, client):
        self.client = client

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
    async def editembed(self, ctx, id: int, title, description):
        if description.startswith("https"):
            print("description is url")
            msg = await ctx.fetch_message(id)
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
            msg = await ctx.fetch_message(id)
            embed = disnake.Embed(title=title, description=description)
            await msg.edit(embed=embed)
            await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def repost(self, ctx, url):
        target_drive = "pog6"
        msg = await ctx.send("Checking FB token...")
        access_token = os.getenv("FB_ACCESS_TOKEN")
        fb_app_id = os.getenv("FB_APP_ID")
        fb_app_secret = os.getenv("FB_APP_SECRET")
        fb_url = f"https://graph.facebook.com/v14.0/debug_token?input_token={access_token}&access_token={fb_app_id}|{fb_app_secret}"
        async with aiohttp.ClientSession() as session:
            async with session.get(fb_url) as response:
                fb_json = await response.json()
        valid_token = fb_json["data"]["is_valid"]
        epoch_expires = (
            "**Never**"
            if fb_json["data"]["expires_at"] == 0
            else f"<t:{fb_json['data']['expires_at']}:R>"
        )
        epoch_access_expires = f"<t:{fb_json['data']['data_access_expires_at']}:R>"
        if not valid_token:
            await msg.edit(
                content=f"{msg.content}\n{fb_json['data']['error']['message']}"
            )
            return
        await ctx.send(
            f"Token expires {epoch_expires}\nAccess expires {epoch_access_expires}"
        )
        msg = await msg.edit(content=f"{msg.content}Done\nChecking for updates...")
        coms = ["rclone/rclone", "selfupdate"]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        msg = await msg.edit(content=f"{msg.content}\n{stdout.decode()}")
        msg = await msg.edit(content=f"{msg.content}\nDownload config file...")
        coms = [
            "wget",
            os.getenv("RCLONE_CONFIG_URL"),
            "-O",
            "/home/kur0/.config/rclone/rclone.conf",
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        msg = await msg.edit(content=f"{msg.content}Done!")
        if "www.youtube.com/watch" in url:
            fixed_link = f"https://youtu.be/{url[32:43]}"
        elif "www.youtube.com/shorts" in url:
            fixed_link = f"https://youtu.be/{url[27:38]}"
        elif "youtu.be" in url:
            fixed_link = url[0:28]

        else:
            fixed_link = url
        # download vid
        tasks = []
        msg = await msg.edit(content=f"{msg.content}\nDownloading video and info...")

        async def dl_vid():
            coms = [
                "yt-dlp",
                "-i",
                "--no-warnings",
                "--yes-playlist",
                "--add-metadata",
                "--merge-output-format",
                "mkv",
                "--all-subs",
                "--write-sub",
                "--convert-subs",
                "srt",
                "--embed-subs",
                "-f",
                "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best",
                "-o",
                "%(title)s-%(id)s.%(ext)s",
                fixed_link,
            ]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)

            if out.returncode == 0:
                return f"  Download success! ({out.returncode})"
            else:
                try:
                    error = f"Downloading fail:\n Return code: {out.returncode}\n{stderr.decode()}"
                except:
                    error = f"Downloading fail:\n Return code: {out.returncode}\n{stdout.decode()}"
                raise Exception(error)

        tasks.append(dl_vid())

        async def title_fname():
            coms = [
                "yt-dlp",
                "--get-title",
                "--get-filename",
                "-o",
                "%(title)s-%(id)s",
                "--no-warnings",
                fixed_link,
            ]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            result = stdout.decode()
            title = result.splitlines()[-2]
            filename = result.splitlines()[-1]
            print(f"{title}\n{filename}")

            if out.returncode == 0:
                return title, filename, f"  Data grab success! ({out.returncode})"
            else:
                try:
                    error = f"Data grab fail:\n Return code: {out.returncode}\n{stderr.decode()}"
                except:
                    error = f"Data grab fail:\n Return code: {out.returncode}\n{stdout.decode()}"
                raise Exception(error)

        tasks.append(title_fname())

        gathered = await asyncio.gather(*tasks)
        dl_result = gathered[0]
        title, filename, info_result = gathered[1]        
        fname1 = glob.glob(f"{glob.escape(filename)}.*")
        for i in fname1:
            if not i.endswith(".srt") and not i.endswith(".json"):
                fname = i
            else:
                os.remove(i)
        print(fname)
        # copy to drive
        tasks = []
        msg = await msg.edit(
            content=f"{msg.content}\n{dl_result}\n{info_result}\nCopying to Drive and uploading to FB..."
        )

        async def to_drive():
            coms = [
                "rclone/rclone",
                "copy",
                fname,
                f"{target_drive}:/archived youtube vids/",
                "--transfers",
                "20",
                "--checkers",
                "20",
                "-v",
                "--stats=5s",
                "--buffer-size",
                "128M",
                "--drive-chunk-size",
                "128M",
                "--drive-acknowledge-abuse",
                "--drive-keep-revision-forever",
                "--drive-server-side-across-configs=true",
                "--suffix=2021_12_22_092152",
                "--suffix-keep-extension",
            ]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)

            if out.returncode == 0:
                return f"Copy to Drive success! ({out.returncode})"
            else:
                try:
                    error = f"Copy to Drive fail:\n Return code: {out.returncode}\n{stderr.decode()}"
                except:
                    error = f"Copy to Drive fail:\n Return code: {out.returncode}\n{stdout.decode()}"
                raise Exception(error)

        tasks.append(to_drive())

        async def to_fb():
            url = f"https://graph-video.facebook.com/v8.0/100887555109330/videos?access_token={access_token}&limit=10"
            data = aiohttp.FormData()
            data.add_field("file", open(fname, mode="rb"), filename="vid.mp4")
            data.add_field("description", f"{title}\n(NOT MINE) Source: {fixed_link}")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as response:
                    data = await response.json()
                    status_code = response.status
            if status_code != 200:
                raise Exception(f"FB FAIL:\n{json.dumps(data, indent=4)}")
            else:
                print("We gucci, my dude.")
                vid_id = data["id"]
                os.remove(fname)
                post_link = f"https://web.facebook.com/100887555109330/videos/{vid_id}"
                return (
                    f"{title} has been uploaded!\n"
                    f"Vid link: https://web.facebook.com/100887555109330/videos/{vid_id}\n"
                    f"Share to FB: https://www.facebook.com/sharer.php?u={post_link}"
                )

        tasks.append(to_fb())

        gathered = await asyncio.gather(*tasks)
        gathered_str = "\n".join(gathered)
        await ctx.send(gathered_str)
        await msg.delete()

    @commands.command()
    @commands.is_owner()
    async def checkhelp(self, ctx):
        f = open("modules/commands.json")
        data = json.load(f)
        f.close()
        hidden_commands = data["hidden"]
        comm_list = []
        for i in data:
            if i == "hidden":
                pass
            else:
                comm_list += data[i]

        public_commandss = [
            c.name for c in self.client.commands if c.name not in hidden_commands
        ]
        diffcomms = [c for c in public_commandss if c not in comm_list]
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
            c for c in comm_list if c not in commands_with_help_msg and c not in aliases
        ]
        diffcomms2_joined = "\n".join(diffcomms2)
        await ctx.send(f"Commands without help commands are:\n{diffcomms2_joined}")

    @commands.command()
    @commands.is_owner()
    async def ytbypass(self, ctx, text):
        letters = [char for char in text]
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


def setup(client):
    client.add_cog(Kur0only(client))
