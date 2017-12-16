from datetime import datetime


def fromtimestamp(timestamp):
    import pytz
    utc = pytz.timezone('UTC')
    if isinstance(timestamp, (int, float)):
        dt = datetime.utcfromtimestamp(timestamp)
    else:
        dt = timestamp
    return dt.replace(tzinfo=utc)
