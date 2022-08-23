#handles api and call bot start 
import asyncio
from tf_backend.discord_bot.bot import bot
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from tf_backend.api.frontend_api import app

config = Config()
config.bind=["0.0.0.0:8888"]

async def busyloop():
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    # asyncio.run(serve(app, Config()))
    loop = asyncio.get_event_loop()
    loop.create_task(serve(app, config, 
    shutdown_trigger=busyloop
    ))
    bot.run()
    
