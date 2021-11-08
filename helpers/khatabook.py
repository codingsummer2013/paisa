import json
import os
from datetime import datetime

from kiteconnect import KiteConnect

from helpers import db, config_reader
from helpers.db import read_db

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '../data/tradebook-UE9384.csv')

tradebook = open(filename, "r")
dictionary = dict()
tradebook.readline()  # ignore 1st line

stock_trades = dict()

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
    cur_object["time"] = date_time_obj.strftime("%Y-%m-%d")
    cur_object["price"] = price

    if key in stock_trades:
        stock_trades[key].append(cur_object)
    else:
        stock_trades[key] = [cur_object]

for stock in stock_trades:
    db.put(stock, json.dumps(stock_trades[stock]))
    # print(stock)


def get_details(stock_name):
    buy_data = db.get(stock_name + ": buy")
    sell_data = db.get(stock_name + ": sell")
    stock_info = dict()
    if buy_data != "NA":
        info_list = buy_data
        count=0
        sum=0
        minimum=999999
        maximum=0
        for info in info_list:
            if (datetime.today() - datetime.strptime(info["time"].strip(), "%Y-%m-%d")).days < int((config_reader.get("TIME_LIMIT")) * 30):
                count += 1
                sum += float(info['price'])
                minimum = min(minimum, float(info['price']))
                maximum = max(maximum, float(info['price']))
        if count !=0:
            buy_info = dict()
            buy_info["average"] = sum/count
            buy_info["minimum"] = minimum
            buy_info["maximum"] = maximum
            stock_info["buy"] = buy_info
    if sell_data != "NA":
        info_list = sell_data
        count=0
        sum=0
        minimum=999999
        maximum=0
        for info in info_list:
            if (datetime.today() - datetime.strptime(info["time"].strip(), "%Y-%m-%d")).days < (int(config_reader.get("TIME_LIMIT")) * 30):
                count += 1
                sum += float(info['price'])
                minimum = min(minimum, float(info['price']))
                maximum = max(maximum, float(info['price']))
        if count !=0:
            sell_info = dict()
            sell_info["average"] = sum/count
            sell_info["minimum"] = minimum
            sell_info["maximum"] = maximum
            stock_info["sell"] = sell_info
    return stock_info