import os
import shutil
import time
import uuid

import aiohttp
import cv2
import disnake
import numpy as np

from myfunctions import subprocess_runner


class GreenScreener:
    def __init__(self, image, cap, out):
        # place custom init vars here
        self.image = image
        self.cap = cap
        self.out = out
        self.frame = 0

    async def start(self):
        done = False
        while not done:
            ret, img = self.cap.read()
            if not ret:
                done = True
                continue

            # i can't rember why i made it resize to the same size but i did
            # vergil = cv2.resize(img, res)
            vergil = img

            self.loop_extras()

            # adds vergil
            image = self.transparent_paste(self.image.copy(), vergil)

            # save
            self.out.write(image)
            self.frame += 1
        print(f"Reached {self.frame} frames")

    def loop_extras(self):
        pass

    def transparent_paste(self, bg, fg):
        bg = bg[:, :, :3]
        alpha_channel = fg[:, :, 3] / 255  # convert from 0-255 to 0.0-1.0
        overlay_colors = fg[:, :, :3]
        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
        h, w = fg.shape[:2]
        background_subsection = bg[0:h, 0:w]
        composite = (
            background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
        )
        bg[0:h, 0:w] = composite
        return bg


class GreenScreenerHandler:
    def __init__(
        self, ctx, link, base_dir, height, width, fps, final_filename, file_prefix
    ):
        self.ctx = ctx
        self.debug_mode = False
        self.log_str = ""
        self.start_time = time.time()
        self.link = link
        self.base_dir = base_dir
        self.final_filename = final_filename
        self.file_prefix = file_prefix
        # unique uuid
        self.random_uuid = uuid.uuid4()

        self.image = None
        self.mid_time = None

        self.cap = cv2.VideoCapture(
            f"{self.base_dir}{self.file_prefix}_%06d.png", cv2.CAP_IMAGES
        )

        # videowriter
        self.res = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        os.makedirs(f"{base_dir}{self.random_uuid}/", exist_ok=True)

        self.vid1 = f"{self.base_dir}{self.random_uuid}/{self.file_prefix}_1.mp4"

        self.out = cv2.VideoWriter(self.vid1, fourcc, fps, self.res)

    async def start(self):
        vergil_status = await self.ctx.send("Getting ready...")
        await self.generate_user_img()
        g_screener = GreenScreener(self.image, self.cap, self.out)
        self.log("Pre stuff")
        await g_screener.start()
        self.log("Green screening done", mid=True)

        self.cap.release()
        self.out.release()

        await vergil_status.edit(
            content="<:motivated1:991217157100818534><:motivated2:991217292761382912><:motivated3:991217345345368074>\nApproaching... (Sponsored by Vergil)"
        )

        final_filepath = await self.ffmpeg_stuff()

        await vergil_status.edit(
            content="", file=disnake.File(final_filepath, filename=self.final_filename)
        )
        self.log("Sent file", mid=True)
        self.log_str += f"Editing done in {time.time()-self.start_time:.2f} seconds\n"
        await self.ctx.send(self.log_str)
        shutil.rmtree(f"{self.base_dir}{self.random_uuid}/")

    async def ffmpeg_stuff(self):
        # vid1 - the greenscreen part
        # vid3 - combined 1 and audio
        vid1 = self.vid1
        vid1_h264 = f"{self.base_dir}{self.random_uuid}/{self.file_prefix}_1_h264.mp4"
        vergil_audio = f"{self.base_dir}{self.file_prefix}.m4a"
        vcodec = "h264"

        coms = [
            "ffmpeg",
            "-i",
            vid1,
            "-i",
            vergil_audio,
            "-vcodec",
            vcodec,
            "-preset",
            "veryfast",
            "-crf",
            "28",
            "-c:a",
            "copy",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            vid1_h264,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        self.log("Converted to H264", mid=True)

        return vid1_h264

    async def generate_user_img(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.link) as resp:
                byte_content = await resp.read()
        user_image = cv2.imdecode(np.array(bytearray(byte_content), dtype=np.uint8), -1)
        self.image = cv2.resize(user_image, self.res)

    def log(self, msg, mid=False):
        if self.debug_mode:
            if mid == False:
                self.log_str += f"{msg}:\t{time.time()-self.start_time:.2f}\n"
            else:
                self.log_str += f"{msg}:\t{time.time()-self.mid_time:.2f}\n"
        self.mid_time = time.time()
