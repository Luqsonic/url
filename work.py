import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import json
import math
import os
import shutil
import subprocess
import time
from aiohttp import web
# the secret configuration specific things

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

#function
import sys
sys.path.insert(1,'./')
from bot import ddl_call_back

from pyrogram import Client

bot = Client(
    session_name= 'Web Streamer',
    api_id=7392881,
    api_hash="8c6390da22f0b6a34ee95ab5bf4ddd9f",
    bot_token="1412992512:AAHb8GUexB17g_v9O990SLRWM4OPf64QhnU"
)

bot.run()


#routes = web.RouteTableDef()
def decode(text):
	c = text.replace("%&)",".")
	c = c.replace("%()(?",":")
	c = c.replace("@+%","/")
	return c


#@routes.get("/{link}")

if __name__ == '__main__':
	while True:
		async def button():
	 	   bot.send_message(chat_id=-559454773,text="boom")
	 	   url = "https://bboxlinks.herokuapp.com/709/VID-20211103-WA0024.mp4"
	 	   #await ddl_call_back(bot, url)
		

