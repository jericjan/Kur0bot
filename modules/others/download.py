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
# import codecs
limiter = AsyncLimiter(1, 1)


class Download(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pbar_list = []

    async def updatebar(self, msg):
        # print("Updating bar...")
        try:

            async with limiter:
                await msg.edit(content=self.pbar_list[-1])
                # print("\033[92m SUCCESS! \033[0m")
        except Exception as e:
            if str(e).startswith("404 Not Found"):
                pass
            else:
                # print(f"\033[91m timeout!\n{e} \033[0m")
                pass
            pass

    @commands.command()
    async def download(self, ctx, link):  # reddit, facebook, instagram, tiktok, yt

        if "reddit.com" in link or "v.redd.it" in link:
            cookiecoms = [
                "gpg",
                "--pinentry-mode=loopback",
                "--passphrase",
                os.getenv("ENCRYPTPASSPHRASE"),
                "cookies (17).txt.gpg",
            ]
            cookieproc = await asyncio.create_subprocess_exec(
                *cookiecoms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await cookieproc.communicate()
            message = await ctx.send("Downloading...")
            coms = [
                "yt-dlp",
                "-f",
                "bestvideo+bestaudio",
                "--cookies",
                "cookies (17).txt",
                "--no-warnings",
                link,
            ]

            print(shjoin(coms))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # stdout, stderr = await proc.communicate()
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
                self.pbar_list.append(line.decode("utf-8"))
                asyncio.ensure_future(self.updatebar(message))
                await asyncio.sleep(1)
                print(f"\033[32m{line.decode('utf-8')}\033[0m")
                # await ctx.send(line.decode('utf-8'))
            if proc.returncode != 0:
                success = False
                await ctx.send("return code is not 0. trying something else")
                coms = [
                    "yt-dlp",
                    "--no-warnings",
                    link,
                ]
                print(shjoin(coms))
                proc = await asyncio.create_subprocess_exec(
                    *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                # stdout, stderr = await proc.communicate()
                while proc.returncode is None:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    self.pbar_list.append(line.decode("utf-8"))
                    asyncio.ensure_future(self.updatebar(message))
                    await asyncio.sleep(1)
                    print(f"\033[32m[{line.decode('utf-8')}\033[0m")
                    linedec = line.decode('utf-8')
                    if re.search(r"Following redirect to ",linedec):
                        success = True
                        print("match!")
                        if re.search(r"https:\/\/www.reddit.com\/over18.+",linedec):
                            link = unquote(re.findall(r"https%3A%2F%2Fwww.reddit.com.+",linedec)[0])
                        else:
                            link = re.findall(r'https://.+',linedec)[0]
                        print(f"match is: {link}")    
                    # await ctx.send(line.decode('utf-8'))
                if proc.returncode != 0 and success == False:
                    await ctx.send("return code is not 0. i give up")
                    return
            print("almost there")
            await message.edit(content="Almost there...")            
            coms2 = [
                "yt-dlp",
                "--get-filename",
                "--cookies",
                "cookies (17).txt",
                "--no-warnings",
                link,
            ]            
            print(shjoin(coms2))
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            try:
                stdout, stderr = await out2.communicate()
                print(f"\033[32m{stdout.decode('utf-8')}\033[0m")
                filename = stdout.decode("utf-8").split("\n")[0]
                clean_name = filename.replace(",","")
                await message.edit(content="Sending video...")
                try:
                    if filename.endswith(".mp4"):
                        await ctx.send(file=disnake.File(filename,filename=clean_name))
                    else:
                        await ctx.send(file=disnake.File(filename,filename=f"{clean_name}.mp4"))
                except Exception as e:
                    await ctx.send(e)
                    await ctx.send(type(e).__name__)
            except disnake.HTTPException:
                await ctx.send(
                    "File too large, broski <:towashrug:853606191711649812>"
                )
            os.remove("cookies (17).txt")
            os.remove(filename)
            await message.delete()

        elif "facebook.com" in link:
            message = await ctx.send("Downloading...")
            # encypted with `gpg -c --pinentry-mode=loopback your-file.txt`
            cookiecoms = [
                "gpg",
                "--pinentry-mode=loopback",
                "--passphrase",
                os.getenv("ENCRYPTPASSPHRASE"),
                "cookies (15).txt.gpg",
            ]
            cookieproc = await asyncio.create_subprocess_exec(
                *cookiecoms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await cookieproc.communicate()
            # res = stdout.decode('UTF-8').split('\n')[2:]
            # fin = '\n'.join(res)
            # print(fin)
            # return_data = io.BytesIO()
            # return_data.write(fin.encode())
            # return_data.seek(0)
            coms = [
                "yt-dlp",
                "-f",
                "best",
                "--cookies",
                "cookies (15).txt",
                "--no-warnings",
                link,
            ]
            coms2 = [
                "yt-dlp",
                "-f",
                "best",
                "--get-filename",
                "--cookies",
                "cookies (15).txt",
                "--no-warnings",
                link,
            ]
            print(shjoin(coms))
            print(shjoin(coms2))
            proc = await asyncio.create_subprocess_exec(
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
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            try:
                stdout, stderr = await out2.communicate()
                filename = stdout.decode("utf-8").split("\n")[-2]
                clean_name = filename.replace(",","")
                print(stdout.decode("utf-8"))
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=disnake.File(filename,filename=clean_name))
                except Exception as e:
                    await ctx.send(e)
            except disnake.HTTPException:
                await ctx.send(
                    "File too large, broski <:towashrug:853606191711649812>"
                )
            except Exception as e:
                await message.edit(content=e)
            os.remove("cookies (15).txt")        
            os.remove(filename)

            await message.delete()
        elif "tiktok.com" in link:
            message = await ctx.send("Downloading...")
            coms = ["yt-dlp", "-f", "best", "--no-warnings", link]
            coms2 = [
                "yt-dlp",
                "-f",
                "best",
                "--get-filename",
                "--no-warnings",
                link,
            ]
            print(shjoin(coms))
            print(shjoin(coms2))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # stdout, stderr = await proc.communicate()
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
                self.pbar_list.append(line.decode("utf-8"))
                asyncio.ensure_future(self.updatebar(message))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            try:
                stdout, stderr = await out2.communicate()
                filename = stdout.decode("utf-8").split("\n")[0]
                clean_name = filename.replace(",","")
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=disnake.File(filename,filename=clean_name))
                except Exception as e:
                    await ctx.send(e)
            except disnake.HTTPException:
                await ctx.send(
                    "File too large, broski <:towashrug:853606191711649812>"
                )
            except Exception as e:
                await message.edit(content=e)
            os.remove(filename)
            await message.delete()
        elif "bilibili.com" in link:
            message = await ctx.send(
                "Bilibili? <:oka:944181217467723826>\n Let me do something different here. Give me a moment..."
            )
            coms = ["yt-dlp", "--get-url", "-j", "--no-warnings", link]

            print(shjoin(coms))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            stdout, stderr = await proc.communicate()
            url = stdout.splitlines()[0]
            json_str = stdout.splitlines()[1]
            json_dict = json.loads(json_str)
            bilibili_id = json_dict["webpage_url_basename"]
            filename = f"bilibili_{bilibili_id}.mp4"
            clean_name = filename.replace(",","")
            coms2 = ["ffmpeg", "-i", url, "-c", "copy", "-y", filename]
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="Downloading...")
            else:
                try:

                    await message.edit(content="Sending video...")
                    try:
                        await ctx.send(file=disnake.File(filename,filename=clean_name))
                    except Exception as e:
                        await ctx.send(e)
                except disnake.HTTPException:
                    await ctx.send(
                        "File too large, broski <:towashrug:853606191711649812>"
                    )
                except Exception as e:
                    await message.edit(content=e)
            os.remove(filename)
            await message.delete()
        # yt links usually
        else:
            message = await ctx.send("Downloading...")
            coms = ["yt-dlp", "-f", "best", "--no-warnings", link]
            coms2 = ["yt-dlp", "-f", "best", "--get-filename", "--no-warnings", link]
            print(shjoin(coms))
            print(shjoin(coms2))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # stdout, stderr = await proc.communicate()
            while proc.returncode is None:
                line = await proc.stdout.readline()
                if not line:
                    break
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
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            try:
                stdout, stderr = await out2.communicate()
                filename = stdout.decode("utf-8").split("\n")[0]
                clean_name = filename.replace(",","")
                await message.edit(content="Sending video...")
                try:
                    await ctx.send(file=disnake.File(filename,filename=clean_name))
                except Exception as e:
                    await ctx.send(e)
            except disnake.HTTPException:
                await ctx.send(
                    "File too large, broski <:towashrug:853606191711649812>"
                )
            except Exception as e:
                await message.edit(content=e)
            os.remove(filename)
            await message.delete()


def setup(client):
    client.add_cog(Download(client))
