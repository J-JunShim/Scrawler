from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


def get_now():
    return datetime.now()


def get_date(daysBefore):
    now = get_now()
    date = now - timedelta(days=daysBefore)

    return date


def get_date_years(yearsBefore):
    now = get_now()

    return relativedelta(year=now.year - yearsBefore)


def dt_format(dt):
    return dt.strftime('%Y%m%d')
