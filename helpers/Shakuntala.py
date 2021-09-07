def get_percentage_diff(previous, current):
    try:
        percentage = (previous - current)/max(previous, current) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage

