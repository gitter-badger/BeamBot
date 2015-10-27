# BeamBot Repository

This is my repository for my PyBot project, a Beam.pro chat bot.

## Setup

Python 3 is required. I develop using Python 3.4 on Ubuntu 14.04/Ubuntu 15.04, other distros and OSes have not been tested.

### Required libraries:

* `websockets`: You can install this via `sudo pip3 install websockets` on Ubuntu.
* If you are developing on anything less than Python 3.4, you will need to install the `asyncio` library. This can be done via `sudo pip3 install asyncio`.

### Setting up the bot

Once the proper libaries are installed, you need to run the `setup.py` script via `python3 setup.py`.

* If you want to autoconnect, the channel ID question can either be answered via getting the ID from  `https://beam.pro/api/v1/channels/INSERT_BEAM_STREAM_OWNER_NAME_HERE`, or by entering the channel's name.

 **Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,`. You would want to take the **20902** (it will be different for another channel) number.

### Running:

Simply run `python3 beambot.py`!

## Features in 3.3.0

**(3.3.0)** - Mucho Beuno, Mucho Grande release 3.3.0! \o/

**(3.3.0)** - Merged release 3.2.16 from 3.3.0 branch into master

**(3.3.0)** - Minor changes made during merge

**(3.3.0)** - Quick patches for the setup script and responses module
bugs in original 3.3.0 release

### Recognitions
* BreachX3 & 2Cubed & dminer78: For hanging out with me on the many, many streams that it took to get this bot in working order & always being happy to help & being super supportive
* xcentrik4: Allowing me to deploy PyBot on his streams & for putting up with my programming mutterings & random bot crashes
* alfw: Finding the fairly major bug in the !give command

### Current issues:

* Need to add more commands and features - The never-ending bug!

* Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

* Add ability to change default command responses (^)

* Anything else I can't think of at this time but is still applicable
