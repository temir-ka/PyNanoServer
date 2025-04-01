import datetime 

def get_current_date():
    x = datetime.datetime.now(datetime.timezone.utc)
    d = f"{x.strftime('%a')}, {x.strftime('%d')} {x.strftime('%b')} {x.strftime('%Y')} {x.strftime('%H')}:{x.strftime('%M')}:{x.strftime('%S')} GMT"
    return d
