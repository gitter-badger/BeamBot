#BeamBot Repository

This is my repository for my beambot project, a Beam.pro chat bot. I need a better name than beambot or pybot, but those are what I'm working with currently.

##Setup

Python 3 is required. I develop using Python 3.4 on Ubuntu 14.04/Ubuntu 15.04, other distros and OSes have not been tested.

###Required libraries:

* `websockets`: You can install this via `sudo pip3 install websockets` on Ubuntu.
* If you are developing on anything less than Python 3.4, you will need to install the `asyncio` library. This can be done via `sudo pip3 install asyncio`.
* `BeautifulSoup4`: This can be installed via `sudo pip3 install beautifulsoup4`.
* `lxml`: This is required for the BeautifulSoup XML parsing and can be installed via `sudo pip3 install lxml`.

###Setting up the config.py file:

Once the proper libaries are installed, you need to edit the `data/config.py.template` file with your Beam.pro information.

* The `BEAM_ADDR` variable should not be touched. It will break everything if that is changed.
* The `USERNAME` and `PASSWORD` variables should be set to the Beam.pro username and password (respectively) for the account you wish the bot to chat using.
* The CHANNEL variable should be updated via the id number gathered by going to `https://beam.pro/api/v1/channels/INSERT_BEAM_STREAM_OWNER_NAME_HERE` and taking the id number. You then swap that number for the 1 in config file.

**Example**: Going to `https://beam.pro/api/v1/channels/ParadigmShift3d` returns `{"id":20902,"token":"ParadigmShift3d","online":false,`. You would want to take the `20902` (it will be different for another channel) number.

##Setting up the database
Simply rename the `data/beambot.sqlite-template` file to `data/beambot.sqlite`

###Running:

Simply run `python3 beambot.py`!

## Features in 1.0.0 - Full Release

It's a Release Candidate because it works in its basic form. However, it still could use improvement, so that's why it's not a full 1.0 release.

**(0.1.0)** - The bot will now announce his presence in chat with a cheery "top 'o the mornin'/evenin'/afternoon" depending on time of day.

**(0.1.0)** - The `!tackle` command now works, as do the `!slap!`, `!uptime`, `!hug`, `!ping` (was working, now updated - Thank you Kirby for the ping pong response >:D),  and `!whoami` commands.

**(0.1.0)** - Command responses are now handled by external module, `responses.py`.

**(0.1.1)** - Added better message filtering support for old messages

**(0.1.2)** - Added 30 second command timeout per user

**(0.1.2)** - Added gears and quote support

**(0.2.0)** - Added user whitelist that will remove command timeout and allow access to mod-only commands

**(0.2.0)** - Added the `!quote`, `!gears`, and `!give` commands.

**(0.2.1)** - Stopped bot from acting on any messages older than when it comes online.

**(0.2.1)** - pybot no longer not constantly pings the REST API + it's more responsive

**(0.2.1)** - Bot will check for existence of config files and creates them if they don't exist

**(0.2.2)** - Updated file structure so config files are now all stored in the `data` directory

**(0.2.3)** - You can now ban and un-ban users via the `!ban <user>` and `!unban <user>` commands respectively

**(0.3.0)** - Cleaned up code, removed unnecessary duplication

**(0.3.0)** - You can now create custom commands via `!command <commandname> <response>`. Also, append `+` to `!command` to make it a mod-only command, and append `-` to remove the command.

**(1.0.0)** - 1.0 release! \o/

**(1.0.0)** - Users in the stream automatically recieve +1 gear/trinket per minute and +3 every 3 minutes if they were involved in chat

###Current issues:

* Need to work on adding more commands and getting all existing commands in working order. Priority on getting existing commands working.

* Need a better name than pybot/beambot

* Need to give pybot/beambot a command line interface to issue commands from

* Add watching of IRC channel for commands

* Make `responses.py` use pickle/XML file to provide commands and responses

* Anything else I can't think of at this time but is still applicable