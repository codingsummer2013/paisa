from datetime import datetime, date

from helpers.arjun import read_historical_data, ohlc_and_put

read_historical_data()

print(ohlc_and_put("NSE:RELIANCE"))