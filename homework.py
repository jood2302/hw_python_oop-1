"""Project: Sprint 2. Calculator calories/money (four classes).

Class Record - Object of 3 values: 'amount', 'comment' and 'date'.
Class Calculator - get day limit at init stage and store it
and list of records.
Have methods - add_record(), get_today_stats(), get_week_stats()
and get_today_balance().
Class CaloriesCalculator - child class of Calculator.
Have method - get_calories_remained()
Class CashCalculator - child class of Calculator.
Have method - get_today_cash_remained().
"""

import datetime as dt
from typing import List, Optional

LOCAL_DATE_FORMAT: str = '%d.%m.%Y'


class Record:

    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        """If value 'date' skiped, set today."""

        self.amount: float = amount
        self.comment: str = comment

        if date is None:
            self.date: dt.date = dt.date.today()
        else:
            self.date = (dt.datetime.date(dt.datetime.strptime(date,
                                  LOCAL_DATE_FORMAT)))


class Calculator:

    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Calculate sum of field 'amount' in self list 'records'
        for current date. Return it."""

        return sum(v for v
                   in [x.amount for x in self.records
                       if x.date == dt.date.today()])

    def get_week_stats(self) -> float:
        """Calculate sum of field 'amount' in self list 'records'
        for last week. Return it."""

        today_date: dt.date = dt.date.today()
        week_ago_date: dt.date = today_date - dt.timedelta(days=7)
        return sum(v for v in
                   [x.amount for x in self.records
                    if week_ago_date < x.date <= today_date])

    def get_today_balance(self) -> float:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """Calculate difference between today_stats and day_limit.
        Return first or second message for user."""

        today_balance: float = self.get_today_balance()
        if today_balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {today_balance} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):

    EURO_RATE: float = 87.94
    USD_RATE: float = 73.91
    RUB_RATE: float = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Get currency name, calculate today balance,
        return message of result in carrency's monetary units.
        If currency name unknown, return err_message"""

        currency_attrib: dict = {'rub': ['руб', self.RUB_RATE],
                                 'eur': ['Euro', self.EURO_RATE],
                                 'usd': ['USD', self.USD_RATE]}

        if not currency_attrib[currency]:
            return 'Тип валюты не распознан, расчёт невозможен.'

        now_cash: float = self.get_today_balance()

        if now_cash == 0:
            return 'Денег нет, держись'

        divider: float = currency_attrib[currency][1]
        currency_name: str = currency_attrib[currency][0]
        now_cash_currency: float = round(now_cash / divider, 2)

        if now_cash_currency < 0:
            now_cash_currency = abs(now_cash_currency)
            return ('Денег нет, держись: твой долг - '
                    f'{now_cash_currency} {currency_name}')
        return ('На сегодня осталось '
                f'{now_cash_currency} {currency_name}')
