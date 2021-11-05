import json
import os

from kiteconnect import KiteConnect

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '../data/database.txt')

db_dict = dict()

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
toeken_filename = os.path.join(directory, 'request_token.txt')
token = open(toeken_filename, "r")
kite.set_access_token(token.readline())

def read_db():
    db_file = open(filename, "r")
    while 1:
        # reading the file
        line = db_file.readline()
        if len(line.split("~~~")) < 2:
            break
        if len(line.split("~~~")) >= 2:
            key = line.split("~~~")[0].strip()
            value = line.split("~~~")[1].strip()
            db_dict[key] = value
    db_file.close()


def get(key):
    read_db()
    if key not in db_dict:
        return "NA"
    return db_dict.get(key)


def put(key, value):
    db_dict[key] = value
    db_file = open(filename, "w")
    for key in db_dict:
        db_file.write(key + "~~~" + db_dict[key] + "\n")
    db_file.close()


def update_db_file():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/database.txt')
    db_file = open(filename, "w")
    for key in db_dict.keys():
        db_file.write(key + "~~~" + json.dumps(db_dict[key]) + "\n")


def log_todays_entries():
    read_db()
    for order in kite.orders():
        if order['status'] == 'COMPLETE':
            key = db_dict[order['tradingsymbol'] + ": " + order['transaction_type'].lower()]
            item = dict()
            item['time'] = order['exchange_timestamp'].strftime("%Y-%m-%d")
            item['price'] = order['price']
            list = []
            if key in db_dict:
                list = db_dict[key]
            list.append(item)
            db_dict[key] = list
    update_db_file()