import os

from kiteconnect import KiteConnect

from helpers import samay, karna, cachedb
from helpers.arjun import ohlc_and_put
from helpers.karna import execute_buy_order_with_minimum_config

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
filename = os.path.join(directory, 'request_token.txt')
token = open(filename, "r")
kite.set_access_token(token.readline())


def khareedo_kachua():
    sip_stocks = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/sip_orders.txt')
    sip_orders_file = open(filename, "r")
    while 1:
        # reading the file
        line = sip_orders_file.readline()
        if len(line) == 0:
            break
        sip_stocks.append(line.strip())
    for stock in sip_stocks:
        if samay.mid_day():
            sip_data = cachedb.get(stock + ": sip : Low%")
            if sip_data == "NA":
                day_low_price = kite.quote("NSE:" + stock)["NSE:" + stock]['ohlc']['low']
                karna.execute_buy_order(stock, day_low_price, 5000)
                cachedb.put(stock + ": sip : Low%", str(day_low_price))
        else:
            sip_data = cachedb.get(stock + ": sip : One%")
            if sip_data == "NA":
                price = kite.ohlc("NSE:" + stock)["NSE:" + stock]['ohlc']['low']
                price_to_buy = int(price * 0.99)
                karna.execute_buy_order(stock, price_to_buy, 5000)
                cachedb.put(stock + ": sip : One%", str(price_to_buy))