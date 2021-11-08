import sys
import glob
import asyncio
import logging
import importlib
import importlib
from aiohttp import web
import aiohttp
from pathlib import Path
from pathlib import Path
from pyrogram import idle
from os import getenv, environ
from dotenv import load_dotenv

from App.server import web_server
from App.keepalive import ping_server
from apscheduler.schedulers.background import BackgroundScheduler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)


loop = asyncio.get_event_loop()

_path = "WebStreamer/bot/plugins/*.py"
files = glob.glob(_path)

APP_NAME = 'route0'
ON_HEROKU = True
FQDN = APP_NAME+'.herokuapp.com'
URL = f"https://{FQDN}/"     
PORT = int(getenv('PORT',8080))

async def start_services():
    print('----------------------------- DONE -----------------------------')
    print('\n')
    print('--------------------------- Importing ---------------------------')
    if ON_HEROKU:
        print('------------------ Starting Keep Alive Service ------------------')
        print('\n')
        scheduler = BackgroundScheduler()
        scheduler.add_job(ping_server, "interval", seconds=1200)
        scheduler.start()
    print('-------------------- Initalizing Web Server --------------------')
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    print('----------------------------- DONE -----------------------------')
    print('\n')
    print('----------------------- Service Started -----------------------')
    print('                        bot =>> luqbot')
    print('                        server ip =>> {}'.format(bind_address))
    if ON_HEROKU:
        print('                        app running on =>> {}'.format(FQDN))
    print('---------------------------------------------------------------')
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopped -----------------------')