import asyncio
import json
import logging
import websockets

import send_events as se


LOCALHOST = "ws://localhost"


class Plugin:
    """Plugin object to register Stream Deck plugin and call actions."""

    def __init__(
            self, port, pluginUUID, registerEvent, info, loop,
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

    def __del__(self):
        """Cleanup websocket connections and async loop when plugin is deleted."""
        try:
            self.websocket.close()
            self.loop.close()
        except Exception as err:
            logging.critical(err)

    async def set_title(self, *args, **kwargs):
        """Set the button title in the Stream Deck App and/or Device."""
        payload = se.create_set_title_payload(*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def set_image(self, *args, **kwargs):
        """Set the button image in the Stream Deck App and/or Device."""
        payload = se.create_set_image_payload(*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def show_alert(self, *args, **kwargs):
        """Show an alert on the Stream Deck Device and Software."""
        payload = se.create_show_alert_payload(*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def show_ok(self, *args, **kwargs):
        """Show an 'ok' checkmark symbol in the Stream Deck App and/or Device."""
        payload = se.create_show_ok_payload(*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def set_state(self, *args, **kwargs):
        """Set the state of an action that supports multiple states."""
        payload = se.create_set_state_payload(*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def switch_to_profile(self, *args, **kwargs):
        """Switch to a Stream Deck profile."""
        """Switch to """
        payload = se.create_switch_to_profile_payload(*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def send_to_property_inspector(self, *args, **kwargs):
        """Send a payload to the property inspector"""
        payload = se.create_send_to_property_inspector_payload(
            *args, **kwargs
        )
        await self.send_message(json.dumps(payload))

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

    async def on_streamdeck_message(self):
        try:
            while True:
                message = await self.websocket.recv()
                logging.debug("StreamDeck Message Received")
                await self.process_data(json.loads(message))
        except websockets.exceptions.ConnectionClosedOK:
            logging.info("Stream Deck connection closed.")
            self.loop.stop()

    async def on_message(self):
        """Waits for message from Stream Deck to send for processing."""
        try:
            task = asyncio.create_task(self.on_streamdeck_message())
            await task
        except Exception as err:
            logging.critical(err)

    async def send_message(self, event):
        """Sends event object to Stream Deck.

        Args:
            event (str): Serialized json event object.
        """
        try:
            await self.websocket.send(event)
        except Exception as err:
            logging.critical(err)
            await self.show_alert()

    async def process_data(self, data):
        """Process data and perform actions.

        Args:
            data (dict): Data dictionary.
        """

        logging.info(f"Processing data: {data}")
