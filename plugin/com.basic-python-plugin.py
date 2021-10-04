import asyncio
import json
import logging
from logging.handlers import RotatingFileHandler
import re
import sys
import websockets

LOCALHOST = "ws://localhost"


logging.basicConfig(
    handlers=[RotatingFileHandler('debug.log', maxBytes=100000, backupCount=10)],
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S'
)

class Plugin:
    """Plugin object to register Stream Deck plugin and call actions."""

    def __init__(
        self, 
        port, 
        pluginUUID, 
        registerEvent, 
        info, 
        loop,
    ):
        """Plugin object initializer.

        `port`, `pluginUUID`, `registerEvent`, and `info` come from the Stream Deck Registration
        process.

        Args:
            port (int): Port to connect plugin to.
            pluginUUID (str): UUID for plugin provided by the Stream Deck.
            registerEvent (str): Register event flag.
            info (dict): Information from Stream Deck about context.
            loop (asyncio.ProactorEventLoop): Async event loop object.
        """
        self.port = port
        self.pluginUUID = pluginUUID
        self.registerEvent = registerEvent
        self.info = info
        self.loop = loop
        
        self.sd_context = None  # context ID provided by Stream Deck once connected

        self.state = 0  # Just here for testing purposes as of now

    def __del__(self):
        try:
            self.websocket.close()
            self.loop.close()
        except Exception as err:
            logging.critical(err)

    async def listen(self):
        """listens to port provided by Stream Deck app and processes messages."""
        try:
            await self._init_websocket()
            await self._register_websocket()
            await self.on_message()
        except Exception as err:
            logging.critical(err)

    async def _init_websocket(self):
        """Sets up connection to port provided by Stream Deck app."""
        uri = f"{LOCALHOST}:{self.port}"
        try:
            self.websocket = await websockets.client.connect(uri)
            return
        except Exception as err:
            logging.critical(err)

    async def _register_websocket(self):
        """Registers plugin with Stream Deck.
        
        Uses `registerEvent` and pluginUUID` provided by the Stream Deck.
        """
        try:
            data = {
                "event": self.registerEvent,
                "uuid": self.pluginUUID
            }

            logging.info("Registering websocket...")
            await self.websocket.send(json.dumps(data))
            return
        except Exception as err:
            logging.critical(err)

    async def on_message(self):
        """Waits for message from Stream Deck to send for processing."""
        try:
            async for message in self.websocket:
                self.process_data(json.loads(message))
        except Exception as err:
            logging.critical(err)

    async def send_message(self, event):
        """Sends event object to Stream Deck.

        Args:
            event (str): Serialized json event object.
        """
        try:
            logging.info(f"Sending event: {event}")
            await self.websocket.send(event)
        except Exception as err:
            logging.critical(err)

    def process_data(self, data):
        """Process data and perform actions.

        Args:
            data (dict): Data dictionary.
        """

        logging.info(f"Processing data: {data}")
        self.state = self.state + 1
        logging.info(f"Testing state: {self.state}")
        
        try:
            if "payload" in data:
                if self.sd_context is None:
                    self.sd_context = data["context"]
        except Exception as err:
            logging.critical(err)


def parse_args(sys_args):
    """Parse arguments passed by Stream Deck app.
    
    Args:
        sys_args (str): Argument string passed by Stream Deck.
    """
    args_length = len(sys_args)
    args = {}
    if args_length > 1:
        try:
            reg = re.compile('-(.*)')
            for i in range(1, args_length, 2):
                flag_index = i
                value_index = i + 1
                flag = reg.search(sys.argv[flag_index]).group(1)
                value = sys.argv[value_index]
                args[flag] = value
                logging.info(f"Flag: {flag}, Value: {value}, Type: {type(value)}")
        except Exception as err:
            logging.critical(err)
    return args

def main():
    try:
        args = parse_args(sys.argv)
        loop = asyncio.get_event_loop()

        plugin = Plugin(
            port=args['port'], 
            pluginUUID=args['pluginUUID'],
            registerEvent=args['registerEvent'], 
            info=args['info'], 
            loop=loop,
        )

        loop.run_until_complete(
            asyncio.gather(
                plugin.listen()
            )
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
