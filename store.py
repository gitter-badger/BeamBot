import json
import os
import sqlite3

import usage

if os.path.exists('data/config.json'):
    config = json.load(open('data/config.json', 'r'))

storePath = 'data/store{}.json'.format(config["CHANNEL"])

def _dumpStore(toDump):
    if os.path.exists(storePath):
        with open(storePath, 'w') as f:
            json.dump(toDump, f, sort_keys=True, indent=4, separators=(',', ': '))
        return True
    else:
        return False

def _updateConfig():
    if os.path.exists('data/config.json'):
        return json.load(open('data/config.json', 'r'))

def _updateStore():
    if os.path.exists(storePath):
        return json.load(open(storePath, 'r'))

def storeEdit(user_name, cur_item, is_mod, is_owner):
    store_items = _updateStore()

    if cur_item[1] == "add":
        if len(cur_item[1:]) >= 4:  # Requires item title + cost + description
            title = cur_item[2]
            try:
                cost = int(cur_item[3])
            except:
                return usage.prepCmd(user_name, "store", is_mod, is_owner)

            description = " ".join(cur_item[4:])
            item_add = {
                "title":title,
                "cost":cost,
                "description":description
                }

            store_items.append(item_add)

            if _dumpStore(store_items):
                return "Store item " + title + " added. It will cost " + str(cost) + " " + config["currency_name"]
            else:
                print ("Store item addition failed, store JSON file missing!")
                return None
        else:
            return usage.prepCmd(user_name, "store", is_mod, is_owner)

    elif cur_item[1] == "remove":
        if len(cur_item[1:]) >= 2:
            store_items[:] = [item for item in store_items if item["title"] != cur_item[2].lower()]
            if _dumpStore(store_items):
                return "Store item {} removed".format(cur_item[2])
            else:
                print ("Store item removal failed, store JSON file missing!")
                return None
        else:
            return usage.prepCmd(user_name, "store", is_mod, is_owner)

    elif cur_item[1] == "edit":
        if len(cur_item[1:]) >= 4:  # Requires item title + cost + description
            for item in store_items:
                if item["title"] == cur_item[2].lower():
                    try:
                        item["cost"] = int(cur_item[3])
                    except:
                        return usage.prepCmd(user_name, "store", is_mod, is_owner)

                    item["description"] = " ".join(cur_item[4:])
                    break

            if _dumpStore(store_items):
                return "Store item {} updated! Cost: {}".format(cur_item[2], cur_item[3])
            else:
                print ("Store item editing failed, store JSON file is missing!")
                return None

        else:
            return usage.prepCmd(user_name, "store", is_mod, is_owner)

    else:
        return usage.prepCmd(user_name, "store", is_mod, is_owner)

def storeList(user_name, is_mod, is_owner):
    response = "Items for sale: "

    store_items = _updateStore()

    if len(store_items) == 0:
        return None

    for item in store_items:
    	response += item["title"] + ": " + str(item["cost"]) + ", "

    return response[:-2]    # [:-2] to remove rogue comma

def storeBuy(user_name, cur_item, is_mod, is_owner):
    from responses import give

    if len(cur_item) >= 2:
        cur_item = cur_item[1:]     # Make it just the arguments, remove the command string
    else:
        return usage.prepCmd(user_name, "buy", is_mod, is_owner)

    store_items = _updateStore()
    config = _updateConfig()

    for item in store_items:
        if cur_item[0].lower() == item["title"]:    # It matches an item in the store
            with sqlite3.connect('data/beambot.sqlite') as con:
                cur = con.cursor()

                command = '''SELECT gears
                            FROM gears
                            WHERE name LIKE \"%''' + user_name + '%\"'''

                cur.execute(command)

                results = cur.fetchall()

                if len(results) >= 1:
                    user_currency = int(results[0][0])
                    if user_currency >= item["cost"]:  # Does the user have enough currency?
                        new_currency = user_currency - item["cost"]

                        command = '''UPDATE gears
                                    SET gears={}
                                    WHERE name="{}"'''.format(new_currency, user_name)

                        cur.execute(command)

                        return item["description"]

                return "Not enough " + config["currency_name"]
