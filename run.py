import logging
import os

from dotenv import load_dotenv

from ooerbot.bot import OoerBot


def main():
    load_dotenv()

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)8s: %(message)s\t(%(name)s)',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=os.getenv('LOG_LEVEL', 'INFO')
    )

    bot = OoerBot()
    bot.load_extensions()
    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
