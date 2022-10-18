import time
from datetime import datetime, date, timedelta

from kiteconnect import KiteConnect

from helpers import db, khatabook, config_reader
from helpers.Shakuntala import selling_price
from helpers.arjun import read_historical_data, is_historical_data_exists, get_historical_stock, \
    ohlc_and_put
from helpers.db import log_todays_entries
from helpers.kachua import khareedo_kachua
from helpers.karna import execute_buy_order_with_minimum_config, execute_sell_order
from helpers.krishna import get_nifty_50_list, is_nifty_50, get_nifty_200_list, purchase_percentile, \
    get_historical_price_to_compare

kite = KiteConnect(api_key="tf77pivddr8pmyin")
token = open("helpers/request_token.txt", "r")
kite.set_access_token(token.readline())

skipped_market_check = False


def khareed_arambh(stock):
    try:
        is_historical_data_exists(stock, False)
        holdings = kite.holdings()
        cur_stock_name = "NSE:" + str(stock)
        # Switching off historical logic
        stock_historical = get_historical_stock(stock)
        # if stock_historical is None:
        #     print("Historical information is Not available, Skipping", stock)
        #     return
        cur_price = kite.quote(cur_stock_name)[cur_stock_name]['last_price']
        prev_day_closing_price = ohlc_and_put(cur_stock_name)[cur_stock_name]['ohlc']['close']
        # historical_price = 999999
        # historical_price = get_historical_price_to_compare(historical_price, stock_historical)

        holding_price = prev_day_closing_price
        comparing_with = "Previous day"
        for holding in holdings:
            if holding['tradingsymbol'] == stock:
                comparing_with = "HOLDING"
                if holding_price > holding['average_price']:
                    holding_price = holding['average_price']
        for pos in kite.positions()['day']:
            if pos['tradingsymbol'] == str(stock) and pos['average_price'] != 0:
                comparing_with = "DAY"
                if holding_price > pos['average_price']:
                    holding_price = pos['average_price']

        for order in kite.orders():
            if order['status'] != 'REJECTED' and order['status'] != 'CANCELLED' and order['tradingsymbol'] == \
                    stock and \
                    order['transaction_type'] == 'BUY':
                comparing_with = "ORDER"
                if holding_price > order['price']:
                    holding_price = order['price']
        change = float(float(cur_price - holding_price)) * float(100) / float(holding_price)

        percentage = purchase_percentile(str(stock), comparing_with)
        print("Khareedna Run: Change for ", cur_stock_name, " ", change, " ", cur_price, "Compared price",
              holding_price, "Compared percentage", percentage, "Comparing with", comparing_with)

        if change < percentage and cur_price < prev_day_closing_price:

            # apply khud ki khatabook checks
            db_price = holding_price
            self_khata_details = khatabook.get_details(stock)
            if 'buy' in self_khata_details:
                if config_reader.get("BUY") == "MINIMUM":
                    db_price = self_khata_details['buy']['minimum']
                if config_reader.get("BUY") == "AVERAGE":
                    db_price = self_khata_details['buy']['average']
                if db_price is not None and holding_price > float(db_price):
                    holding_price = float(db_price)
                    percentage = 0.2
            change = float(float(cur_price - holding_price)) * float(100) / float(holding_price)

            if change < percentage:
                execute_buy_order_with_minimum_config(str(stock), cur_price)
    except Exception as e:
        print("Exception occurred, Skipping the instance", e, stock)


def becho_re():
    for stock in kite.holdings():
        try:
            if stock['average_price'] == 0:
                continue
            compared_price = stock['average_price']
            percentage = float(config_reader.get("SELL_PROFIT_PERCENTAGE"))
            change = (100 * (stock['last_price'] - compared_price) / compared_price)

            # BUY price check
            if change < percentage:
                continue

            """ Disabling khatabook checks for now
            # apply khud ki khatabook checks
            self_khata_details = khatabook.get_details(stock['tradingsymbol'])
            if 'sell' in self_khata_details:
                if config_reader.get("SELL") == "MAXIMUM":
                    db_price = self_khata_details['sell']['maximum']
                if config_reader.get("SELL") == "AVERAGE":
                    db_price = self_khata_details['sell']['average']
                if db_price is not None and compared_price < float(db_price):
                    compared_price = float(db_price)
                    percentage = 0.2
            """

            change = (100 * (stock['last_price'] - compared_price) / compared_price)
            print("Bechna Run: Stock ", stock['tradingsymbol'], " Change", change, "Compared price", compared_price,
                  " Actual price ", stock['last_price'])
            price_to_sell = selling_price(stock['last_price'])
            if stock['day_change_percentage'] > float(config_reader.get("SELL_DAY_CHANGE_PERCENTILE")) and change > percentage:
                quantity = stock["quantity"] + stock["t1_quantity"]
                today_quantity = 0
                for order in kite.orders():
                    if (order['status'] != 'REJECTED' and order['status'] != 'CANCELLED') and order['tradingsymbol'] == \
                            stock['tradingsymbol']:
                        if order['transaction_type'] == 'SELL':
                            today_quantity = today_quantity - order['quantity']
                        if order['transaction_type'] == 'BUY':
                            today_quantity = today_quantity + order['quantity']
                        quantity = quantity + today_quantity

                for order in kite.orders():
                    if order['status'] != 'REJECTED' and order['status'] != 'CANCELLED' and order['tradingsymbol'] == \
                            stock['tradingsymbol'] and price_to_sell < order['price'] and \
                            order['transaction_type'] == 'SELL':
                        price_to_sell = max(price_to_sell, order['price'])
                print("Selling Stock ", stock['tradingsymbol'], " Change", change, quantity)
                execute_sell_order(stock['tradingsymbol'], quantity, selling_price(price_to_sell))
        except Exception as e:
            print("Exception occurred, Skipping the instance", e, stock)


def khareedo_re():
    nifty200 = get_nifty_50_list()
    for stock in nifty200:
        khareed_arambh(stock)
    # khareed_arambh("HCLTECH")


def market_closed():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30) # time in indian timezone
    four_pm = now.replace(hour=15, minute=45, second=0, microsecond=0)
    return now > four_pm


while True:
    if (not market_closed()) or skipped_market_check:
        khareedo_kachua()
        becho_re()
        khareedo_re()
        # becho_re()
        time.sleep(60)
    else:
        log_todays_entries()
        print("Done for the day")
        time.sleep(60000)
