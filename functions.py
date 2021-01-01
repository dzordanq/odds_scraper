from datetime import datetime, timezone, timedelta


def days_diffrence(event_date):
    event_date = datetime.fromisoformat(event_date)
    today_date = datetime.today()
    today_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
    date_diffrence = event_date - today_date
    
    return date_diffrence.days

def convert_utc_to_local(local_timezone, event_date):
    event_date = datetime.strptime(event_date,'%Y-%m-%dT%H:%M:%SZ')
    event_date = event_date.replace(tzinfo=timezone.utc).astimezone(tz=local_timezone)
    date = event_date.strftime("%Y-%m-%d")
    hour = event_date.strftime("%H:%M:%S")

    return date, hour

def convert_utc_to_local_for_nba(local_timezone, event_date):
    event_date = datetime.strptime(event_date,'%Y-%m-%dT%H:%M:%SZ')
    event_date = event_date.replace(tzinfo=timezone.utc).astimezone(tz=local_timezone)
    event_date = event_date - timedelta(minutes=10)
    date = event_date.strftime("%Y-%m-%d")
    hour = event_date.strftime("%H:%M:%S")

    return date, hour