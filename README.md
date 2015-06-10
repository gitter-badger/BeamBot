#BeamBot Repository

This is my repository for my beambot project, a Beam.pro chat bot. I need a better name than beambot or pybot, but those are what I'm working with currently.

##Setup

Python 3 is required. I develop using Python 3.4 on Ubuntu 14.04/Ubuntu 15.04, other distros and OSes have not been tested.

###Required libraries:

* `websockets`: You can install this via `sudo pip3 install websockets` on Ubuntu.
* If you are developing on anything less than Python 3.4, you will need to install the `asyncio` library. This can be done via `sudo pip3 install asyncio`.

###Setting up the config.py file:

Once the proper libaries are installed, you need to edit the `config.py.template` file with your Beam.pro information.

* The BEAM_ADDR variable should not be touched. It will break everything if that is changed.
* The USERNAME and PASSWORD variables should be set to the Beam.pro username and password (respectively) for the account you wish the bot to chat using.
* The CHANNEL variable should be updated via the id number gathered by going to `https://beam.pro/api/v1/channels/INSERT_BEAM_STREAM_OWNER_NAME_HERE` and taking the id number. You then swap that number for the 1 in config file.

**Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,`. You would want to take the 20902 (it will be different for another channel) number.

###Running:

Simply run `python3 beambot.py`!
