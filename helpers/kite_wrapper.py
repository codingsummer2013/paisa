import json
import os

from kiteconnect import KiteConnect

kite = KiteConnect(api_key="tf77pivddr8pmyin")
directory = os.path.dirname(__file__)
toeken_filename = os.path.join(directory, 'request_token.txt')
token = open(toeken_filename, "r")
kite.set_access_token(token.readline())


def orders(mock_behaviour=False):
    if mock_behaviour:
        db_file = open(os.path.join(directory, '../tests/data/orders_mock_data.txt'), "r")
        response = db_file.readline()
        return json.loads(response)
    else:
        return kite.orders()
