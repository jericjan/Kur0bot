import os
import shutil
import time
import uuid

import aiohttp
import cv2
import disnake
import numpy as np
from disnake.ext import commands

from myfunctions import msg_link_grabber, subprocess_runner


class Vergil(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def quickvergil(self, ctx, link=None):
        start_time = time.time()
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        # open up video
        vergil_status = await ctx.send("Getting motivated...")
        cap = cv2.VideoCapture(
            "videos/vergil_greenscreen/vergil_%06d.png", cv2.CAP_IMAGES
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                byte_content = await resp.read()
        user_image = cv2.imdecode(np.array(bytearray(byte_content), dtype=np.uint8), -1)

        # grab one frame
        _, frame = cap.read()
        h, w = frame.shape[:2]

        # videowriter
        res = (w, h)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        random_uuid = uuid.uuid4()
        os.makedirs(f"videos/vergil_greenscreen/{random_uuid}/", exist_ok=True)
        out = cv2.VideoWriter(
            f"videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4", fourcc, 30.0, res
        )

        # loop
        done = False
        while not done:
            # get frame
            ret, img = cap.read()
            if not ret:
                done = True
                continue

            # resize
            vergil = cv2.resize(img, res)
            image = cv2.resize(user_image, res)
            # extract alpha channel from foreground image as mask and make 3 channels
            image = image[:, :, :3]
            alpha_channel = vergil[:, :, 3] / 255  # convert from 0-255 to 0.0-1.0
            overlay_colors = vergil[:, :, :3]

            alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

            h, w = vergil.shape[:2]
            background_subsection = image[0:h, 0:w]
            composite = (
                background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            )
            image[0:h, 0:w] = composite
            # save
            out.write(image)
        # close caps
        cap.release()
        out.release()
        await vergil_status.edit(content="Obtaining more power!")
        vid1 = f"videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4"
        vid1_h264 = f"videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4"
        vid1_ts = f"videos/vergil_greenscreen/{random_uuid}/vergil_1.ts"
        vid2 = "videos/vergil_greenscreen/vergil_smol.mp4"
        vid2_ts = "videos/vergil_greenscreen/vergil_smol.ts"
        vid3 = f"videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4"
        vid4 = f"videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4"
        vid5 = f"videos/vergil_greenscreen/{random_uuid}/vergil_5.mp4"
        vergil_audio = "videos/vergil_greenscreen/vergil_full.m4a"
        coms = ["ffmpeg", "-i", vid1, "-vcodec", "h264", vid1_h264]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        coms = [
            "ffmpeg",
            "-i",
            vid1_h264,
            "-c",
            "copy",
            "-bsf:v",
            "h264_mp4toannexb",
            "-f",
            "mpegts",
            vid1_ts,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        if not os.path.exists(vid2_ts):
            coms = [
                "ffmpeg",
                "-i",
                vid2,
                "-c",
                "copy",
                "-bsf:v",
                "h264_mp4toannexb",
                "-f",
                "mpegts",
                vid2_ts,
            ]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await vergil_status.edit(content="Becoming the reclaimer of my name...")
        coms = [
            "ffmpeg",
            "-i",
            f"concat:{vid1_ts}|{vid2_ts}",
            "-c",
            "copy",
            "-bsf:a",
            "aac_adtstoasc",
            vid3,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        coms = [
            "ffmpeg",
            "-i",
            vid3,
            "-i",
            vergil_audio,
            "-c",
            "copy",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            vid4,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        coms = ["ffmpeg", "-i", vid4, "-c", "copy", vid5]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        await vergil_status.edit(content="Approaching...")
        await vergil_status.edit(
            content="", file=disnake.File(vid5, filename="vergil status.mp4")
        )
        end = time.time() - start_time
        await ctx.send(f"Vergil arrived in {end:.2f} seconds")
        shutil.rmtree(f"videos/vergil_greenscreen/{random_uuid}/")

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

    @commands.command()
    async def vergil(self, ctx, link=None):
        debug_mode = False
        start_time = time.time()
        link = await msg_link_grabber.grab_link(ctx, link)
        print(link)

        # unique uuid
        random_uuid = uuid.uuid4()

        # open up video
        vergil_status = await ctx.send("Getting motivated...")
        cap = cv2.VideoCapture(
            "videos/vergil_greenscreen/vergil_%06d.png", cv2.CAP_IMAGES
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                byte_content = await resp.json()
        user_image = cv2.imdecode(np.array(bytearray(byte_content), dtype=np.uint8), -1)

        # grab one frame
        _, frame = cap.read()
        h, w = frame.shape[:2]

        # videowriter
        res = (w, h)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        os.makedirs(f"videos/vergil_greenscreen/{random_uuid}/", exist_ok=True)
        out = cv2.VideoWriter(
            f"videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4", fourcc, 30.0, res
        )

        # resizes user's image and makes copy w/o filters
        image = cv2.resize(user_image, res)
        pre_filtered_image = image.copy()

        # add cut remnant+cracked effect
        remnant = cv2.imread(
            "videos/vergil_greenscreen/vergil_remnant.png", cv2.IMREAD_UNCHANGED
        )
        image = self.transparent_paste(image, remnant)

        # converts to RGBA and makes copy w/ filters
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        post_filtered_image = image.copy()
        log = ""
        if debug_mode:
            log += f"Pre stuff:\t{time.time()-start_time:.2f}\n"
        mid_time = time.time()

        # loop
        frame = 0
        done = False
        shift = 10
        saved_position = 0
        blue = 5
        while not done:
            ret, img = cap.read()
            if not ret:
                done = True
                continue

            # resize
            vergil = cv2.resize(img, res)

            if (
                frame < 16
            ):  # use img w/o filters before frame 17. it's 1 frame less for some reason
                image = pre_filtered_image.copy()
            else:  # use the image w/ filters after frame 17
                image = post_filtered_image.copy()
                # creating blue
                blue_img = np.full((480, 854, 4), (blue, 0, 0, 255), np.uint8)
                # eases in blue
                if blue < 50:
                    blue += 5
                # converts to RGBA
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                # adding blue to img
                image = cv2.add(image, blue_img)

                # The number of pixels
                num_rows, num_cols = image.shape[:2]

                # controls the movement of the slices
                saved_position = saved_position + shift
                shift -= 0.25

                # right side
                right_mask = cv2.imread(
                    "videos/vergil_greenscreen/imagecut_right.png", 0
                )
                right_cut = cv2.bitwise_and(image, image, mask=right_mask)
                # Creating a translation matrix
                translation_matrix = np.float32(
                    [[1, 0, saved_position], [0, 1, saved_position]]
                )
                # Image translation
                img_left = cv2.warpAffine(
                    right_cut, translation_matrix, (num_cols, num_rows)
                )

                # left side
                left_mask = cv2.imread("videos/vergil_greenscreen/imagecut_left.png", 0)
                left_cut = cv2.bitwise_and(image, image, mask=left_mask)
                # Creating a translation matrix
                translation_matrix = np.float32(
                    [[1, 0, -saved_position], [0, 1, -saved_position]]
                )
                # Image translation
                img_right = cv2.warpAffine(
                    left_cut, translation_matrix, (num_cols, num_rows)
                )

                # creates the background behind the slices. first tuple is size, second is color
                solid_background = np.full((480, 854, 4), (63, 57, 54, 255), np.uint8)

                # combines the two sliced images
                cuts = cv2.addWeighted(img_left, 1, img_right, 1, 0.0)

                # adding the background
                image = self.transparent_paste(solid_background, cuts)
            # adds vergil
            image = self.transparent_paste(image, vergil)

            # save
            out.write(image)
            frame += 1
        print(f"Reached {frame} frames")

        if debug_mode:
            log += f"Green screening done:\t{time.time()-mid_time:.2f}\n"
        mid_time = time.time()
        # close caps
        cap.release()
        out.release()
        await vergil_status.edit(
            content="<:motivated1:991217157100818534><:motivated2:991217292761382912><:motivated3:991217345345368074>\nApproaching..."
        )
        vid1 = f"videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4"
        vid1_h264 = f"videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4"
        vid1_ts = f"videos/vergil_greenscreen/{random_uuid}/vergil_1.ts"
        vid2 = "videos/vergil_greenscreen/vergil_smol.mp4"
        vid2_ts = "videos/vergil_greenscreen/vergil_smol.ts"
        vid3 = f"videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4"
        vid4 = f"videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4"
        vergil_audio = "videos/vergil_greenscreen/vergil_full.m4a"
        vcodec = "h264"

        coms = [
            "ffmpeg",
            "-i",
            vid1,
            "-vcodec",
            vcodec,
            "-preset",
            "veryfast",
            "-crf",
            "28",
            vid1_h264,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        if debug_mode:
            log += f"Converted to H264:\t{time.time()-mid_time:.2f}\n"
        mid_time = time.time()

        coms = [
            "ffmpeg",
            "-i",
            vid1_h264,
            "-c",
            "copy",
            "-bsf:v",
            "h264_mp4toannexb",
            "-f",
            "mpegts",
            vid1_ts,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        if debug_mode:
            log += f"Converted to MPEG-TS:\t{time.time()-mid_time:.2f}\n"
        mid_time = time.time()

        if not os.path.exists(vid2_ts):
            coms = [
                "ffmpeg",
                "-i",
                vid2,
                "-c",
                "copy",
                "-bsf:v",
                "h264_mp4toannexb",
                "-f",
                "mpegts",
                vid2_ts,
            ]
            out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
            log += (
                f"(2) Converted to MPEG-TS: {time.time()-mid_time:.2f} seconds passed\n"
            )
            mid_time = time.time()

        coms = [
            "ffmpeg",
            "-i",
            f"concat:{vid1_ts}|{vid2_ts}",
            "-c",
            "copy",
            "-bsf:a",
            "aac_adtstoasc",
            vid3,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        if debug_mode:
            log += f"Concatenatted vods:\t{time.time()-mid_time:.2f}\n"
        mid_time = time.time()

        coms = [
            "ffmpeg",
            "-i",
            vid3,
            "-i",
            vergil_audio,
            "-c",
            "copy",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            vid4,
        ]
        out, stdout, stderr = await subprocess_runner.run_subprocess(coms)
        if debug_mode:
            log += f"Added audio:\t{time.time()-mid_time:.2f}\n"
        mid_time = time.time()

        await vergil_status.edit(
            content="", file=disnake.File(vid4, filename="vergil status.mp4")
        )
        if debug_mode:
            log += f"Sent file:\t{time.time()-mid_time:.2f}\n"
        log += f"Vergil arrived in {time.time()-start_time:.2f} seconds\n"
        await ctx.send(log)
        shutil.rmtree(f"videos/vergil_greenscreen/{random_uuid}/")


def setup(client):
    client.add_cog(Vergil(client))
