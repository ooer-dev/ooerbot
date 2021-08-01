import logging

from config import LOG_LEVEL, TOKEN
from ooerbot.bot import OoerBot


def main():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)8s: %(message)s\t(%(name)s)',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=LOG_LEVEL
    )

    bot = OoerBot()
    bot.load_extensions()
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
