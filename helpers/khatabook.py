import os
from datetime import datetime

from helpers import db

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '../data/tradebook-UE9384.csv')

tradebook = open(filename, "r")
dictionary = dict()
tradebook.readline() # ignore 1st line
while 1:
    # reading the file
    line = tradebook.readline()
    if len(line) == 0:
        break
    # print(line)
    words = line.split(",")
    name = words[0]
    type = words[6]
    time = words[11]
    price = words[8]
    key = name + ": " + type

    cur_object = dict()
    # 2021-04-05T10:57:28
    date_time_obj = datetime.strptime(time.strip(), "%Y-%m-%dt%H:%M:%S")
    cur_object["time"] = date_time_obj
    cur_object["price"] = price

    overwrite = True

    if key in dictionary:
        obj = dictionary[key]
        dt = obj["time"]
        price = obj["price"]

    if overwrite:
        dictionary[key] = cur_object
        if type == "sell":
            db.put(key, str(price))
