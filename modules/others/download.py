from disnake.ext import commands
import disnake
import asyncio
import os
from shlex import join as shjoin
import subprocess
from aiolimiter import AsyncLimiter
import json
import re
from urllib.parse import unquote
from myfunctions import subprocess_runner, file_handler

limiter = AsyncLimiter(1, 1)


class Download(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pbar_list = []

    async def updatebar(self, msg):
        try:
            async with limiter:
                await msg.edit(content=self.pbar_list[-1])
        except Exception as e:
            if str(e).startswith("404 Not Found"):
                pass
            else:
                pass
            pass

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def download(self, ctx, link):  # reddit, facebook, instagram, tiktok, yt
        if "reddit.com" in link or "v.redd.it" in link:
            cookiecoms = [
                "gpg",
                "--pinentry-mode=loopback",
                "--passphrase",
                os.getenv("ENCRYPTPASSPHRASE"),
                "cookies/seventina.gpg",
            ]
            cookieproc, stdout, stderr = await subprocess_runner.run_subprocess(
                cookiecoms
            )
            message = await ctx.send("Downloading...")
            coms = [
                "yt-dlp",
                "-f",
                "bestvideo+bestaudio",
                "--cookies",
                "cookies/seventina",
                "--no-warnings",
                link,
            ]

            print(shjoin(coms))
            proc = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
                self.pbar_list.append(line.decode("utf-8"))
                asyncio.ensure_future(self.updatebar(message))
                await asyncio.sleep(1)
                print(f"\033[32m{line.decode('utf-8')}\033[0m")
            if proc.returncode != 0:
                success = False
                await ctx.send("return code is not 0. trying something else")
                coms = [
                    "yt-dlp",
                    "--no-warnings",
                    link,
                ]
                print(shjoin(coms))
                proc = await asyncio.create_subprocess_exec(  # reads stdout live
                    *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                while proc.returncode is None:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    self.pbar_list.append(line.decode("utf-8"))
                    asyncio.ensure_future(self.updatebar(message))
                    await asyncio.sleep(1)
                    print(f"\033[32m[{line.decode('utf-8')}\033[0m")
                    linedec = line.decode("utf-8")
                    if re.search(r"Following redirect to ", linedec):
                        success = True
                        print("match!")
                        if re.search(r"https:\/\/www.reddit.com\/over18.+", linedec):
                            link = unquote(
                                re.findall(r"https%3A%2F%2Fwww.reddit.com.+", linedec)[
                                    0
                                ]
                            )
                        else:
                            link = re.findall(r"https://.+", linedec)[0]
                        print(f"match is: {link}")
                if proc.returncode != 0 and success == False:
                    await ctx.send("return code is not 0. i give up")
                    return
            print("almost there")
            await message.edit(content="Almost there...")
            coms2 = [
                "yt-dlp",
                "--get-filename",
                "--cookies",
                "cookies/seventina",
                "--no-warnings",
                link,
            ]
            out2, stdout, stderr = await subprocess_runner.run_subprocess(coms2)
            try:
                print(f"\033[32m{stdout.decode('utf-8')}\033[0m")
                filename = stdout.decode("utf-8").split("\n")[0]
                try:
                    if filename.endswith(".mp4"):
                        await file_handler.send_file(ctx, message, filename)
                    else:
                        clean_name = f"{filename.replace(',', '')}.mp4"
                        await file_handler.send_file(ctx, message, filename, clean_name)
                except Exception as e:
                    await ctx.send(e)
                    await ctx.send(type(e).__name__)
            except disnake.HTTPException:
                await ctx.send("File too large, broski <:towashrug:853606191711649812>")
            file_handler.delete_file("cookies/seventina")
            file_handler.delete_file(filename)
            await message.delete()

        elif "facebook.com" in link:
            message = await ctx.send("Downloading...")
            # encypted with `gpg -c --pinentry-mode=loopback --passphrase 'pass' your-file.txt`
            cookiecoms = [
                "gpg",
                "--pinentry-mode=loopback",
                "--passphrase",
                os.getenv("ENCRYPTPASSPHRASE"),
                "cookies/iofifteen.gpg",
            ]
            cookieproc, stdout, stderr = await subprocess_runner.run_subprocess(
                cookiecoms
            )
            coms = [
                "yt-dlp",
                "-f",
                "b",
                "--cookies",
                "cookies/iofifteen",
                "--no-warnings",
                link,
            ]
            coms2 = [
                "yt-dlp",
                "-f",
                "b",
                "--get-filename",
                "--cookies",
                "cookies/iofifteen",
                "--no-warnings",
                link,
            ]
            proc = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
                self.pbar_list.append(line.decode("utf-8"))
                asyncio.ensure_future(self.updatebar(message))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2, stdout, stderr = await subprocess_runner.run_subprocess(coms2)
            try:
                filename = stdout.decode("utf-8").split("\n")[-2]
                await file_handler.send_file(ctx, message, filename)
            except Exception as e:
                await message.edit(content=e)
            file_handler.delete_file("cookies/iofifteen")
            file_handler.delete_file(filename)

            await message.delete()
        elif "tiktok.com" in link:
            message = await ctx.send("Downloading...")
            coms = ["yt-dlp", "-f", "b[vcodec=h264]", "--no-warnings", link]
            coms2 = [
                "yt-dlp",
                "-f",
                "b",
                "--get-filename",
                "--no-warnings",
                link,
            ]
            print(shjoin(coms))
            proc = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
                self.pbar_list.append(line.decode("utf-8"))
                asyncio.ensure_future(self.updatebar(message))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2, stdout, stderr = await subprocess_runner.run_subprocess(coms2)
            try:
                filename = stdout.decode("utf-8").split("\n")[0]
                await file_handler.send_file(ctx, message, filename)
            except Exception as e:
                await message.edit(content=e)
            file_handler.delete_file(filename)
            await message.delete()
        elif "bilibili.com" in link:
            message = await ctx.send(
                "Bilibili? <:oka:944181217467723826>\n Let me do something different here. Give me a moment..."
            )
            coms = ["yt-dlp", "--get-url", "-j", "--no-warnings", link]
            proc, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            url = stdout.splitlines()[0]
            json_str = stdout.splitlines()[1]
            json_dict = json.loads(json_str)
            bilibili_id = json_dict["webpage_url_basename"]
            filename = f"bilibili_{bilibili_id}.mp4"
            coms2 = ["ffmpeg", "-i", url, "-c", "copy", "-y", filename]
            out2 = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="Downloading...")
            else:
                await file_handler.send_file(ctx, message, filename)
            file_handler.delete_file(filename)
            await message.delete()
        elif "instagram.com" and "/stories/" in link:
            message = await ctx.send("Downloading...")
            cookiecoms = [
                "gpg",
                "--pinentry-mode=loopback",
                "--passphrase",
                os.getenv("ENCRYPTPASSPHRASE"),
                "cookies/morbius.gpg",
            ]
            cookieproc, stdout, stderr = await subprocess_runner.run_subprocess(
                cookiecoms
            )           
            coms = ["yt-dlp", "-f", "b", "--no-warnings", "--cookies", "cookies/morbius",link]
            coms2 = ["yt-dlp", "-f", "b", "--get-filename", "--no-warnings", "--cookies", "cookies/morbius", link]                
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            await message.edit(content="Almost there...")
            out2, stdout, stderr = await subprocess_runner.run_subprocess(coms2)
            try:
                filenames = [x for x in stdout.decode("utf-8").split("\n") if x]
                if len(filenames) == 1:
                    await file_handler.send_file(ctx, message, filenames[0])
                else:
                
                    msg = await ctx.send(
                        f"This story has {len(filenames)} videos. Instagram is weird and I can't exactly find which video this is in the story. Tell me the nth video that you want (Ex: 2). You have 5 minutes.\nType \"all\" and I'll DM you all the videos."
                    )

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    try:
                        await_msg = await self.client.wait_for(
                            "message", check=check, timeout=300
                        )
                        if await_msg.content.isdecimal():
                            index = int(await_msg.content) - 1
                            await file_handler.send_file(ctx, message, filenames[index])
                        elif await_msg.content.lower() == "all":
                            for file in filenames:
                                await ctx.author.send(file=disnake.File(file))                   
                        else:
                            await ctx.send("Invalid!", delete_after=3)
                            await ctx.message.delete()
                        await await_msg.delete()
                    except asyncio.TimeoutError:
                        await ctx.send("Too slow lmao!", delete_after=3)
                        await ctx.message.delete()
                    await msg.delete()                         

            except Exception as e:
                await ctx.send(e)           
            file_handler.delete_file("cookies/morbius")
            for file in filenames:
                file_handler.delete_file(file)
        # yt links usually
        else:
            message = await ctx.send("Downloading...")
            coms = ["yt-dlp", "-f", "b", "--no-warnings", link]
            coms2 = ["yt-dlp", "-f", "b", "--get-filename", "--no-warnings", link]
            print(shjoin(coms))
            print(shjoin(coms2))
            proc = await asyncio.create_subprocess_exec(  # reads stdout live
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
                print(line.decode("utf-8"))
                self.pbar_list.append(line.decode("utf-8"))
                asyncio.ensure_future(self.updatebar(message))
                await asyncio.sleep(1)
            if proc.returncode != 0:
                response = await proc.stdout.read()
                response = response.decode("utf-8")
                await message.edit(content=response)
                await ctx.send("epic fail <a:trollplane:934777423881445436>")
                return
            await message.edit(content="Almost there...")
            out2, stdout, stderr = await subprocess_runner.run_subprocess(coms2)
            try:
                filename = stdout.decode("utf-8").split("\n")[0]
                await file_handler.send_file(ctx, message, filename)
            except Exception as e:
                await ctx.send(e)

            await message.delete()


def setup(client):
    client.add_cog(Download(client))
