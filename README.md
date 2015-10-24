#BeamBot Repository

This is my repository for my PyBot project, a Beam.pro chat bot.

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

## Features in 3.2.14

**NOTE**: With the 3.2.14 release, I removed the new features listed for all old versions up to version 3.2.10. They are still accessible in the repository history.

###### **(3.2.10)** - Fixed bug where bot wasn't connecting to the correct API endpoint & thus wasn't authenticating, crashing the bot

###### **(3.2.10)** - You can now pass the -nsm/--nostartmsg argument when starting the bot to stop it from sending the startup greeting message

###### **(3.2.10)** - Added messages.py to handle message sending and websocket closing

###### **(3.2.10)** - Fixed bug where users sending /me messages would crash part of the bot

###### **(3.2.10)** - Added [[currency]] custom command variable, returns the running user's currency

###### **(3.2.11)** - Added scheduled commands, run at specified intervals (!schedule command)

###### **(3.2.11)** - Fixed the quote system to be less confusing & actually work

###### **(3.2.11)** - Updated code to work with Beam's chat API 10/9/15 changes

###### **(3.2.11)** - Fixed schedule command not working because of conflicting module & function names

##### **(3.2.12)** - 	Updated !schedule command to select randomly from the list of all registered messages every 5 minutes

##### **(3.2.12)** - Updated !schedule command syntax to only require the message text

##### **(3.2.12)** - Added code to send a ping over the websocket every 3 minutes to help keep the bot's connection alive

##### **(3.2.12a)** - Fixed !schedule command (broken by a rogue `break` statement) & variable name conflict

##### **(3.2.13)** - Added scheduled message removal capabilities

##### **(3.2.13)** - Fixed users not actually being announced when they enter or leave (and related crash)

##### **(3.2.13)** - Fixed crash caused by enter/leave announce fix

##### **(3.2.13)** - Related to ^: Fixed commands not being recognized

##### **(3.2.13)** - Fixed blame command not working properly

##### **(3.2.13)** - Added update capabilities to scheduled messages (via !schedule **update** MESSAGETEXTHERE) and also to custom commands (via !command **update** COMMANDHERE COMMANDTEXTHERE)

##### **(3.2.13)** - Fixed bug in usage code that crashed bot when returning usage

##### **(3.2.15)** - Added ability to remove quotes

##### **(3.2.15)** - Fixed a lot of minor bugs discovered by stress-testing the bot

**(3.2.16)** - Hopefully fixed NoneType not iterable exception that was crashing the bot

**(3.2.16)** - Added store command, customizable store that allows you add and remove items that cost a certain number of currency

**(3.2.16)** - Fixed bugs where users could send currency without being charged & users could give negative values (found by alfw)

### Info on future 3.3.0 release

The code has, as I've been adding to it, slowly been getting less tidy and well-written.

Plus, although I've tested the bot myself, I've yet to see it in action or have it truly tested by any other user than myself. (Thank you to @xcentrik4 on Twitter for letting me deploy my bot on his streams)

Thus, although I plan on adding a few new features and commands for 3.3.0, it's going to mainly be a boring (but very important) stability and quality improvement release.

**Plans for 3.3.0:**

* Clean up the codebase and stress-test/bug test the code with outside users, preferably in a production (live stream with active chat) environment.

* This release will fix bugs ~~#2~~ (Not going to change the bot name, at least not for 3.3.0), #3, ~~#5~~ (Fixed as of 3.2.3), ~~#6~~ (Fixed as of 3.2.3) and #7

### Recognitions
BreachX3 & 2Cubed & dminer78: For hanging out with me on the many, many streams that it took to get this bot in working order & always being happy to help & being super supportive
xcentrik4: Allowing me to deploy PyBot on his streams & for putting up with my programming mutterings & random bot crashes

###Current issues:

* Need to add more commands and features - The never-ending bug!

* Make `responses.py` use JSON/XML file to provide commands and responses (preferably JSON)

* Add ability to change default command responses (^)

* Anything else I can't think of at this time but is still applicable
