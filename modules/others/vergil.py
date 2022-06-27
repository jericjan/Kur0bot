from disnake.ext import commands
import disnake
import cv2
import numpy as np
import uuid
import requests
import os
import asyncio
import subprocess
from shlex import join as shlexjoin
import shutil
class Vergil(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def vergil(self, ctx, link=None):    
        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
            if ctx.message.attachments:  # message has images
                print("is attachment")
                link = ctx.message.attachments[0].url
            elif ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                if msg.attachments:  # if replied has image
                    link = msg.attachments[0].url
                elif msg.embeds:  # if replied has link
                    link = msg.embeds[0].url

                # print("embmeds: {0}".format(msg.embeds))
                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # link= msg.attachments[0].url
                else:
                    await ctx.send("the message you replied to has no image, baka!")
                    return
            else:
                await ctx.send("you did something wrong. brug. try again.")
                return
            print(link)   
            
        # open up video
        vergil_status = await ctx.send("Getting motivated...")
        cap = cv2.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        url_response = requests.get(link)
        user_image = cv2.imdecode(np.array(bytearray(url_response.content), dtype=np.uint8), -1)

        # grab one frame
        _, frame = cap.read()
        h,w = frame.shape[:2]

        # videowriter 
        res = (w, h);
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        random_uuid = uuid.uuid4()
        os.makedirs(f'videos/vergil_greenscreen/{random_uuid}/', exist_ok=True)
        out = cv2.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4',fourcc, 30.0, res)

        # loop
        done = False
        while not done:
            # get frame
            ret, img =  cap.read()
            if not ret:
                done = True
                continue

            # resize
            vergil = cv2.resize(img, res)
            image = cv2.resize(user_image, res)            
            # extract alpha channel from foreground image as mask and make 3 channels
            image = image[:, :, :3]
            alpha_channel = vergil[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
            overlay_colors = vergil[:, :, :3]
            
            alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            
            h, w = vergil.shape[:2]
            background_subsection = image[0:h, 0:w]
            composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            image[0:h, 0:w] = composite
            # save
            out.write(image);
        # close caps
        cap.release();
        out.release();  
        await vergil_status.edit(content="Obtaining more power!")
        vid1 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4'
        vid1_h264 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4'
        vid1_ts = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.ts'
        vid2 = f'videos/vergil_greenscreen/vergil_after_full.mp4'
        vid2_ts = f'videos/vergil_greenscreen/vergil_after_full.ts'
        vid3 = f'videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4'
        vid4 = f'videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4'
        vergil_audio =  f'videos/vergil_greenscreen/vergil_full.m4a'
        coms = ["ffmpeg" ,"-i", vid1, "-vcodec", "h264", vid1_h264] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()            
        coms = ["ffmpeg" ,"-i", vid1_h264, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid1_ts] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()      
        print(stdout.decode('utf-8'))
        if not os.path.exists(vid2_ts):
            coms = ["ffmpeg" ,"-i", vid2, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", vid2_ts] 
            print(shlexjoin(coms))
            out = await asyncio.create_subprocess_exec(
                *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )        
            stdout, stderr = await out.communicate()      
            print(stdout.decode('utf-8'))           
        await vergil_status.edit(content="Becoming the reclaimer of my name...")    
        coms = ['ffmpeg', '-i', f'concat:{vid1_ts}|{vid2_ts}',"-c", "copy", "-bsf:a", "aac_adtstoasc", vid3]  
        # coms = ["ffmpeg" ,"-i", vid1_fixed, "-i", vid2, "-i", vergil_audio, \
                # "-filter_complex", "[0:v] [1:v] concat=n=2:v=1 [vv]", \
                # "-map", "[vv]", "-map", "2:a:0", vid3] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        print(stdout.decode('utf-8'))
        coms = ['ffmpeg', '-i', vid3,'-i',vergil_audio,"-c", "copy", "-map", "0:v:0", "-map", "1:a:0", vid4]  
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        print(stdout.decode('utf-8'))
        await vergil_status.edit(content="Approaching...")    
        await vergil_status.edit(content="",file=disnake.File(vid4, filename="vergil status.mp4"))
        shutil.rmtree(f'videos/vergil_greenscreen/{random_uuid}/')
        
    @commands.command()
    async def smallvergil(self, ctx, link=None):    
        if link == None:
            print(ctx.message.attachments)  # a list
            print(ctx.message.reference)
            if ctx.message.attachments:  # message has images
                print("is attachment")
                link = ctx.message.attachments[0].url
            elif ctx.message.reference is not None:  # message is replying
                print("is reply")
                id = ctx.message.reference.message_id
                msg = await ctx.channel.fetch_message(id)
                if msg.attachments:  # if replied has image
                    link = msg.attachments[0].url
                elif msg.embeds:  # if replied has link
                    link = msg.embeds[0].url

                # print("embmeds: {0}".format(msg.embeds))
                # if re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content):
                #   link = re.search(r'http.*\bpng\b|http.*\bjpg\b|http.*\bjpeg\b',msg.content)[0]
                # link= msg.attachments[0].url
                else:
                    await ctx.send("the message you replied to has no image, baka!")
            else:
                await ctx.send("you did something wrong. brug. try again.")
                return
            print(link)   
            
        # open up video
        cap = cv2.VideoCapture("videos/vergil_greenscreen/vergil_%06d.png",cv2.CAP_IMAGES)
        url_response = requests.get(link)
        user_image = cv2.imdecode(np.array(bytearray(url_response.content), dtype=np.uint8), -1)

        # grab one frame
        _, frame = cap.read()
        h,w = frame.shape[:2]

        # videowriter 
        res = (w, h);
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        random_uuid = uuid.uuid4()
        os.makedirs(f'videos/vergil_greenscreen/{random_uuid}/', exist_ok=True)
        out = cv2.VideoWriter(f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4',fourcc, 30.0, res)

        # loop
        done = False
        while not done:
            # get frame
            ret, img =  cap.read()
            if not ret:
                done = True
                continue

            # resize
            vergil = cv2.resize(img, res)
            image = cv2.resize(user_image, res)            
            # extract alpha channel from foreground image as mask and make 3 channels
            image = image[:, :, :3]
            alpha_channel = vergil[:, :, 3] / 255 # convert from 0-255 to 0.0-1.0
            overlay_colors = vergil[:, :, :3]
            
            alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
            
            h, w = vergil.shape[:2]
            background_subsection = image[0:h, 0:w]
            composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
            image[0:h, 0:w] = composite
            # save
            out.write(image);
        # close caps
        cap.release();
        out.release();  
        vid1 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.mp4'
        vid1_h264 = f'videos/vergil_greenscreen/{random_uuid}/vergil_1_h264.mp4'
        vid1_ts = f'videos/vergil_greenscreen/{random_uuid}/vergil_1.ts'
        vid2 = f'videos/vergil_greenscreen/vergil_after_full.mp4'
        vid2_ts = f'videos/vergil_greenscreen/vergil_after_full.ts'
        vid3 = f'videos/vergil_greenscreen/{random_uuid}/vergil_3.mp4'
        vid4 = f'videos/vergil_greenscreen/{random_uuid}/vergil_4.mp4'
        vergil_audio =  f'videos/vergil_greenscreen/vergil_full.m4a'
        coms = ["ffmpeg" ,"-i", vid1, "-vcodec", "h264", vid1_h264] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate()             
        coms = ["ffmpeg" ,"-i", vid1_h264, "-i", vid2, "-i", vergil_audio, \
                "-filter_complex", "[0:v] [1:v] concat=n=2:v=1 [vv]", \
                "-map", "[vv]", "-map", "2:a:0", vid3] 
        print(shlexjoin(coms))
        out = await asyncio.create_subprocess_exec(
            *coms, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )        
        stdout, stderr = await out.communicate() 
        print(stdout.decode('utf-8'))
        
        await ctx.send(file=disnake.File(vid3, filename="vergil status.mp4"))
        shutil.rmtree(f'videos/vergil_greenscreen/{random_uuid}/')

        
def setup(client):
    client.add_cog(Vergil(client))
