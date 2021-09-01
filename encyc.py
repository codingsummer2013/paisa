data = open("encyc.txt", "r")
while 1:
    # reading the file
    line = data.readline()

    if len(line) == 0:
        break
    key = line.split("~~")[0]
    value = line.split("~~")[1]
    print(key + " " + value)