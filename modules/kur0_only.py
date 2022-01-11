from disnake.ext import commands
import disnake
import asyncio
import subprocess
import os
import requests
import glob
import json


class Kur0only(commands.Cog):
    @commands.command()
    async def makeembed(self, ctx, title, description):
        if ctx.author.id == 396892407884546058:
            print("is kur0")
            if description.startswith("https"):
                print("description is url")
                x = requests.get(
                    f"https://quiet-sun-6d6e.cantilfrederick.workers.dev/?{description}"
                )
                embed = disnake.Embed(title=title, description=x.text)
                await ctx.send(embed=embed)
                await ctx.message.delete()
            else:
                print("description is text")
                embed = disnake.Embed(title=title, description=description)
                await ctx.send(embed=embed)
                await ctx.message.delete()
        else:
            print(ctx.author.id)
            await ctx.send("only kur0 can do this lel")
            await ctx.message.delete()

    @commands.command()
    async def editembed(self, ctx, id: int, title, description):
        if ctx.author.id == 396892407884546058:
            print("is kur0")
            if description.startswith("https"):
                print("description is url")
                msg = await ctx.fetch_message(id)
                x = requests.get(
                    f"https://quiet-sun-6d6e.cantilfrederick.workers.dev/?{description}"
                )
                embed = disnake.Embed(title=title, description=x.text)
                await msg.edit(embed=embed)
                await ctx.message.delete()
            else:
                print("description is text")
                msg = await ctx.fetch_message(id)
                embed = disnake.Embed(title=title, description=description)
                await msg.edit(embed=embed)
                await ctx.message.delete()
        else:
            print(ctx.author.id)
            await ctx.send("only kur0 can do this lel")
            await ctx.message.delete()

    @commands.command()
    async def repost(self, ctx, url):
        if ctx.author.id == 396892407884546058:
            print("is kur0")
            msg = await ctx.send("Checking for updates...")
            coms = ["rclone/rclone", "selfupdate"]
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await out.communicate()
            msg = await msg.edit(content=f"{msg.content}\n{stdout.decode()}")
            msg = await msg.edit(content=f"{msg.content}\nDownload config file...")
            coms = [
                "wget",
                os.getenv("RCLONE_CONFIG_URL"),
                "-O",
                "/config/rclone/rclone.conf",
            ]
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await out.communicate()
            print(stdout.decode())
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
            msg = await msg.edit(content=f"{msg.content}\nDownloading video...")
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
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await out.communicate()
            print(stdout.decode())

            if out.returncode == 0:
                msg = await msg.edit(content=f"{msg.content}Done! ({out.returncode})")
            else:
                try:
                    msg = await msg.edit(
                        content=f"{msg.content}\n Return code: {out.returncode}\n{stderr.decode()}"
                    )
                except:
                    msg = await msg.edit(
                        content=f"{msg.content}\n Return code: {out.returncode}\n{stdout.decode()}"
                    )
                return

            # get title and filename
            msg = await msg.edit(
                content=f"{msg.content}\nGetting title and filename..."
            )
            coms = [
                "yt-dlp",
                "--get-title",
                "--get-filename",
                "-o",
                "%(title)s-%(id)s",
                "--no-warnings",
                fixed_link,
            ]
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await out.communicate()
            result = stdout.decode()
            title = result.splitlines()[-2]
            filename = result.splitlines()[-1]
            print(f"{title}\n{filename}")
            fname1 = glob.glob(f"{glob.escape(filename)}.*")
            for i in fname1:
                if not i.endswith(".srt") and not i.endswith(".json"):
                    fname = i
                else:
                    os.remove(i)
            print(fname)

            if out.returncode == 0:
                msg = await msg.edit(content=f"{msg.content}Done! ({out.returncode})")
            else:
                try:
                    msg = await msg.edit(
                        content=f"{msg.content}\n Return code: {out.returncode}\n{stderr.decode()}"
                    )
                except:
                    msg = await msg.edit(
                        content=f"{msg.content}\n Return code: {out.returncode}\n{stdout.decode()}"
                    )
                return
            # copy to drive
            msg = await msg.edit(content=f"{msg.content}\nCopying to Drive...")
            coms = [
                "rclone/rclone",
                "copy",
                fname,
                "g3:/archived youtube vids/",
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
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await out.communicate()
            print(stdout.decode())
            # print(stderr)

            if out.returncode == 0:
                msg = await msg.edit(content=f"{msg.content}Done! ({out.returncode})")
            else:
                try:
                    msg = await msg.edit(
                        content=f"{msg.content}\n Return code: {out.returncode}\n{stderr.decode()}"
                    )
                except:
                    msg = await msg.edit(
                        content=f"{msg.content}\n Return code: {out.returncode}\n{stdout.decode()}"
                    )
                return
            # upload to fb
            msg = await msg.edit(content=f"{msg.content}\nUploading to FB...")
            access_token = os.getenv("FB_ACCESS_TOKEN")

            url = f"https://graph-video.facebook.com/v8.0/100887555109330/videos?access_token={access_token}&limit=10"
            files = {"file": ("vid.mp4", open(fname, mode="rb"))}
            flag = requests.post(
                url,
                files=files,
                data={"description": f"{title}\n(NOT MINE) Source: {fixed_link}"},
            )  # .text
            flagg = flag.text

            data = json.loads(flagg)

            if flag.status_code != 200:
                print(flagg)

            else:
                print("We gucci, my dude.")
                vid_id = data["id"]

                if out.returncode == 0:
                    msg = await msg.edit(
                        content=f"{msg.content}Done! ({out.returncode})"
                    )
                else:
                    try:
                        msg = await msg.edit(
                            content=f"{msg.content}\n Return code: {out.returncode}\n{stderr.decode()}"
                        )
                    except:
                        msg = await msg.edit(
                            content=f"{msg.content}\n Return code: {out.returncode}\n{stdout.decode()}"
                        )
                    return
                await msg.delete()
                await ctx.send(f"{title} has been uploaded!")
                await ctx.send(
                    f"Vid link: https://web.facebook.com/100887555109330/videos/{vid_id}"
                )
                post_link = f"https://web.facebook.com/100887555109330/videos/{vid_id}"
                await ctx.send(
                    f"Share to FB: https://www.facebook.com/sharer.php?u={post_link}"
                )
                os.remove(fname)
        else:
            print(ctx.author.id)
            await ctx.send("you found secret command. only kur0 can do this tho lel")


def setup(client):
    client.add_cog(Kur0only(client))
