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

* **NEW as of 3.2.6** - You can now just provide the stream owner's name. However, the numeric ID is still accepted.

**Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,`. You would want to take the `20902` (it will be different for another channel) number.

###Running:

Simply run `python3 beambot.py`!

## Features in 3.2.7

**NOTE**: With the 3.2.6 release, I removed the new features listed for all old versions up to version 3.2.2. They are still accessible in the repository history.

###### **(3.2.2)** - Fixed code where including @ symbol in user-referencing command would mess it up

###### **(3.2.2)** - General progress towards 3.3.0 (a stability & quality release)

###### **(3.2.3)** - General progress towards 3.3.0 (a stability & quality release)

###### **(3.2.3)** - Updated bot to use per-channel ban lists, custom command lists, & whitelists

###### **(3.2.3)** - Bot now will recognize the streamer/channel mods & will automatically act as if they are whitelisted (Fixes #5)

###### **(3.2.3)** - Bot now recognizes the streamer/channel owner separately from the stream mods. Not used currently, but definitely eventually.

###### **(3.2.4)** - Bot will now connect to & monitor beam.pro/pybot chat for bot control commands (!restart, !halt, !msg)

###### **(3.2.5)** - Bot now prints nicely formatted information about the messages, instead of raw JSON

######**(3.2.5)** - Removed extraneous message blacklisting code, since it is no longer needed since the bot uses websockets correctly.

###### **(3.2.5)** - Fixed bug where only the first custom command would actually work

###### **(3.2.5)** - Fixed bug where non-existent commands would elicit a blank message from the bot

###### **(3.2.6)** - Added auto_start.py to make the bot auto-launch if a channel goes live

###### **(3.2.6)** - Updated setup script to either take numeric ID or channel name

###### **(3.2.6)** - Updated bot to create lock file on startup and remove it on proper shutdown

**(3.2.7)** - Removed auto_start.py because it wasn't useful

**(3.2.7)** - Removed lock file because it's not needed anymore (no autostart)

**(3.2.7)** - Removed whitelist entirely, it was only in place because of me being lazy and not wanting to implement a simple feature

**(3.2.7)** - Yes, I just essentially undid the entire previous release. But there were broken things I had to fix and in the process of doing that I realized that those "features" were useless and annoying :P

### Info on future 3.3.0 release

The code has, as I've been adding to it, slowly been getting less tidy and well-written.

Plus, although I've tested the bot myself, I've yet to see it in action or have it truly tested by any other user than myself. (Thank you to @xcentrik4 on Twitter for letting me deploy my bot on his streams)

Thus, although I plan on adding a few new features and commands for 3.3.0, it's going to mainly be a boring (but very important) stability and quality improvement release.

**Plans for 3.3.0:**

* Update `return None` statements to return usage from `data/commandList.json` if `None` is being returned for anything other than command timeout.

* Clean up the codebase and stress-test/bug test the code with outside users, preferably in a production (live stream with active chat) environment.

* This release will fix bugs ~~#2~~ (Not going to change the bot name, at least not for 3.3.0), #3, ~~#5~~ (Fixed as of 3.2.3), ~~#6~~ (Fixed as of 3.2.3) and #7

###Current issues:

* Need to add more commands and features - The never-ending bug!

* Make bot watch beam.pro/pybot for commands (Groundworks laid as of 3.2.4)

* Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

* Add settings & ability to change default command responses (^)

* Add [[count]], [[currency]] custom response variable

* Fix bug in the response-monitoring code where it won't show emoticons as text in terminal output (micro bug, lines 203-204 in beambot.py)

* Anything else I can't think of at this time but is still applicable
