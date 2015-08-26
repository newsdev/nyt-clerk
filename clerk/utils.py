import datetime

def current_term():
    now = datetime.datetime.now()
    if now.month < 10:
        return "%s" % (now.year - 1)
    else:
        return "%s" % now.year