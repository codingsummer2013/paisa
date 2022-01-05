import json
import os
from datetime import datetime

historical_data = []
historical_row_data = []

def clean_historical_data():
    global historical_data
    historical_data = []
    global historical_row_data
    historical_row_data = []
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "r")
    while 1:
        # reading the file
        line = historical_file.readline()
        if len(line)<1 or len(line.split("~~~")) <2 :
            break
        if len(line.split("~~~")) == 2:
            info_list = json.loads(line.split("~~~")[1])
            historical_row_item = []
            for info in info_list:
                if (datetime.today() - datetime.strptime(info["time"].strip(), "%Y-%m-%d")).days < int(
                        90):
                    historical_row_item.append(info)
        historical_row_stock_detail = {"name": line.split("~~~")[0].strip(), "price": historical_row_item}
        historical_row_data.append(historical_row_stock_detail)
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, '../data/historical_data.txt')
    historical_file = open(filename, "w")
    for stock in historical_row_data:
        historical_file.write(stock["name"] + "~~~" + json.dumps(stock["price"]) + "\n")


clean_historical_data()