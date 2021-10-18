import os
from dotenv import load_dotenv

from bot import bot
from db.connection import create_schema
from logger import setup_app_logger
from quart import Quart


def main():
    logger = setup_app_logger()
    logger.info('starting bot')

    create_schema()

    app = Quart(__name__)

    @app.route('/')
    def hello():
        return 'Hello World!'

    bot.loop.create_task(app.run_task())

    load_dotenv()
    bot_token = os.environ.get('bot_token')
    bot.run(bot_token)


if __name__ == '__main__':
    main()