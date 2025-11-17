from datetime import datetime

def set_current_date() -> str:
    date = datetime.now()
    return date.strftime('%d.%m.%Y %H:%M')