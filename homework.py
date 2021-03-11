# Project: Sprint 2. Calculator calories/money (four classes).
# Yandex.Praktikum.Python developer.
# Author: Vasiliy Kovylin. Backend, Cohort 16, Student.

# Description:
# Need make four classes for two calculators:
# Class Record
# Class Calculator
# Class CaloriesCalculator
# Class CashCalculator

# Methods for Record:
# no methods, only data

# Methods for Calculator:
# add_record()
# get_today_stats()
# get_week_stats()
#
# Methods for CaloriesCalculator:
# get_calories_remained()
#
# Methods for CashCalculator:
# get_today_cash_remained(currency)

import datetime as dt
from typing import List

LOCAL_DATE_FORMAT: str = '%d.%m.%Y'


def time_to_date(date: str) -> dt.date:
    """ Get string of date in format "dd.dd.yyyy" and
        return dt.date obj with this

    """
    tmp_date: List[str] = date.split('.')
    return dt.date(tmp_date[0], tmp_date[1], tmp_date[2])


class Record:
    """ is object of 3 values: 'amount', 'comment' and 'date'

    """

    def __init__(self, amount: float, comment: str, date: str = None) -> None:
        """ Needs 3 named values: 'amount', 'comment' and 'date'
            In call of this, value 'date' may be skipped
            In this case, in the value 'date' should be
            written the value of current day.

        """
        self.amount: float = amount
        self.comment: str = comment

        if date is None:
            self.date: dt.date = dt.date.today()
        else:
            self.date: dt.date = time_to_date(date)
            # dt.datetime.strptime(date, LOCAL_DATE_FORMAT)


class Calculator:
    """ Parent class. Contains basic functionality, including list or records.

    """
    def __init__(self, limit: int) -> None:
        """ Value "limit" - day limit for proper functioning own methods

        """
        self.limit: int = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """  Adds record to self list of records. Incoming - obj of class Record

        """
        self.records.append(record)

    def get_today_stats(self) -> float:
        """ calculates sum of field 'amount' in self list 'records' for current date

        """
        today: dt.date = dt.date.today()
        today_sum: float = 0
        for rec in self.records:
            if rec.date == today:
                today_sum += rec.amount
        return today_sum

    def get_week_stats(self) -> float:
        """ calculates sum of field 'amount' in self list 'records' for current date
            and six days ago
        """
        today: dt.date = dt.date.today()
        week_sum: float = 0
        for rec in self.records:
            if rec.date > today - dt.timedelta(days=7) and rec.date <= today:
                week_sum += rec.amount
        return week_sum


class CaloriesCalculator(Calculator):
    """ Child class of 'Calculator'. All of this included.
        Added new own method
    """
    def get_calories_remained(self) -> str:
        """ Calculates difference between today_stats and day_limit
            and print first or second message for user
        """
        is_over: float = self.limit - self.get_today_stats()
        if is_over > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f' но с общей калорийностью не более {is_over} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """ Child class of 'Calculator'. All of this included.
        Added new own method

    """
    EURO_RATE: float = 87.94
    USD_RATE: float = 73.91

    def __init__(self, limit: int) -> None:
        """ Currency rate are defined into class

        """
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str) -> str:
        """ From call wait 1 of 3 currency name, calculates balance and
            return message with the value in the recalculated form.

        """

        now_cash: float = self.limit - self.get_today_stats()

        if currency == 'usd':
            multiplier: float = 1 / self.USD_RATE
            currency_name: str = 'USD'
        elif currency == 'eur':
            multiplier: float = 1 / self.EURO_RATE
            currency_name: str = 'Euro'
        else:
            multiplier: float = 1
            currency_name: str = 'руб'

        if now_cash == 0:
            return 'Денег нет, держись'

        elif now_cash < 0:
            now_cash *= -1
            return (f"Денег нет, держись: твой долг - "
                    f"{round(now_cash *  multiplier, 2)} {currency_name}")
        else:
            return (f"На сегодня осталось "
                    f"{round(now_cash *  multiplier, 2)} {currency_name}")
