import datetime 

def get_current_date():
    x = datetime.datetime.now(datetime.timezone.utc)
    d = f"{x.strftime('%a')}, {x.strftime('%d')} {x.strftime('%b')} {x.strftime('%Y')} {x.strftime('%H')}:{x.strftime('%M')}:{x.strftime('%S')} GMT"
    return d

def load_static_file(file_name):
    try:
        with open(file_name) as f:
            return f.read()
    except FileNotFoundError:
        return None