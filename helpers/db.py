import os

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '../data/database.txt')

db_dict = dict()


def read_db():
    db_file = open(filename, "r")
    while 1:
        # reading the file
        line = db_file.readline()
        if len(line.split("~~~")) < 2:
            break
        if len(line.split("~~~")) >= 2:
            key = line.split("~~~")[0].strip()
            value = line.split("~~~")[1].strip()
            db_dict[key] = value
    db_file.close()


def get(key):
    read_db()
    return db_dict.get(key)


def get_price(key):
    read_db()
    return db_dict.get(key)


def put(key, value):
    db_dict[key] = value
    db_file = open(filename, "w")
    for key in db_dict:
        db_file.write(key + "~~~" + db_dict[key] + "\n")
    db_file.close()