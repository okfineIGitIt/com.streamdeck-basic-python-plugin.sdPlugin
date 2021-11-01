"""Base plugin to interact with Stream Deck App."""

import asyncio
import json
import logging
import websockets

import send_events as se


LOCALHOST = "ws://localhost"


class StreamDeckPluginBase:
    """Base plugin to interact with Stream Deck App."""

    def __init__(
            self, port, pluginUUID, registerEvent, info, loop,
    ):
        """Plugin object initializer.

        `port`, `pluginUUID`, `registerEvent`, and `info` come from the Stream Deck registration
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

        self.create_payload_functions = {
            "setSettings": se.create_set_settings_payload,
            "getSettings": se.create_get_settings_payload,
            "setGlobalSettings": se.create_set_global_settings_payload,
            "getGlobalSettings": se.create_get_global_settings_payload,
            "openUrl": se.create_open_url_payload,
            "logMessage": se.create_log_message_payload,
            "setTitle": se.create_set_title_payload,
            "setImage": se.create_set_image_payload,
            "showAlert": se.create_show_alert_payload,
            "showOk": se.create_show_ok_payload,
            "setState": se.create_switch_to_profile_payload,
            "switchToProfile": se.create_switch_to_profile_payload,
            "sendToPropertyInspector": se.create_send_to_property_inspector_payload,
        }

    def __del__(self):
        """Cleanup websocket connections and async loop when plugin is deleted."""
        try:
            self.websocket.close()
            self.loop.close()
        except Exception as err:
            logging.critical(err)

    async def send_event(self, event_name: str, *args, **kwargs):
        """Sends standard 'send event' to Plugin Manager.

        Args:
            event_name (str): Name of event to send.
            *args: Arguments to pass to payload creation function.
            **kwargs: Keyword arguments to pass to payload creation function:
        """
        if event_name not in self.create_payload_functions.keys():
            raise ValueError(f"No such send event: {event_name}")

        payload = self.create_payload_functions[event_name](*args, **kwargs)
        await self.send_message(json.dumps(payload))

    async def listen(self):
        """Listens to port provided by Stream Deck app and processes messages."""
        try:
            await self._init_websocket()
            await self._register_websocket()
            await self.start_listeners()
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
        except Exception as err:
            logging.critical(err)

    async def on_streamdeck_message(self):
        """Receive messages from Stream Deck and send data for processing."""
        try:
            while True:
                message = await self.websocket.recv()
                await self.process_streamdeck_data(json.loads(message))
        except websockets.exceptions.ConnectionClosedOK:
            logging.info("Stream Deck connection closed.")
            self.loop.stop()

    async def start_listeners(self):
        """Start listeners for Stream Deck."""
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

    async def process_streamdeck_data(self, data):
        """Process data from Stream Deck and perform actions.

        Args:
            data (dict): Data dictionary.
        """

        logging.info(f"Processing data: {data}")



