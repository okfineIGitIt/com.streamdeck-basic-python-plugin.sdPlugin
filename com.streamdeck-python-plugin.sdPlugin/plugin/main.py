import asyncio
import logging
from logging.handlers import RotatingFileHandler
import sys

from plugin_core import Plugin
import utils


logging.basicConfig(
    handlers=[RotatingFileHandler('debug.log', maxBytes=100000, backupCount=10)],
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S'
)


def main():
    loop = None

    try:
        loop = asyncio.get_event_loop()
        args = utils.parse_args(sys.argv)

        plugin = Plugin(
            port=args['port'],
            pluginUUID=args['pluginUUID'],
            registerEvent=args['registerEvent'],
            info=args['info'],
            loop=loop,
        )

        loop.run_until_complete(
            asyncio.gather(plugin.listen())
        )

        loop.run_forever()
        loop.stop()
        loop.close()
    except Exception as err:
        logging.critical(err)
        loop.stop()
        loop.close()


if __name__ == '__main__':
    main()
    logging.shutdown()  # Need this to properly disconnect from log file

    for task in asyncio.all_tasks():
        task.cancel()

    sys.exit()
