from datetime import datetime, timedelta


def ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30) # time in indian timezone


def mid_day():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)  # time in indian timezone
    twelve_pm = now.replace(hour=12, minute=0, second=0, microsecond=0)
    return now > twelve_pm