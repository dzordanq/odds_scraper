from datetime import datetime

def days_diffrence(event_date):
    event_date = datetime.fromisoformat(event_date)
    today_date = datetime.today()
    today_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
    date_diffrence = event_date - today_date
    
    return date_diffrence.days