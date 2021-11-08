import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import aiohttp
import json
import math
import os
import shutil
import time
from datetime import datetime

# the secret configuration specific things

# the Strings used for this "thing"

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import sys
sys.path.insert(1,'./')
from display_progress import progress_for_pyrogram,humanbytes,TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image


async def ddl_call_back(bot,link):
    logger.info(link)
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # youtube_dl exteactors
    tg_send_type = "file"
    youtube_dl_format =""
    youtube_dl_ext = "mp4"
    thumb_image_path = DOWNLOAD_LOCATION + \
        "/" + str(680601089) + ".jpg"
    youtube_dl_url = link
    custom_file_name = os.path.basename(youtube_dl_url)
    description = " "
    start = datetime.now()
    k = await bot.send_message(
        text="Starting Download",
        chat_id=-559454773
    )
    tmp_directory_for_each_user = DOWNLOAD_LOCATION + "/" + str(680601089)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                bot,
                session,
                youtube_dl_url,
                download_directory,
                -559454773,
                k.message_id,
                c_time
            )
        except asyncio.TimeoutError:
            await bot.edit_message_text(
                text="Slow url",
                chat_id=-559454773,
                message_id=k.message_id
            )
            return False
    if os.path.exists(download_directory):
        end_one = datetime.now()
        await bot.edit_message_text(
            text="Starting Upload",
            chat_id=-559454773,
            message_id=k.messagw_id
        )
        file_size = 2097152000 + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_directory).st_size
        if file_size > 2097152000:
            await bot.edit_message_text(
                chat_id=-559454773,
                text="Exceeded API Limit",
                message_id=k.message_id
            )
        else:
            # get the correct width, height, and duration for videos greater than 10MB
            # ref: message from @BotSupport
            width = 0
            height = 0
            duration = 0
            if tg_send_type != "file":
                metadata = extractMetadata(createParser(download_directory))
                if metadata is not None:
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
            # get the correct width, height, and duration for videos greater than 10MB
            if os.path.exists(thumb_image_path):
                width = 0
                height = 0
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                if tg_send_type == "vm":
                    height = width
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                Image.open(thumb_image_path).convert(
                    "RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                if tg_send_type == "file":
                    img.resize((320, height))
                else:
                    img.resize((90, height))
                img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            else:
                thumb_image_path = None
            start_time = time.time()
            # try to upload file
            if tg_send_type == "audio":
                await bot.send_audio(
                    chat_id=-559454773,
                    audio=download_directory,
                    caption=description,
                    duration=duration,
                    # performer=response_json["uploader"],
                    # title=response_json["title"],
                    # reply_markup=reply_markup,
                    thumb=thumb_image_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "Started Upload...",
                        k,
                        start_time
                    )
                )
            elif tg_send_type == "file":
                await bot.send_document(
                    chat_id=-559454773,
                    document=download_directory,
                    thumb=thumb_image_path,
                    caption=description,
                    # reply_markup=reply_markup,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "Starting Upload...",
                        k,
                        start_time
                    )
                )
            elif tg_send_type == "vm":
                await bot.send_video_note(
                    chat_id=-559454773,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumb_image_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "Starting Upload...",
                        k,
                        start_time
                    )
                )
            elif tg_send_type == "video":
                await bot.send_video(
                    chat_id=-559454773,
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    # reply_markup=reply_markup,
                    thumb=thumb_image_path,
                    #reply_to_message_id=update
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "Starting Upload...",
                        k,
                        start_time
                    )
                )
            else:
                logger.info("Did this happen? :\\")
            end_two = datetime.now()
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except:
                pass
            """
            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await bot.edit_message_text(
                text="n",
                chat_id=-559454773,
                message_id=mess_id,
                disable_web_page_preview=True
            )"""
            await bot.delete_messages(
        		chat_id=-559454773,
        		message_ids=k.message_id,
        		revoke=True
        	)
    else:
        await bot.send_message(
            text="Incorrect Link",
            chat_id=-559454773,
            disable_web_page_preview=True
        )


async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=3600) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await bot.edit_message_text(
            chat_id,
            message_id,
            text="""Initiating Download
URL: {}
File Size: {}""".format(os.path.basename(url), humanbytes(total_length))
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(128)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += 128
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
URL: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(
    os.path.basename(url),
    humanbytes(total_length),
    humanbytes(downloaded),
    TimeFormatter(time_to_completion)
)
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()