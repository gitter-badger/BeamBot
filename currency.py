"""
	This file is part of PyBot,
	PyBot(c) RPiAwesomeness 2015-2016

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/agpl.html>.
"""

import os
import sqlite3
import json

import usage

if os.path.exists('data/config.json'):
    config = json.load(open('data/config.json', 'r'))

def _updateConfig():
    if os.path.exists('data/config.json'):
        return json.load(open('data/config.json', 'r'))

def _returnCon():
    if os.path.exists('data/beambot.sqlite'):
        con = sqlite3.connect('data/beambot.sqlite')
        return con
    else:
        return False

def _returnCurrency(user_name):
    con = _returnCon()
    if con != False:
        cur = con.cursor()

        command = '''SELECT gears
                    FROM gears
                    WHERE name="{}"'''.format(user_name)

        cur.execute(command)
        con.commit()

        results = cur.fetchall()
        con.close()

        return results

def _updateCurrency(user_name, new_total):
    con = _returnCon()
    if con != False:
        cur = con.cursor()

        command = '''UPDATE gears
                    SET gears={}
                    WHERE name="{}"'''.format(new_total, user_name)

        cur.execute(command)
        con.commit()

        results = cur.fetchall()
        con.close()
        return results

def _addName(user_name):    # Adds user to database
    con = _returnCon()

    if con != False:
        cur = con.cursor()

        command = '''INSERT INTO gears
                    (name, gears)
                    VALUES ("{}", 1)'''.format(user_name)

        cur.execute(command)

        con.commit()

        result = cur.fetchall()

        con.close()
        return result

def autoCurrency(user_recv, num_send):

    results = _returnCurrency(user_recv)

    if len(results) >= 1:   # At least one result for that user, user exists
        current_currency = results[0][0]
        current_currency += 1

        return _updateCurrency(user_recv, current_currency)

    else:               # Non-existent user, create them
        return _addName(user_recv)

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

        con = _returnCon()
        if con != False:
            results = _returnCurrency(user_recv)

            if len(results) >= 1:   # Check if the user recieving exists in the database
                recv_currency_original = results[0][0]  # The recieving user's current # of currency

                results = _returnCurrency(user_name)

                if len(results) >= 1:   # Check if the user sending exists in database
                    send_currency_original = results[0][0]  # The sending user's current # of currency

                    if num_send <= send_currency_original and num_send > 0: # Make sure the sending user has enough dimes & it's not 0 or negative

                        user_recv_dimes = int(recv_currency_original) + int(num_send)
                        user_send_dimes = int(send_currency_original) - int(num_send)

                        _updateCurrency(user_recv, user_recv_dimes)
                        _updateCurrency(user_name, user_send_dimes)

                        return "@ {} now has {} {} !".format(user_recv, str(user_recv_dimes), config['currency_name'])

                    else:
                        return None         # Sending user lacks enough currency to send

                else:       # User not in dimes database
                    _addName(user_recv)

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

    con = _returnCon()

    if con != False:

        results = _returnCurrency(user)

        # Return number of currency
        if len(results) >= 1:
            return str(results[0][0]), user
        else:
            return False, user
    else:
        return None
