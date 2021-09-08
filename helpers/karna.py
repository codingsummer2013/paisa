import os
from datetime import date
from time import sleep

from kiteconnect import KiteConnect

from helpers.krishna import blacklist_sell, blacklist_buy, is_blacklist_sell, is_blacklist_buy, portfolio_amount, \
    get_stock_amount, today_trading_amount, get_quantity_bucket

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
filename = os.path.join(directory, 'request_token.txt')
token = open(filename, "r")
kite.set_access_token(token.readline())


def execute_buy_order(name, price):
    if is_blacklist_buy(name):
        print("Blacklisted to buy", name)
        return
    stock_max_amout = get_stock_amount(name)
    if portfolio_amount(name) + today_trading_amount(name) > stock_max_amout:
        print("Quantity exceeds trade amount, rejecting ", name)
        return

    order_id = kite.place_order(tradingsymbol= name,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=get_quantity_bucket(name, price),
                                order_type=kite.ORDER_TYPE_LIMIT,
                                price=price,
                                product=kite.PRODUCT_CNC,
                                variety=kite.VARIETY_REGULAR)
    print("Order placed. ID is: ", order_id)
    sleep(10)


def execute_sell_order(name, quantity, price):
    if is_blacklist_sell(name):
        print("Blacklisted to sell", name)
        return
    if quantity * price > 5000:
        order_id = kite.place_order(tradingsymbol= name,
                                    exchange=kite.EXCHANGE_NSE,
                                    transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    quantity=int(quantity),
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    price=price,
                                    product=kite.PRODUCT_CNC,
                                    variety=kite.VARIETY_REGULAR)
        print("Order placed. ID is: {}".format(order_id))
        sleep(10)
        result = name + "," + str(price) + "," + str(date.today()) + ",Sell\n"
        print(result)
