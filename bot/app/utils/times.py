import time


def get_times(start_time: int=None):

    unix_time = start_time or time.time()

    lcl = time.localtime(unix_time)
    offset = lcl.tm_sec + lcl.tm_min*60 + lcl.tm_hour*3600

    today = unix_time - offset
    week_ago = unix_time - offset - 3600*24*6
    month_ago = unix_time - offset - 360024*30

    return today, week_ago, month_ago
