"""Project: Sprint 2. Calculator calories/money (four classes).

Class Record
Class Calculator
Class CaloriesCalculator
Class CashCalculator.
"""

import datetime as dt
from typing import List, Optional

LOCAL_DATE_FORMAT: str = '%d.%m.%Y'


class Record:
    """Object of 3 values: 'amount', 'comment' and 'date'.'"""

    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        """if value 'date' skiiped, turn today."""

        self.amount: float = amount
        self.comment: str = comment

        if date is None:
            self.date: dt.date = dt.date.today()
        else:
            self.date: dt.date = (dt.datetime.date(dt.datetime.strptime(date,
                                  LOCAL_DATE_FORMAT)))


class Calculator:
    """Parent class. Contains basic functionality,
       including list or records."""

    def __init__(self, limit: int) -> None:
        """Value "limit" - day limit for proper functioning own methods."""
        self.limit: int = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        """calculates sum of field 'amount' in self list 'records'
        for current date.
        """
        return self.get_day_stats(dt.date.today())

    def get_week_stats(self) -> float:
        """calculates sum of field 'amount' in self list 'records' for
        current date and six days ago.
        """

        today_date: dt.date = dt.date.today()
        tmp_list: List = [x.amount for x in self.records
                          if (dt.timedelta(days=7)
                              > (today_date - x.date)
                              >= dt.timedelta(days=0))]

        return sum(v for v in tmp_list)

    def today_balance(self) -> float:
        return self.limit - self.get_today_stats()

    def get_day_stats(self, date: dt.date) -> float:
        tmp_list: List = [x.amount for x in self.records if x.date == date]
        return sum(v for v in tmp_list)


class CaloriesCalculator(Calculator):
    """Child class of 'Calculator'. All of this included.
    Added new own method get_calories_remained().
    """

    def get_calories_remained(self) -> str:
        """Calculates difference between today_stats and day_limit
        and print first or second message for user.
        """

        overhead: float = self.today_balance()
        if overhead > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {overhead} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Simple upgrade of class Calculator for specific
    functionality.
    """

    EURO_RATE: float = 87.94
    USD_RATE: float = 73.91
    RUB_RATE: float = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Get currency name, calculate today balance,
        return message of result in carrency's dimensions.
        """

        self.currency_attrib: dict = {'rub': 'руб',
                                      'eur': 'Euro',
                                      'usd': 'USD'}

        self.currency_rate: dict = {'rub': self.RUB_RATE,
                                    'eur': self.EURO_RATE,
                                    'usd': self.USD_RATE}

        now_cash: float = self.limit - self.get_today_stats()

        if now_cash == 0:
            return 'Денег нет, держись'

        divider: float = self.currency_rate[currency]
        now_cash_currency: float = round(now_cash / divider, 2)
        currency_name: str = self.currency_attrib[currency]

        if now_cash_currency < 0:
            now_cash_currency = abs(now_cash_currency)
            return ('Денег нет, держись: твой долг - '
                    f'{now_cash_currency} {currency_name}')
        return ('На сегодня осталось '
                f'{now_cash_currency} {currency_name}')
