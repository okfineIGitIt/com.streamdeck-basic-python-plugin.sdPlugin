```
Note: There are ways to tweak this configuration if you know what you are doing. This instructions are intended
to be the most direct path to get python up and running on your machine.
```

# Pre-requisites

1. Elgato Stream Deck (tested with Elgato Stream Deck V1, but should work with any model).
2. Stream Deck Software (https://www.elgato.com/en/downloads).
3. Stream Deck DistributionTool (https://developer.elgato.com/documentation/stream-deck/sdk/exporting-your-plugin/).
4. Windows 10 system (have not needed to distribute on Linux/Mac yet).
5. Python (https://realpython.com/installing-python/#how-to-install-from-the-full-installer).

    You will need to have at least python-3.8 installed on your system.

    **Make sure that python is in your system path.**

# Environment Setup

## 1. Create a virtual environment with `venv`

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
