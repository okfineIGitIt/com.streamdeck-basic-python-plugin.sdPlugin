"""Stream Deck App `Send Event` payload creators.

Reference: https://developer.elgato.com/documentation/stream-deck/sdk/events-sent/
"""

from utils import get_image_as_base64_string


def create_set_settings_payload(context: str, payload):
    """Create and return "setSettings" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
        payload (dict): Dictionary with info to add to settings.
    Returns:
        dict: Dictionary with payload to save data for an instance's context.
    """
    return {
        "event": "setSettings",
        "context": context,
        "payload": payload
    }


def create_get_settings_payload(context: str):
    """Create and return "getSettings" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
    Returns:
        dict: Dictionary with payload to get save data for an instance's context.
    """
    return {
        "event": "setSettings",
        "context": context,
    }


def create_set_global_settings_payload(plugin_context: str, payload):
    """Create and return "setGlobalSettings" dictionary to send to the Plugin Manager.

    Args:
        plugin_context (str): An opaque value identifying the plugin/Property Inspector.
            Received during the plugin registration procedure.
        payload (dict): Dictionary with info to add to global settings.

    Returns:
        dict: Dictionary with payload to save data for plugin context.
    """
    return {
        "event": "setGlobalSettings",
        "context": plugin_context,
        "payload": payload
    }


def create_get_global_settings_payload(plugin_context: str):
    """Create and return "getGlobalSettings" dictionary to send to the Plugin Manager.

    Args:
        plugin_context (str): An opaque value identifying the plugin/Property Inspector.
            Received during the plugin registration procedure.

    Returns:
        dict: Dictionary with payload to get save data for plugin context.
    """
    return {
        "event": "getGlobalSettings",
        "context": plugin_context,
    }


def create_open_url_payload(url: str):
    """Create and return "openUrl" dictionary to send to the Plugin Manager.

    Args:
        url (str): Url to open in browser.
    Returns:
        dict: Dictionary with payload to open url in browser.
    """

    return {
        "event": "openUrl",
        "payload": {
            "url": url
        }
    }


def create_log_message_payload(message: str):
    """Create and return "logMessage" dictionary to send to the Plugin Manager.

    As per Stream Deck documentation:
    Logs are saved to disk per plugin in the folder `~/Library/Logs/StreamDeck/` on macOS and
    `%appdata%\\Elgato\\StreamDeck\\logs\\` on Windows. Note that the log files are rotated each
    time the Stream Deck application is relaunched.

    Args:
        message (str): Message to log in Stream Deck log files.

    Returns:
        dict: Dictionary with payload to get save message to Stream Deck log file.
    """
    return {
        "event": "logMessage",
        "payload": {
            "message": message
        }
    }


def create_set_image_payload(
    context: str, image_path: str = None, target: int = 0, state: int = None
):
    """Create and return "setImage" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
        image_path (str): Path to image. If not set, the default action image in the manifest.json is set.
        target (int): Defines whether the image is set on the hardware, the software, or both.
                Hardware and software - 0 (default)
                Only on the hardware - 1
                Only on the software - 2
        state (int): A 0-based integer value representing the state of an action with multiple states. 
            This is an optional parameter. If not specified, the title is set to all states.

    Returns:
        dict: Dictionary with payload to set an image.
    """

    payload = {
        "event": "setImage",
        "context": context,
        "payload": {
            "target": target,
        }
    }

    if image_path:
        image_b64_string = get_image_as_base64_string(image_path)
        payload["payload"]["image"] = image_b64_string

    if state is not None:
        payload["state"] = state

    return payload


def create_set_title_payload(
    context: str, title: str, target: int, state: int = None
):
    """Create and return "setTitle" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
        title (str): Title to display.
        target (int): Defines whether the image is set on the hardware, the software, or both.
                Hardware and software - 0 (default)
                Only on the hardware - 1
                Only on the software - 2
        state (int): A 0-based integer value representing the state of an action with multiple states. 
            This is an optional parameter. If not specified, the title is set to all states.

    Returns:
        dict: Dictionary with payload to set a title.
    """
    payload = {
        "event": "setTitle",
        "context": context,
        "payload": {
            "title": title,
            "target": target,
        }
    }

    if state is not None:
        payload["state"] = state

    return payload


def create_show_alert_payload(context: str):
    """Create and return "showAlert" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.

    Returns:
        dict: Dictionary with payload to show an alert in the button.
    """
    return {
        "event": "showAlert",
        "context": context,
    }


def create_show_ok_payload(context: str):
    """Create and return "showOk" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.

    Returns:
        dict: Dictionary with payload to show an ok symbol in the button.
    """

    return {
        "event": "showOk",
        "context": context,
    }


def create_set_state_payload(context: str, state: int):
    """Create and return "setState" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
        state (int): A 0-based integer value representing the state of an action with multiple states.

    Returns:
        dict: Dictionary with payload to set the plugin action state.
    """
    return {
        "event": "setState",
        "context": context,
        "payload": {
            "state": state
        }
    }


def create_switch_to_profile_payload(context: str, device: str, profile: str):
    """Create and return "switchToProfile" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
        device (str): Unique device identifier.
        profile (str): Profile name.

    Returns:
        dict: Dictionary with payload to switch to a different profile.
    """
    return {
        "event": "switchToProfile",
        "context": context,
        "device": device,
        "payload": {
            "profile": profile
        }
    }


def create_send_to_property_inspector_payload(context: str, action: str, payload: dict):
    """Create and return "sendToPropertyInspector" dictionary to send to the Plugin Manager.

    Args:
        context (str): An opaque value identifying the instance's action you want to modify.
        action (str): Action name.
        payload (dict): Extra arguments to send to propertyInspector.

    Returns:
        dict: Dictionary to send to the Property Inspector.
    """
    return {
        "action": action,
        "event": "sendToPropertyInspector",
        "context": context,
        "payload": payload
    }
