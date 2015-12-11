# BeamBot Repository

This is my repository for my PyBot project, a Beam.pro chat bot.

## Setup

Python 3 is required. I develop using Python 3.4 on Ubuntu 14.04/Ubuntu 15.04, other distros and OSes have not been tested.

### Required Modules:

- `websockets`: Easily installable from `pip` with `pip3 install websockets`.
- `asyncio`: Only required if Python 3 version is older than 3.4. Easily installable from `pip` with `pip3 install asyncio`.

### Bot Setup

Once the proper modules are installed, run the `setup.py` script with `python3 setup.py`.

- To use autoconnect, input either the ID retrieved from `https://beam.pro/api/v1/channels/INSERT_BEAM_STREAM_OWNER_NAME_HERE` or the desired channel's name to the channel ID prompt.

 **Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,...}`. Use the **`"id"`** specified (in this case, **20902**).

### Running:

Simply run `beambot.py` with Python 3! (`python3 beambot.py`)

## Features in 3.3.3

##### **(3.3.0)** - Mucho Beuno, Mucho Grande release 3.3.0! \o/

##### **(3.3.1)** - Fixed bug in currency code where automatic currency wasn't given out unless you were already in the DB

##### **(3.3.1)** - Cleaned up/improved the currency code

##### **(3.3.2)** - Removed any mentions of announcing follows

##### **(3.3.2)** - Added option to set custom currency command

##### **(3.3.2b)** - Fixed a bug where just ! as a message would crash the bot

##### **(3.3.2b)** - Fixed a bug where bot would crash when running currency commands within the command timeout

##### **(3.3.3)** - Fixed TypeError NoneType bug that would crash the bot

**(3.3.3a)** - Maybe fixed TypeError NoneType bug? Nobody knows.

### Recognitions
- BreachX3 & 2Cubed & dminer78: For hanging out with me on the many, many streams that it took to get this bot in working order & always being happy to help & being super supportive
- xcentrik4: Allowing me to deploy PyBot on his streams & for putting up with my programming mutterings & random bot crashes
- alfw: Finding the fairly major bug in the !give command

### Current Issues:

- Need more commands and features. The never-ending task!

- Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

- Add ability to change default command responses (^)

- Anything else I can't think of at this time but is still applicable
