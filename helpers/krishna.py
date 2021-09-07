import os

nifty50 = []
nifty200 = []


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


def is_nifty_50(stock):
    read_nifty_200()
    if stock in nifty200:
        return True
    return False
