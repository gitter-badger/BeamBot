import usage
import sqlite3
import os

def addQuote(user, split, is_mod, is_owner):

    # The user is the first item after !quote add
    if len(split) == 1:	# It's just a username, anything more indicates an incorrect command
        return usage.prepCmd(user, "quote", is_mod, is_owner)

    elif len(split) >= 2:
        # The quote is the second item(s) in the list
        quote = " ".join(split[1:]).replace('"', "''")

        command = '''INSERT INTO quotes
                    (name, quote)
                    VALUES ("{}", "{}")'''.format(user, quote)

        if os.path.exists('data/beambot.sqlite'):
            with sqlite3.connect('data/beambot.sqlite') as con:
                cur = con.cursor()
                cur.execute(command)
                return "Quote #" + str(cursor.lastrowid) + " added! " + quote + " - " + user
        else:
            return None

    else:
        return usage.prepCmd(user, "quote", is_mod, is_owner)

def removeQuote(user, split, is_mod, is_owner):

    # split is set to equal everything after the !quote add/remove
    user = split[0]

    if user[0] == '@':
        user = user[1:]	# Remove the @ sign, we work without them

    if len(split) == 1:	# It's just a username, anything more indicates an incorrect command
        return usage.prepCmd(user, "quote", is_mod, is_owner)

    elif len(split) >= 2:
        quote_id = split[1]

        command = """DELETE FROM quotes
                        WHERE id LIKE {}""".format(quote_id)

        if os.path.exists('data/beambot.sqlite'):
            with sqlite3.connect('data/beambot.sqlite') as con:
                cur = con.cursor()
                cur.execute(command)

                if cur.rowcount >= 1:
                    return "Quote #" + str(quote_id) + "removed " + quote + " - " + user
        else:
            return None

    else:
        return usage.prepCmd(user, "quote", is_mod, is_owner)
