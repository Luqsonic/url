import logging
import aiohttp


APP_NAME = 'route0'
ON_HEROKU = True
FQDN = APP_NAME+'.herokuapp.com'
URL = f"https://{FQDN}/"     

async def ping_server():
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(URL) as resp:
                logging.info("Pinged server with response: {}".format(resp.status))
    except TimeoutError:
        logging.warning("Couldn't connect to the site URL..!")
