import os
from datetime import date
from time import sleep

from kiteconnect import KiteConnect

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
filename = os.path.join(directory, 'request_token.txt')
token = open(filename, "r")
kite.set_access_token(token.readline())


def execute_buy_order(name, quantity, price):
    order_id = kite.place_order(tradingsymbol= name,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=max(quantity, 1),
                                order_type=kite.ORDER_TYPE_LIMIT,
                                price=price,
                                product=kite.PRODUCT_CNC,
                                variety=kite.VARIETY_REGULAR)
    print("Order placed. ID is: ", order_id)
    sleep(10)



def execute_sell_order(name, quantity, price):
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
