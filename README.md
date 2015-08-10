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

## Features in 3.2.1

**NOTE**: With the 3.2.1 release, I removed the new features listed for all old versions up to version 3.0.0. They are still accessible in the repository history.

###### **(3.0.0)** - Changed custom command storage medium from XML to JSON because it's simpler

###### **(3.0.0)** - Changed custom commands so you can now update an existing command's response

###### **(3.0.0)** - Added !raid, !raided and !twitch commands

###### **(3.1.0)**	- Added `setup.py` setup script, so user no longer has to manually edit config.py

###### **(3.1.0)** - Removed `config.py` to replace it with `config.json`, since that is simpler and easier to maintain/easier for the user to set up initially.

###### **(3.1.0)** - Fixed a couple of random incorrect file names

###### **(3.1.0)** - Updated code to use new `config.json` data.

###### **(3.2.0)** - Added response variables `[[args]]` and `[[user]]`` for custom commands

###### **(3.2.0)** - `!give`, `!quote`, and `!gears` now can be called via ``@USERNAME`
###### OR plain `USERNAME` (no @ character)

###### **(3.2.0)** - Working on implementing `!commands` and `!throw`/`!catch`.

###### **(3.2.0)** - Working on transferring command responses to `data/responses.json`

###### **(3.2.0)** - Added `!currency` command, works exactly as `!dimes`

###### **(3.2.0)** - Updated `setup.py` script to set up `data/commandList.json`

###### **(3.2.1)** - Added `!blame` command to blame people!

###### **(3.2.1)** - Added `!commands` command to list available commands

###### **(3.2.1)** - Updated command timeout to include global timeout (3 times max per minute)

###### **(3.2.1)** - General progress towards 3.3.0 (a stability & quality release)

###### **(3.2.2)** - Fixed code where including @ symbol in user-referencing command would mess it up

###### **(3.2.2)** - General progress towards 3.3.0 (a stability & quality release)

**(3.2.3)** - General progress towards 3.3.0 (a stability & quality release)

**(3.2.3)** - Updated bot to use per-channel ban lists, custom command lists, & whitelists

**(3.2.3)** - Bot now will recognize the streamer/channel mods & will automatically act as if they are whitelisted (Fixes #5)

### Info on future 3.3.0 release

The code has, as I've been adding to it, slowly been getting less tidy and well-written.

Plus, although I've tested the bot myself, I've yet to see it in action or have it truly tested by any other user than myself.

Thus, although I plan on adding a few new features and commands for 3.3.0, it's going to mainly be a boring (but very important) stability and quality improvement release.

**Plans for 3.3.0:**

* Update `return None` statements to return usage from `data/commandList.json` if `None` is being returned for anything other than command timeout.

* Add `!throw` and `!catch` commands for functions

* Clean up the codebase and stress-test/bug test the heck out of the code with outside users, preferably in a production (live stream with active chat) environment.

* ~~Automatically whitelist channel mods and streamer as well as automatically detect streamer instead of using hard-coded "ParadigmShift3d".~~ (Fixed as of 3.2.3)

* This release will fix bugs #2, #3, ~~#5~~ (Fixed as of 3.2.3), #6 and #7

###Current issues:

* Need to add more commands and features - The never-ending bug!

* Need a better name than pybot/beambot (Bug #2)

* Make bot watch beam.pro/pybot for commands

* Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

* Add [[count]] custom response variable

* Anything else I can't think of at this time but is still applicable
