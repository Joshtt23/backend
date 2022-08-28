#handles api and call bot start 
import asyncio
from tf_backend.discord_bot.bot import bot
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from tf_backend.api.frontend_api import app
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tf_backend.holders.WalletInfo import HolderChecker

config = Config()
config.bind=["0.0.0.0:8888"]
config.certfile = "./tf_backend/api/certs/MyCert.crt"
config.keyfile = "./tf_backend/api/certs/MyKey.key"


async def busyloop():
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(HolderChecker, 'interval', minutes=10)
    scheduler.start()
    loop = asyncio.get_event_loop()
    loop.create_task(serve(app, config, 
    shutdown_trigger=busyloop
    ))
    bot.run()
    
