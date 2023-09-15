import json
import os
from datetime import datetime

from kiteconnect import KiteConnect

from helpers import db, config_reader
from helpers.db import read_db

directory = os.path.dirname(__file__)
# filename = os.path.join(directory, '../data/tradebook-UE9384.csv')

# tradebook = open(filename, "r")
dictionary = dict()
# tradebook.readline()  # ignore 1st line

stock_trades = dict()

# while 1:
#     # reading the file
#     line = tradebook.readline()
#     if len(line) == 0:
#         break
#     # print(line)
#     words = line.split(",")
#     name = words[0]
#     type = words[6]
#     time = words[11]
#     price = words[8]
#     key = name + ": " + type
#
#     cur_object = dict()
#     # 2021-04-05T10:57:28
#     date_time_obj = datetime.strptime(time.strip(), "%Y-%m-%dt%H:%M:%S")
#     cur_object["time"] = date_time_obj.strftime("%Y-%m-%d")
#     cur_object["price"] = price
#
#     if key in stock_trades:
#         stock_trades[key].append(cur_object)
#     else:
#         stock_trades[key] = [cur_object]
#
# for stock in stock_trades:
#     db.put(stock, json.dumps(stock_trades[stock]))
#     # print(stock)


def readdb():
    filename = os.path.join(directory, '../data/database.txt')
    tradebook = open(filename, "r")
    global dictionary
    dictionary = dict()
    while 1:
        # reading the file
        line = tradebook.readline()
        if len(line.split("~~~")) < 2:
            break
        if len(line.split("~~~")) >= 2:
            key = line.split("~~~")[0].strip() # jswsteel: buy:221116000711671
            value = json.loads(line.split("~~~")[1].strip())
            trade_key = key.split(":")[0].strip() + "||"+ key.split(":")[1].strip()
            if trade_key not in dictionary:
                dictionary[trade_key] = []
            dictionary[trade_key].append(value)
    tradebook.close()


def get_details(stock_name):
    readdb()
    buy_data = dictionary.get(stock_name.lower() + "||buy")
    sell_data = dictionary.get(stock_name.lower() + "||sell")
    stock_info = dict()
    if buy_data is not None:
        info_list = buy_data
        count=0
        sum=0
        minimum=999999
        maximum=0
        for info in info_list:
            if (datetime.today() - datetime.strptime(info["time"].strip(), "%Y-%m-%d")).days < int((config_reader.get("KHATA_BUY_DAYS"))):
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
    if sell_data is not None:
        info_list = sell_data
        count=0
        sum=0
        minimum=999999
        maximum=0
        for info in info_list:
            if (datetime.today() - datetime.strptime(info["time"].strip(), "%Y-%m-%d")).days < (int(config_reader.get("KHATA_SELL_DAYS"))):
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


def get_price_to_buy(stock):
    price = 9999999
    self_khata_details = get_details(stock.lower())
    if 'buy' in self_khata_details:
        if config_reader.get("BUY_COMPARISON") == "MINIMUM":
            db_price = self_khata_details['buy']['minimum']
        if config_reader.get("BUY_COMPARISON") == "AVERAGE":
            db_price = self_khata_details['buy']['average']
        if db_price < price:
            price = db_price
    if 'sell' in self_khata_details:
        if config_reader.get("SELL_COMPARISON") == "MAXIMUM":
            db_price = self_khata_details['sell']['maximum']
        if config_reader.get("SELL_COMPARISON") == "AVERAGE":
            db_price = self_khata_details['sell']['average']
        if db_price < price:
            price = db_price
    return price

# readdb()
# get_details("reliance")