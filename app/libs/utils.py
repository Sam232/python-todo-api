from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d"


class DateUtils:
    @staticmethod
    def format_date(date_object):
        return datetime.strftime(date_object, DATETIME_FORMAT)
