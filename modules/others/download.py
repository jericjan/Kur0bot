from discord.ext import commands
import discord
import asyncio
import os
from shlex import join as shjoin
import subprocess
import codecs


class Download(commands.Cog):
    # def __init__(self, client):
    #     self.client = client

    @commands.command()
    async def download(self, ctx, link):

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
                link,
            ]
            coms2 = [
                "yt-dlp",
                "--get-filename",
                "--cookies",
                "cookies (17).txt",
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
                line = await proc.stdout.read(100)
                if not line:
                    break
                await message.edit(content=line.decode("utf-8"))
                # await ctx.send(line.decode('utf-8'))
                await asyncio.sleep(1)
            if proc.returncode != 0:
                await ctx.send("return code is not 0. trying something else")
                coms = ["yt-dlp", "--cookies", "cookies (17).txt", link]
                print(shjoin(coms))
                proc = await asyncio.create_subprocess_exec(
                    *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                # stdout, stderr = await proc.communicate()
                while proc.returncode is None:
                    line = await proc.stdout.read(100)
                    if not line:
                        break
                    await message.edit(content=line.decode("utf-8"))
                    # await ctx.send(line.decode('utf-8'))
                    await asyncio.sleep(1)
                if proc.returncode != 0:
                    await ctx.send("return code is not 0. i give up")
                    return
            await message.edit(content="Almost there...")
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="A little more...")
            else:
                os.remove("cookies (17).txt")
                try:
                    thing = await out2.stdout.read()
                    filename = thing.decode("utf-8").split("\n")[0]
                    await message.edit(content="Sending video...")
                    try:
                        await ctx.send(file=discord.File(filename))
                    except Exception as e:
                        await ctx.send(e)
                        await ctx.send(type(e).__name__)
                except discord.HTTPException:
                    await ctx.send(
                        "File too large, broski <:towashrug:853606191711649812>"
                    )
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
            coms = ["yt-dlp", "-f", "best", "--cookies", "cookies (15).txt", link]
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
                line = await proc.stdout.read(100)
                if not line:
                    break
                await message.edit(content=line.decode("utf-8"))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="A little more...")
            else:
                os.remove("cookies (15).txt")
                try:
                    thing = await out2.stdout.read()
                    filename = thing.decode("utf-8").split("\n")[-2]
                    print(thing.decode("utf-8"))
                    await message.edit(content="Sending video...")
                    try:
                        await ctx.send(file=discord.File(filename))
                    except Exception as e:
                        await ctx.send(e)
                except discord.HTTPException:
                    await ctx.send(
                        "File too large, broski <:towashrug:853606191711649812>"
                    )
                except Exception as e:
                    await message.edit(content=e)
            os.remove(filename)

            await message.delete()

        elif "instagram.com" in link:
            message = await ctx.send("Downloading...")
            cookiecoms = [
                "gpg",
                "--pinentry-mode=loopback",
                "--passphrase",
                os.getenv("ENCRYPTPASSPHRASE"),
                "instacook.txt.gpg",
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
            coms = ["yt-dlp", "-f", "best", "--cookies", "instacook.txt", link]
            coms2 = [
                "yt-dlp",
                "-f",
                "best",
                "--get-filename",
                "--cookies",
                "instacook.txt",
                "--no-warnings",
                link,
            ]
            print(shjoin(coms))
            print(shjoin(coms2))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )

            while proc.returncode is None:
                line = await proc.stdout.read(100)
                if not line:
                    break
                await message.edit(content=line.decode("utf-8"))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="A little more...")
            else:
                os.remove("instacook.txt")
                try:
                    thing = await out2.stdout.read()
                    filename = thing.decode("utf-8").split("\n")[-2]
                    print(thing.decode("utf-8"))
                    await message.edit(content="Sending video...")
                    try:
                        await ctx.send(file=discord.File(filename))
                    except Exception as e:
                        await ctx.send(e)
                except discord.HTTPException:
                    await ctx.send(
                        "File too large, broski <:towashrug:853606191711649812>"
                    )
                except Exception as e:
                    await message.edit(content=e)
            os.remove(filename)

            await message.delete()

            # await ctx.send('I can\'t do Facebook links, unfortunately. It should work but idk why it don\'t')
        # tiktok
        elif "tiktok.com" in link:
            message = await ctx.send("Downloading...")
            coms = ["tiktok-yt-dlp/yt-dlp", "-f", "best", link]
            coms2 = [
                "tiktok-yt-dlp/yt-dlp",
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
                line = await proc.stdout.read(100)
                if not line:
                    break
                await message.edit(content=line.decode("utf-8"))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="A little more...")
            else:
                try:
                    thing = await out2.stdout.read()
                    filename = thing.decode("utf-8").split("\n")[0]
                    await message.edit(content="Sending video...")
                    try:
                        await ctx.send(file=discord.File(filename))
                    except Exception as e:
                        await ctx.send(e)
                except discord.HTTPException:
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
            coms = ["yt-dlp", "-f", "best", link]
            coms2 = ["yt-dlp", "-f", "best", "--get-filename", "--no-warnings", link]
            print(shjoin(coms))
            print(shjoin(coms2))
            proc = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            # stdout, stderr = await proc.communicate()
            while proc.returncode is None:
                line = await proc.stdout.read(100)
                if not line:
                    break
                await message.edit(content=line.decode("utf-8"))
                await asyncio.sleep(1)
            await message.edit(content="Almost there...")
            out2 = await asyncio.create_subprocess_exec(
                *coms2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while out2.returncode is None:
                await message.edit(content="A little more...")
            else:
                try:
                    thing = await out2.stdout.read()
                    filename = thing.decode("utf-8").split("\n")[0]
                    await message.edit(content="Sending video...")
                    try:
                        await ctx.send(file=discord.File(filename))
                    except Exception as e:
                        await ctx.send(e)
                except discord.HTTPException:
                    await ctx.send(
                        "File too large, broski <:towashrug:853606191711649812>"
                    )
                except Exception as e:
                    await message.edit(content=e)
            os.remove(filename)
            await message.delete()


def setup(client):
    client.add_cog(Download(client))
