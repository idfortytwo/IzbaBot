import os
from dotenv import load_dotenv

from bot import bot


def main():
    load_dotenv()
    bot_token = os.environ.get('bot_token')
    bot.run(bot_token)


if __name__ == '__main__':
    main()