import base64
from pathlib import Path
import sys
import logging
import re


SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg"]


def get_image_as_base64_string(image_path):
    """Convert image to a base64 string

    Args:
        image_path (str): Path to image.

    Returns:
        str:
    """
    b64_prefix = ""
    image_path = Path(image_path)

    if not image_path.is_file:
        raise ValueError(f"Path is not a file: {image_path}")

    extension = image_path.suffix.lower()

    if extension not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(f"Image extension not supported: {extension}")

    if extension == ".png":
        b64_prefix = "data:image/png;base64,"
    if extension == ".jpg":
        b64_prefix = "data:image/jpg;base64,"

    with open(image_path, "rb") as img_file:
        image_string = base64.b64encode(img_file.read()).decode('utf-8')

    image_string = b64_prefix + image_string

    return image_string


def parse_args(sys_args):
    """Parse arguments passed by Stream Deck app.

    Args:
        sys_args ([str]): Argument string passed by Stream Deck.

    Returns:
        dict: Dictionary of arguments.
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
