import os
from datetime import datetime, timedelta

from kiteconnect import KiteConnect

from helpers import config_reader

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
filename = os.path.join(directory, 'request_token.txt')
token = open(filename, "r")
kite.set_access_token(token.readline())


nifty50 = []
nifty200 = []
blacklist_sell = []
blacklist_buy = []


def read_nifty_50():
    global nifty50
    nifty50 = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/nifty50.txt')
    nifty50_file = open(filename, "r")
    while 1:
        # reading the file
        line = nifty50_file.readline()
        if len(line) == 0:
            break
        nifty50.append(line.strip())


def get_nifty_50_list():
    read_nifty_50()
    return nifty50


def is_nifty_50(stock):
    read_nifty_50()
    if stock in nifty50:
        return True
    return False


def read_nifty_200():
    global nifty200
    nifty200 = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/nifty200.txt')
    nifty200_file = open(filename, "r")
    while 1:
        # reading the file
        line = nifty200_file.readline()
        if len(line) == 0:
            break
        nifty200.append(line.strip())


def get_nifty_200_list():
    read_nifty_200()
    return nifty200


def is_nifty_200(stock):
    read_nifty_200()
    if stock in nifty200:
        return True
    return False


def read_blacklist_buy():
    global blacklist_buy
    blacklist_buy = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/blacklist_to_buy.txt')
    blacklist_buy_file = open(filename, "r")
    while 1:
        # reading the file
        line = blacklist_buy_file.readline()
        if len(line) == 0:
            break
        blacklist_buy.append(line.strip())


def is_blacklist_buy(stock):
    read_blacklist_buy()
    if stock in blacklist_buy:
        return True
    return False


def read_blacklist_sell():
    global blacklist_sell
    blacklist_sell = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/blacklist_to_sell.txt')
    blacklist_sell_file = open(filename, "r")
    while 1:
        # reading the file
        line = blacklist_sell_file.readline()
        if len(line) == 0:
            break
        blacklist_sell.append(line.strip())


def is_blacklist_sell(stock):
    read_blacklist_sell()
    if stock in blacklist_sell:
        return True
    return False


def portfolio_amount(name):
    holdings = kite.holdings()
    amount=0
    for holding in holdings:
        if holding['tradingsymbol'] == name:
            amount = holding['average_price'] * (holding['t1_quantity'] + holding['quantity'])
    return amount


def get_stock_amount(name):
    custom_amount = get_custom_trade_limit(name)
    if custom_amount is not None:
        return custom_amount
    if is_nifty_50(name):
        return 250000
    else:
        return 150000


def today_trading_amount(name):
    trade_amount=0
    for pos in kite.positions()['day']:
        if pos['tradingsymbol'] == name:
            trade_amount = pos['average_price'] * pos['quantity']
    return trade_amount


def get_custom_trade_limit(name):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/shakuni.txt')
    trade_file = open(filename, "r")
    while 1:
        # reading the file
        line = trade_file.readline()
        if len(line.split(",")) >= 2:
            stock = {"name": line.split(",")[0].strip(), "amount": float(line.split(",")[1].strip())}
            if stock["name"] == name:
                return stock["amount"]
        return None


def get_quantity_bucket(name, price):
    if is_nifty_50(name):
        quantity = int(int(config_reader.get("NIFTY_50_BUCKET")) / price)
    else:
        quantity = int(int(config_reader.get("NIFTY_200_BUCKET")) / price)
    return max(quantity, 1)


def purchase_percentile(name, comparing_with):
    if comparing_with == "HISTORICAL" and not applying_auto_values():
        if is_nifty_50(name):
            return -1.0 * float(config_reader.get("NIFTY_50_BUY"))
        else:
            return -1.0 * float(config_reader.get("NIFTY_200_BUY"))
    else:
        return -1.0 * float(config_reader.get("LAST_PURCHASE_DIFF"))


def get_quantity_bucket_to_sell(name, price, quantity):
    if price * quantity < int(config_reader.get("SELL_BUCKET")) *2:
        return quantity
    return int (int(config_reader.get("SELL_BUCKET"))/price)


def get_historical_price_to_compare(historical_price, stock_historical):
    if config_reader.get("RUNNING_MODE") == "AUTO":
        if market_mid_day():
            # print("Running in auto mode with average price" + datetime.utcnow() + timedelta(hours=5, minutes=30))
            historical_price = stock_historical['price']['average']
            return historical_price
        else:
            # print("Running in auto mode with minimum price")
            historical_price = stock_historical['price']['minimum']
            return historical_price
    if config_reader.get("HISTORICAL") == "MINIMUM":
        historical_price = stock_historical['price']['minimum']
    if config_reader.get("HISTORICAL") == "AVERAGE":
        historical_price = stock_historical['price']['average']
    return historical_price


def market_mid_day():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30) # time in indian timezone
    twelve_thiry = now.replace(hour=12, minute=30, second=0, microsecond=0)
    return now > twelve_thiry


def applying_auto_values():
    if config_reader.get("RUNNING_MODE") == "AUTO":
        if market_mid_day():
            print("Running in auto mode with Override values", (datetime.utcnow() + timedelta(hours=5, minutes=30)))
            return True
        else:
            print("Running in auto mode with Default values", (datetime.utcnow() + timedelta(hours=5, minutes=30)))
            return False
    return False
