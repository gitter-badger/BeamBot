#BeamBot Repository

This is my repository for my beambot project, a Beam.pro chat bot. I need a better name than beambot or pybot, but those are what I'm working with currently.

##Setup

Python 3 is required. I develop using Python 3.4 on Ubuntu 14.04/Ubuntu 15.04, other distros and OSes have not been tested.

###Required libraries:

* `websockets`: You can install this via `sudo pip3 install websockets` on Ubuntu.
* If you are developing on anything less than Python 3.4, you will need to install the `asyncio` library. This can be done via `sudo pip3 install asyncio`.

###Setting up the bot

Once the proper libaries are installed, you need to run the `setup.py` script via `python3 setup.py`.

* If you want to autoconnect, the channel prompt should be answered via the id number gathered by going to `https://beam.pro/api/v1/channels/INSERT_BEAM_STREAM_OWNER_NAME_HERE` and taking that id number.

**Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,`. You would want to take the `20902` (it will be different for another channel) number.

###Running:

Simply run `python3 beambot.py`!

## Features in 3.0.0

**NOTE**: With the 3.1.0 release, I removed the new features listed for all old versions up to version 1.0.0. They are still accessible in the repository history, but the list was getting long

###### **(1.0.0)** - 1.0 release! \o/

###### **(1.0.0)** - Users in the stream automatically recieve +1 gear/trinket per minute and +3 every 3 minutes if they were involved in chat

###### **(2.0.0)** - Jumping to 2.0.0 release really quickly because I made a major change to the way the code works. I moved the code that takes the raw command and converts it into a usable set of information, and the code that figures out which command exactly was sent into a separate file - `commands.py`.

###### **(2.0.0)** - Cleaned up the code a bit, and removed unnecessary code.

###### **(2.1.0)** - Added auto-connect/channel auto-selection via username

###### **(2.2.0)** - Fixed a configuration conflict with the IRC and beam information.

###### **(2.2.0)** - Changed gears to dimes

###### **(3.0.0)** - Changed custom command storage medium from XML to JSON because it's simpler

###### **(3.0.0)** - Changed custom commands so you can now update an existing command's response

###### **(3.0.0)** - Added !raid, !raided and !twitch commands

**(3.1.0)**	- Added `setup.py` setup script, so user no longer has to manually edit config.py

**(3.1.0)** - Removed `config.py` to replace it with `config.json`, since that is simpler and easier to maintain/easier for the user to set up initially.

**(3.1.0)** - Fixed a couple of random incorrect file names

**(3.1.0)** - Updated code to use new `config.json` data.

###Current issues:

* Need to add more commands and features

* Need a better name than pybot/beambot (Bug #2)

* Make bot watch beam.pro/pybot for commands

* Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

* Anything else I can't think of at this time but is still applicable
