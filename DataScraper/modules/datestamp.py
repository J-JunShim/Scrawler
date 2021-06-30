from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


def get_now():
    return datetime.now()


def get_date_days(daysBefore):
    now = get_now()
    date = now - timedelta(days=daysBefore)

    return date


def get_date_years(yearsBefore):
    now = get_now()

    return relativedelta(year=now.year - yearsBefore)


def timestamp():
    return get_now().strftime('%Y-%m-%d_%H%M%S')
