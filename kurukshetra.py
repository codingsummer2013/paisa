import time

from kiteconnect import KiteConnect

from helpers.arjun import read_historical_data, is_historical_data_exists, get_historical_stock
from helpers.karna import execute_buy_order
from helpers.krishna import get_nifty_50_list, is_nifty_50, get_nifty_200_list

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
            if pos['tradingsymbol'] == stock_historical["name"] and pos['average_price'] != 0 and holding_price > pos[
                'average_price']:
                holding_price = pos['average_price']
        change = float(float(cur_price - holding_price)) * float(100) / float(holding_price)
        print("Change for ", cur_stock_name, " ", change, " ", cur_price, " & holding", holding_price)
        trade_amount = 0
        for pos in kite.positions()['day']:
            if pos['tradingsymbol'] == stock_historical["name"]:
                trade_amount = pos['average_price'] * pos['quantity']
        if trade_amount > 50000:
            print("Trade amount reached", cur_stock_name)
            return
        else:
            if change < -1 and cur_price < prev_day_closing_price:
                try:
                    execute_buy_order(stock_historical["name"], int(10000 / cur_price), cur_price)
                except Exception as e:
                    print("Exception occured for stock", stock_historical, e)
                    time.sleep(10)
        time.sleep(20)

    except Exception as e:
        print("Exception occurred, Skipping the instance", e, stock)

while True:
    nifty200 = get_nifty_200_list()
    for stock in nifty200:
        khareed_arambh(stock)
    time.sleep(60)

