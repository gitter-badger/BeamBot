# BeamBot Repository

This is my repository for my PyBot project, a Beam.pro chat bot.

## Setup

Python 3 is required. I develop using Python 3.5 on Ubuntu 14.04/Ubuntu 15.04, other distros and OSes have not been tested.

### Required Modules:

- `autobahn`: Easily installable from `pip` with `pip3 install autobahn`.
- `pyOpenSSL` & `service_identity`: Installed via `sudo pip3 install service-identity` (this will install pyOpenSSL)
- `requests`: Installed via `sudo pip3 install requests`
- **Note**: You may run into an issue when installing `pyOpenSSL` where it crashes when installing the `cryptography` module. You should look [here](http://stackoverflow.com/questions/22073516/failed-to-install-python-cryptography-package-with-pip-and-setup-py) to see what to do.

### Bot Setup

Once the proper modules are installed, run the `setup.py` script with `python3 setup.py`.

- To use autoconnect, input either the ID retrieved from `https://beam.pro/api/v1/channels/INSERT_BEAM_STREAM_OWNER_NAME_HERE` or the desired channel's name to the channel ID prompt.

 **Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,...}`. Use the **`"id"`** specified (in this case, **20902**).

### Running:

Simply run `beambot_rewrite.py` with Python 3! (`python3 beambot_rewrite.py`)

## Features in 4.0.0.A

**(4.0.0.A)** - Changed to using Autobahn/Twisted instead of manual websockets & asyncio

### Recognitions
- BreachX3 & 2Cubed & dminer78: For hanging out with me on the many, many streams that it took to get this bot in working order & always being happy to help & being super supportive
- xcentrik4: Allowing me to deploy PyBot on his streams & for putting up with my programming mutterings & random bot crashes
- alfw: Finding the fairly major bug in the !give command

### Current Issues:

- Need more commands and features. The never-ending task!

- Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

- Add ability to change default command responses (^)

- Anything else I can't think of at this time but is still applicable
