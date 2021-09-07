import os

import requests

from helpers.Shakuntala import get_percentage_diff

historical_data = []


def read_historical_data():
    global historical_data
    historical_data = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "r")
    while 1:
        # reading the file
        line = historical_file.readline()
        if len(line) == 0:
            break
        if len(line.split(",")) > 3:
            stock = {"name": line.split(",")[0].strip(), "price": float(line.split(",")[1].strip())}
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
    cumulative_price = 0
    api_response = api_result.json()
    day_count = 0
    moving_average = 30
    local_dict = {}
    last_price = 0
    for data in reversed(api_response['data']['eod']):
        day_count += 1
        cumulative_price += data['close']
        local_dict[day_count] = data['close']
        last_price = data['close']
        if day_count >= moving_average:
            cumulative_price -= local_dict[day_count - (moving_average - 1)]
    result = str(stockname) + ',' + str(float(cumulative_price / moving_average)) + ',' + str(last_price) + ',' + str(
        get_percentage_diff(float(cumulative_price / moving_average), last_price)) + "\n"
    print(result)
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "a")
    historical_file.write(result)


def get_historical_stock(stockname):
    read_historical_data()
    for item in historical_data:
        if item["name"] == stockname:
            return item
    return None

