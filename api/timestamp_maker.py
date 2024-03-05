from datetime import datetime, timedelta


class TimestampMaker:
    @staticmethod
    def get_prev_month_timestamps():
        current_date = datetime.now()
        first_day_current_month = current_date.replace(day=1)
        first_day_last_month = first_day_current_month - timedelta(days=1)
        first_day_last_month = first_day_last_month.replace(day=1)
        last_day_last_month = first_day_current_month - timedelta(days=1)
        last_month_first_moment = first_day_last_month.strftime('%Y-%m-%d 00:00')
        last_month_last_moment = last_day_last_month.strftime('%Y-%m-%d 23:59')
        return last_month_first_moment, last_month_last_moment, first_day_last_month

    @staticmethod
    def get_prev_month_for_email():
        current_date = datetime.now()
        first_day_current_month = current_date.replace(day=1)
        first_day_last_month = first_day_current_month - timedelta(days=1)
        return  first_day_last_month.strftime("%m/%Y")

    @staticmethod
    def is_it_the_second_to_new_month():
        current_date = datetime.now()
        return current_date.day == 2
