> Note: There are ways to tweak this configuration if you know what you are doing. This instructions are intended
to be the most direct path to get python up and running on your machine.

# Prerequisites

1. Elgato Stream Deck (tested with Elgato Stream Deck V1, but should work with any model).
2. Stream Deck Software (https://www.elgato.com/en/downloads).
3. Stream Deck DistributionTool (https://developer.elgato.com/documentation/stream-deck/sdk/exporting-your-plugin/).
4. Windows 10 system (have not needed to distribute on Linux/Mac yet).
5. Python (https://realpython.com/installing-python/#how-to-install-from-the-full-installer).

    You will need to have at least python-3.8 installed on your system.

    **Make sure that python is in your system path.**

# Environment Setup

Open a command line in the project folder.
Create a virtual environment with the following command:
```bash
~/com.streamdeck-basic-python-plugin.sdPlugin/> python -m venv .venv
```

Activate this new virtual environment:
```bash
~/com.streamdeck-basic-python-plugin.sdPlugin/> .venv\Scripts\activate.bat
```

Make sure `pip` is up-to-date:
```bash
~/com.streamdeck-basic-python-plugin.sdPlugin/> python -m pip install --upgrade pip
```

Install packages from requirements.txt file:
```bash
~/com.streamdeck-basic-python-plugin.sdPlugin/> pip install -r requirements.txt
```

# Creating a Stream Deck Plugin

Creating a Stream Deck python plugin consists of 4 steps.

## 1. Write the python code.

`com.basic-python-plugin.py` is where the Elgato Stream Deck runs code from.

The `Plugin().process_data()` function is where actions can be performed based on updates from the Stream Deck app:
```python
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
```

Based on the `data` from the app, different actions can be programmed.

## 2. Create an executable from the python code.

To create the executable `pyinstaller` will be used. Run the following command to create the executable:
```bash
~/com.streamdeck-basic-python-plugin.sdPlugin/> pyinstaller plugin/com.basic-python-plugin.py
```

This will create a `dist` and `build` folder in the `plugin` folder.

**The path to the executable will be `plugin/dist/com.basic-python-plugin.exe`.**

> Note: `pyinstaller` will find all imports and include them in the build. There are some external libraries where additional setup is needed, in which case some customization will be needed (https://pyinstaller.readthedocs.io/en/stable/operating-mode.html#analysis-finding-the-files-your-program-needs)

## 3. Set up `manifest.json` to point to the executable.

If no modifications are made to the image filenames and the executable path doesn't change, the `manifest.json` can be left as is.

Otherwise, this documentation from Elgato is a good reference for how to set up the json:
https://developer.elgato.com/documentation/stream-deck/sdk/manifest/

## 4. Package the plugin using the package distribution tool provided by Elgato.

Reference: https://developer.elgato.com/documentation/stream-deck/sdk/exporting-your-plugin/

Finally, to install the plugin in the Stream Deck app, Elgato has provided a distribution tool for both Mac and Windows.

**For the next step, open a shell in the parent directory of the plugin folder.**
**For example, if the plugin folder was C:/Desktop/com.streamdeck-basic-python-plugin.sdPlugin, then the shell would need to be running from C:/Desktop.**


Run this command from the command line:
```bash
~/> tools/DistributionTool.exe -b -i com.streamdeck-basic-python-plugin.sdPlugin -o Release
```

`com.streamdeck-basic-python-plugin.sdPlugin` is the *plugin folder* (**not** the python executable), and the value after `-o` is where to put the distribution file.

In the above case , you should find a `com.streamdeck-basic-python-plugin.streamDeckPlugin` file in `com.streamdeck-basic-python-plugin.sdPlugin/Release`.

Double clicking `com.streamdeck-basic-python-plugin.streamDeckPlugin` will install your plugin.

During development, if you make changes to the plugin code and rebuild it, you will need to uninstall the old plugin first before installing the updated plugin in the Stream Deck App.
MAKE SURE YOU ARE **NOT** ACCESSING THE APP PLUGIN FOLDER WHEN DOING THIS (`C:\Users\\(user)\AppData\Roaming\Elgato\StreamDeck\Plugins\\(plugin-name)` for Windows). The uninstall will not complete properly if so and you may have to restart your system, close the Stream Deck app, and delete the plugin folder manually from the App Plugin folder as an administrator.

![Uninstall Streamdeck Plugin](/docs/assets/uninstalling_streamdeck_plugin.png)


# Potential Error Messages

## `WARNING: lib not found: api-ms-win-core-path-l1-1-0.dll dependency of ...\python\python39\python39.dll`

Solutions:
- Uninstall and re-install python

    Do not have a good explanation for this fix other than that it worked for me. May be that the python paths were not set up properly.
