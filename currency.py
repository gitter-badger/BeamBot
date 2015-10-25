import os
import sqlite3
import json

import usage

if os.path.exists('data/config.json'):
    config = json.load(open('data/config.json', 'r'))

def _updateConfig():
    if os.path.exists('data/config.json'):
        return json.load(open('data/config.json', 'r'))

def give(user_name, cur_item, is_mod, is_owner):

    split = cur_item[1:].split()

    if len(split) >= 3:
        user_recv = split[1]    # User recieving dimes
        if user_recv[0] == '@':
            user_recv = user_recv[1:]           # Remove the @ character
            try:    # Try to convert argument to int type
                num_send = int(split[2])    # Number of dimes being transferred
            except: # Oops! User didn't provide an integer
                return usage.prepCmd(user_name, "give", is_mod, is_owner)

        if os.path.exists('data/beambot.sqlite'):
            with sqlite3.connect('data/beambot.sqlite') as con:
                cur = con.cursor()

                command = '''SELECT gears
                            FROM gears
                            WHERE name="{}"'''.format(user_recv)

                cur.execute(command)
                results = cur.fetchall()

                if len(results) >= 1:
                    recv_currency_original = results[0][0]

                    command = '''SELECT gears
                                FROM gears
                                WHERE name="{}"'''.format(user_name)

                    cur.execute(command)
                    results = cur.fetchall()

                    if len(results) >= 1:
                        send_currency_original = results[0][0]

                        if user_name == "PyBot":    # If it's bot, ignore removal of dimes & # check
                            user_recv_dimes = int(recv_currency_original) + int(num_send)
                            user_send_dimes = int(send_currency_original) - int(num_send)

                            command = '''UPDATE gears
                                        SET gears = CASE name
                                            WHEN "{}" THEN "{}"
                                            WHEN "{}" THEN "{}"
                                        END
                                        WHERE name IN ("{}","{}")'''.format(user_recv, user_recv_dimes,
                                                                        user_name, user_send_dimes,
                                                                        user_recv, user_name)

                            cur.execute(command)

                            return "@" + user_recv + " now has " + str(user_dimes) + " " + config['currency_name'] + "!"

                        if num_send <= recv_currency_original and num_send > 0: # Make sure the sending user has enough dimes & it's not 0 or negative

                            user_recv_dimes = int(recv_currency_original) + int(num_send)
                            user_send_dimes = int(send_currency_original) - int(num_send)

                            print ('user_recv:\t',user_recv)
                            print ('user_name:\t',user_name)
                            print ('user_send_dimes:',user_send_dimes)
                            print ('user_recv_dimes:',user_recv_dimes)
                            print ('num_send:\t',num_send)

                            # If name is user_recv, set the gears for that name to user_recv_dimes
                            # If name is user_name, set the gears for that name to send_new_dimes
                            command = '''UPDATE gears
                                        SET gears = CASE name
                                            WHEN "{}" THEN "{}"
                                            WHEN "{}" THEN "{}"
                                        END
                                        WHERE name IN ("{}","{}")'''.format(user_recv, user_recv_dimes,
                                                                        user_name, user_send_dimes,
                                                                        user_recv, user_name)

                            cur.execute(command)

                            return "@ {} now has {} {} !".format(user_recv, str(user_recv_dimes), config['currency_name'])

                        else:
                            return None

                    else:       # User not in dimes database
                        command = '''INSERT INTO gears
                                    (name, gears)
                                    VALUES ("{}", {})'''.format(user_recv, str(num_send))

                        cur.execute(command)    # Soooo... add 'em!

                        return "@ {} now has {} {} !".format(user_recv, str(num_send), config['currency_name'])
        else:
            return None
    else:
        return usage.prepCmd(user_name, "give", is_mod, is_owner)

def dimes(user_name, cur_item, is_mod, is_owner):

    split = cur_item[1:].split()

    if len(split) >= 2:
        if split[1][0] == "@":
            user = split[1][1:]     # Remove @ character
        else:
            user = split[1]
    else:
        user = user_name

    if os.path.exists('data/beambot.sqlite'):
        with sqlite3.connect('data/beambot.sqlite') as con:
            cur = con.cursor()

            command = '''SELECT gears
                        FROM gears
                        WHERE name LIKE \"%''' + user + '%\"'''

            cur.execute(command)

            results = cur.fetchall()

            # Return number of currency
            if len(results) >= 1:
                print ('results[0][0]:\t', str(results[0][0]))
                return str(results[0][0]), user
            else:
                return False, user

    else:
        return None
