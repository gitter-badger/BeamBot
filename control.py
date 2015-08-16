def goodbye(is_owner, msgLocalID):
    if is_owner:
        packet = {
            "type":"method",
            "method":"msg",
            "arguments":['See you later my dear sir, wot wot!'],
            "id":msgLocalID
        }

        return packet, True	# Return the Goodbye message packet &
    else:		# Don't want anyone but owner killing the bot
        return None, False
