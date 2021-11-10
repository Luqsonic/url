from pyrogram import Client, filters
import asyncio

BOT_TOKEN = '1412992512:AAHb8GUexB17g_v9O990SLRWM4OPf64QhnU'
API_ID = 7392881
API_HASH = "8c6390da22f0b6a34ee95ab5bf4ddd9f"


if __name__ == "__main__":
    Bot = Client(
    "Simple-Pyrogram-Bot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)
    #Bot.run()

    async def boom():
    	print("car")
    	#await Bot.start()
    	await Bot.send_message(
    	chat_id=-559454773,
        text="https://uploadbot2.cf/dl/1042866842/www.1TamilMV.vip_Bigg_Boss_Tamil_S05_EP36_DAY_35_UNSEEN_720p_AVC_UNTOUCHED_AAC_682MB.mp4"
    )
    asyncio.run(Bot.run())
    asyncio.run(boom())
