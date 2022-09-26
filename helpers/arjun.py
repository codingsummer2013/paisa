import json
import os
from datetime import datetime, date

import requests
from kiteconnect import KiteConnect

from helpers import config_reader
from helpers.Shakuntala import get_percentage_diff
from helpers.krishna import applying_auto_values

historical_data = []
historical_row_data = []

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
filename = os.path.join(directory, 'request_token.txt')
token = open(filename, "r")
kite.set_access_token(token.readline())


def read_historical_data():
    global historical_data
    historical_data = []
    global historical_row_data
    historical_row_data = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "r")
    if applying_auto_values():
        limit = 60
    else:
        limit = int(
            (config_reader.get("HISTORICAL_LIMIT")))
    while 1:
        # reading the file
        line = historical_file.readline()
        if len(line.split("~~~")) <2 :
            break
        if len(line.split("~~~")) == 2:
            info_list = json.loads(line.split("~~~")[1])
            count = 0
            sum = 0
            minimum = 999999
            maximum = 0
            historical_row_item = []
            for info in info_list:
                historical_row_item.append(info)
                if (datetime.today() - datetime.strptime(info["time"].strip(), "%Y-%m-%d")).days < limit:
                    count += 1
                    sum += float(info['price'])
                    minimum = min(minimum, float(info['price']))
                    maximum = max(maximum, float(info['price']))
            if count != 0:
                stock_historical_info = dict()
                stock_historical_info["average"] = sum / count
                stock_historical_info["minimum"] = minimum
                stock_historical_info["maximum"] = maximum
            else:
                return None
            stock = {"name": line.split("~~~")[0].strip(), "price": stock_historical_info}
        historical_row_stock_detail = {"name": line.split("~~~")[0].strip(), "price": historical_row_item}
        historical_row_data.append(historical_row_stock_detail)
        historical_data.append(stock)


def get_historical_data_list():
    read_historical_data()
    return historical_data


def is_historical_data_exists(stock, load=False):
    read_historical_data()
    exists = False
    for item in historical_data:
        if item["name"] == stock:
            exists = True
    if exists:
        return True
    if load:
        load_stock(stock)
    return False


def load_stock(stockname):
    # Use a breakpoint in the code line below to debug your script.
    params = {
        'access_key': '38cc942205b3dbe824710c0a64ac1ebb'
    }
    api_result = requests.get('http://api.marketstack.com/v1/tickers/' + stockname + '.XNSE/eod', params)
    api_response = api_result.json()
    trades = []
    for data in reversed(api_response['data']['eod']):
        # sample data = {'open': 1990.0, 'high': 2105.0, 'low': 1990.0, 'close': 2094.8, 'volume': 26051179.0, 'adj_high': None, 'adj_low': None, 'adj_close': 2094.8, 'adj_open': None, 'adj_volume': None, 'split_factor': 1.0, 'dividend': 0.0, 'symbol': 'RELIANCE.XNSE', 'exchange': 'XNSE', 'date': '2021-05-28T00:00:00+0000'}
        cur_object = dict()

        date_time_obj = datetime.strptime(data['date'].strip(), "%Y-%m-%dT%H:%M:%S+%f")
        cur_object["time"] = date_time_obj.strftime("%Y-%m-%d")
        cur_object["price"] = float(data['close'])
        trades.append(cur_object)

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "a")
    print(stockname + "~~~" + json.dumps(trades))
    historical_file.write(stockname + "~~~" + json.dumps(trades) + "\n")


def get_historical_stock(stockname):
    read_historical_data()
    for item in historical_data:
        if item["name"] == stockname:
            return item
    return None


def update_historical_file():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "w")
    for stock in historical_row_data:
        historical_file.write(stock["name"] + "~~~" + json.dumps(stock["price"]) + "\n")


def ohlc_and_put(stockname):
    output = kite.ohlc(stockname)
    date_string = date.today().strftime("%Y-%m-%d")
    for stock in historical_row_data:
        if stockname == "NSE:" + stock["name"]:
            data_exists = False
            for record in stock["price"]:
                if record['time'] == date_string:
                    data_exists = True
            if not data_exists:
                cur_object = dict()
                cur_object["time"] = date_string
                cur_object["price"] = output[stockname]['ohlc']['close']
                stock["price"].append(cur_object)
                update_historical_file()
    return output
