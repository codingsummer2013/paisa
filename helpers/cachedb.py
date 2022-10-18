import json
import os
from datetime import datetime

from kiteconnect import KiteConnect

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '../data/cache_database.txt')

db_dict = dict()
today_date = str(datetime.today().day) + "-" +str(datetime.today().month) + "-"+str(datetime.today().year)

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
            value = (line.split("~~~")[1].strip())
            db_dict[key] = value
    db_file.close()


def clear_cache():
    db_file = open(filename, "w")
    db_file.close()


def get(key):
    read_db()
    global db_dict
    if db_dict.get("AAJ") != today_date:
        clear_cache()
        db_dict = dict()
    if key not in db_dict:
        return "NA"
    return db_dict.get(key)


def put(key, value):
    db_dict[key] = value
    db_file = open(filename, "w")
    db_file.write("AAJ" + "~~~" + str(today_date) + "\n")
    for key in db_dict:
        db_file.write(key + "~~~" + str(db_dict[key]) + "\n")
    db_file.close()
