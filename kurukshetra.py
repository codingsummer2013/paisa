import time

from kiteconnect import KiteConnect

from helpers.Shakuntala import selling_price
from helpers.arjun import read_historical_data, is_historical_data_exists, get_historical_stock
from helpers.karna import execute_buy_order, execute_sell_order
from helpers.krishna import get_nifty_50_list, is_nifty_50, get_nifty_200_list, purchase_percentile

kite = KiteConnect(api_key="tf77pivddr8pmyin")
token = open("helpers/request_token.txt", "r")
kite.set_access_token(token.readline())


def khareed_arambh(stock):
    try:
        is_historical_data_exists(stock, True)
        holdings = kite.holdings()
        cur_stock_name = "NSE:" + str(stock)
        stock_historical = get_historical_stock(stock)
        if stock_historical is None:
            print("Historical information is Not available, Skipping", stock)
            return
        cur_price = kite.quote(cur_stock_name)[cur_stock_name]['last_price']
        prev_day_closing_price = kite.ohlc(cur_stock_name)[cur_stock_name]['ohlc']['close']
        holding_price = stock_historical["price"]
        for holding in holdings:
            if holding['tradingsymbol'] == stock and holding_price > holding['average_price']:
                holding_price = holding['average_price']
        for pos in kite.positions()['day']:
            if pos['tradingsymbol'] == stock_historical["name"] and pos['average_price'] != 0 and \
                    holding_price > pos['average_price']:
                holding_price = pos['average_price']
        change = float(float(cur_price - holding_price)) * float(100) / float(holding_price)
        print("Change for ", cur_stock_name, " ", change, " ", cur_price, " & holding", holding_price)
        if change < purchase_percentile(stock_historical["name"]) and cur_price < prev_day_closing_price:
            execute_buy_order(stock_historical["name"], cur_price)
    except Exception as e:
        print("Exception occurred, Skipping the instance", e, stock)


def becho_re():
    for stock in kite.holdings():
        if stock['average_price'] == 0:
            continue
        change = (100 * (stock['last_price'] - stock['average_price']) / stock['average_price'])
        print("Stock ", stock['tradingsymbol'], " Change", change)
        if stock['day_change_percentage'] > 0.5 and change > 2:
            quantity = stock["quantity"] + stock["t1_quantity"]
            today_quantity = 0
            for order in kite.orders():
                if (order['status'] != 'REJECTED' and order['status'] != 'CANCELLED') and order['tradingsymbol'] == stock['tradingsymbol']:
                    if order['transaction_type'] == 'SELL':
                        today_quantity = today_quantity - order['quantity']
                    if order['transaction_type'] == 'BUY':
                        today_quantity = today_quantity + order['quantity']
                    quantity = quantity + today_quantity
            print ("Selling Stock ", stock['tradingsymbol'], " Change", change, quantity)
            execute_sell_order(stock['tradingsymbol'], quantity, selling_price(stock['last_price']))


def khareedo_re():
    nifty200 = get_nifty_200_list()
    for stock in nifty200:
        khareed_arambh(stock)


while True:
    khareedo_re()
    becho_re()
    time.sleep(60)

