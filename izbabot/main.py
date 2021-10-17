import os
from dotenv import load_dotenv

from bot import bot
from utils import setup_logger


def main():
    logger = setup_logger('logger')
    logger.debug('starting bot')

    load_dotenv()
    bot_token = os.environ.get('bot_token')
    bot.run(bot_token)


if __name__ == '__main__':
    main()