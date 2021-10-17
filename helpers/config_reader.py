import os

directory = os.path.dirname(__file__)
filename = os.path.join(directory, '../CONFIG')

db_dict = dict()


def read_db():
    db_file = open(filename, "r")
    while 1:
        # reading the file
        line = db_file.readline()
        if line.find("###") == 0:
            continue
        if len(line.split(":")) < 2:
            break
        key = line.split(":")[0].strip()
        value = line.split(":")[1].strip()
        db_dict[key] = value
    db_file.close()


def get(key):
    read_db()
    if key not in db_dict:
        return "NA"
    return db_dict.get(key)
