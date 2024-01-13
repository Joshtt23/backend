import threading
import asyncio
from tf_backend.discord_bot.bot import bot
from hypercorn.config import Config
from hypercorn.asyncio import serve
from tf_backend.api.frontend_api import app
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tf_backend.holders.WalletInfo import HolderChecker

def run_bot():
    bot.run()  # This is a blocking call

async def start_server():
    config = Config()
    config.bind = ["0.0.0.0:8888"]
    config.certfile = "./tf_backend/api/certs/ssl-bundle.crt"
    config.keyfile = "./tf_backend/api/certs/MyKey.pem"
    await serve(app, config)

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(HolderChecker, 'interval', minutes=5)
    scheduler.start()

    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Run the asyncio event loop for the server in the main thread
    asyncio.run(start_server())

    # bot_thread.join() is removed
