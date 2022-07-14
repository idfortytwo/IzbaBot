import os
import asyncio

from dotenv import load_dotenv

from bot import bot
from db.connection import create_schema
from logger import setup_app_logger
from quart import Quart


def main():
    logger = setup_app_logger()
    logger.info('starting bot')

    loop = asyncio.get_event_loop()
    task = loop.create_task(create_schema())
    loop.run_until_complete(task)

    app = Quart(__name__)

    @app.route('/')
    def hello():
        return 'up and running'

    port = os.environ.get('PORT', 5000)
    bot.loop.create_task(app.run_task(host='0.0.0.0', port=port))

    load_dotenv()
    bot_token = os.environ.get('bot_token')
    bot.run(bot_token)


if __name__ == '__main__':
    main()