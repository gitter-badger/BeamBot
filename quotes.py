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

import usage
import sqlite3
import os

def addQuote(user_name, quote_user, split, is_mod, is_owner):

    split = split[2:] # split is set to equal everything after the !quote add/remove

    # The user is the first item after !quote add
    if len(split) == 1:	# It's just a username, anything more indicates an incorrect command
        return usage.prepCmd(user_name, "quote", is_mod, is_owner)

    elif len(split) >= 2:
        # The quote is the second item(s) in the list
        quote = " ".join(split[1:]).replace('"', "''")

        command = '''INSERT INTO quotes
                    (name, quote)
                    VALUES ("{}", "{}")'''.format(quote_user, quote)

        if os.path.exists('data/beambot.sqlite'):
            with sqlite3.connect('data/beambot.sqlite') as con:
                cur = con.cursor()
                cur.execute(command)
                return "Quote #" + str(cur.lastrowid) + " added! " + quote + " - " + quote_user
        else:
            return None

    else:
        return usage.prepCmd(user, "quote", is_mod, is_owner)

def removeQuote(user, split, is_mod, is_owner):

    if len(split) == 1:	# It's just a username, anything more indicates an incorrect command
        return usage.prepCmd(user, "quote", is_mod, is_owner)

    elif len(split) >= 2:
        quote_id = split[2]

        command = """DELETE FROM quotes
                        WHERE id LIKE {}""".format(quote_id)

        if os.path.exists('data/beambot.sqlite'):
            with sqlite3.connect('data/beambot.sqlite') as con:
                cur = con.cursor()
                cur.execute(command)

                if cur.rowcount >= 1:
                    return "Quote #" + str(quote_id) + " removed."
        else:
            return None

    else:
        return usage.prepCmd(user, "quote", is_mod, is_owner)
