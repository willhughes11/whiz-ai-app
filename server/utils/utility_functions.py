from datetime import datetime, date, timedelta
from decimal import Decimal

def object_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    elif isinstance(x, date):
        return x.isoformat()
    elif isinstance(x,timedelta):
        return(str(x))
    elif isinstance(x, Decimal):
        return float(x)