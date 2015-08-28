import subprocess
from time import sleep
import requests
import json
import os

config = json.load(open('data/config.json', 'r'))   # Read in the data from the config.json config file
addr = config['BEAM_ADDR']      # Get the Beam.pro API link
chan = config['CHANNEL']        # Get the Beam.pro channel ID

session = requests.Session()    # Create a REST requests thingy to communicate with the Beam servers

while True:         # Loop forever

    is_live = False

    chanStatus = session.get(
        addr + '/channels/' + chan
    )   # Get the information about the channel

    try:
        is_live = chanStatus.json()['online']   # Get the status of the channel
    except:     # online is not a key in the chanStatus JSON data
        print ('online is not a key!')
        is_live = False

    if is_live:     # If the channel is live...
        if not os.path.exists(chan + '.lock'):  # Check if the bot is running via channel ID.lock file
            try:
                subprocess.call(['python3','beambot.py'])   # Launch the bot
            except KeyboardInterrupt:           # Grab Ctrl-C
                if os.path.exists(chan + '.lock'):
                    os.remove(chan + '.lock')
                    quit()  # Eventually add code to send !goodbye command
        else:                                   # Bot is already running, don't launch it again!
            pass
