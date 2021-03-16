"""Project: Sprint 2. Calculator calories/money (four classes)."""
import datetime as dt
from typing import List, Optional, Tuple

LOCAL_DATE_FORMAT: str = '%d.%m.%Y'


class Record:

    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        """Save values in instance."""
        """If the 'date' value is omitted, set the value as today."""
        self.amount: float = amount
        self.comment: str = comment
        self.date: dt.date
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, LOCAL_DATE_FORMAT).date()


class Calculator:

    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Calculate sum 'amount' for current date. Return it."""
        day_today: dt.date = dt.date.today()
        
        return sum(x.amount for x in self.records
                   if x.date == day_today)

    def get_week_stats(self) -> float:
        """Calculate sum 'amount' for last week. Return it."""
        day_today: dt.date = dt.date.today()
        week_ago_date: dt.date = day_today - dt.timedelta(days=7)
        
        return sum(x.amount for x in self.records
                   if week_ago_date < x.date <= today_date)

    def get_today_balance(self) -> float:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """Calculate day balance. Return message."""
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
        """Get currency. Calculate today balance. Return message."""
        now_cash: float = self.get_today_balance()

        if now_cash == 0:
            return 'Денег нет, держись'
                
        currency_attrib: dict = {'rub': ['руб', self.RUB_RATE],
                                 'eur': ['Euro', self.EURO_RATE],
                                 'usd': ['USD', self.USD_RATE]}
        
        """currency_attrib: Tuple = ('rub': ['руб', self.RUB_RATE],
                                 'eur': ['Euro', self.EURO_RATE],
                                 'usd': ['USD', self.USD_RATE])"""


        cur_currency_attrib: Optional[List] = currency_attrib.get(currency)
        if cur_currency_attrib is None:
            return (f'Тип валюты {currency} неизвестен.'
                    'Корректный расчёт невозможен.')

        divider: float = cur_currency_attrib[1]
        currency_name: str = cur_currency_attrib[0]
        now_cash_currency: float = round(now_cash / divider, 2)

        if now_cash_currency < 0:
            today_debt: float = abs(now_cash_currency)
            return ('Денег нет, держись: твой долг - '
                    f'{today_debt} {currency_name}')
        return ('На сегодня осталось '
                f'{now_cash_currency} {currency_name}')
