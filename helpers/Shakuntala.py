def get_percentage_diff(previous, current):
    try:
        percentage = (previous - current)/max(previous, current) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage


def selling_price(price):
    price = int(price * 1005)
    while price % 50 != 0:
        price += 1
    return float(float(price) / float(1000))