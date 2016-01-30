import datetime
from common.deprecated import deprecated

@deprecated
def timestamp():
    return current()

def current():
    return int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds() * 1000)