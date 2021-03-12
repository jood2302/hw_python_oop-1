"""Project: Sprint 2. Calculator calories/money (four classes).

   Class Record
   Class Calculator
   Class CaloriesCalculator
   Class CashCalculator
"""

import datetime as dt
from typing import List, Optional

LOCAL_DATE_FORMAT: str = '%d.%m.%Y'


class Record:
    """is object of 3 values: 'amount', 'comment' and 'date'"""

    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None) -> None:
        """Needs 3 named values: 'amount', 'comment' and 'date'
            In call of this, value 'date' may be skipped
            In this case, in the value 'date' should be
            written the value of current day."""
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
        """Value "limit" - day limit for proper functioning own methods"""
        self.limit: int = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        """calculates sum of field 'amount' in self list 'records'
           for current date"""

        return self.get_day_stats(dt.date.today())
        """today_sum: float = 0
        for rec in self.records:
            if rec.date == today:
                today_sum += rec.amount
        return today_sum"""

    def get_week_stats(self) -> float:
        """calculates sum of field 'amount' in self list 'records' for current date
           and six days ago"""
        today: dt.date = dt.date.today()
        delta_time: dt.date = dt.timedelta(days=1)
        tmp_list: List = []
        for x in range(7):
            delta_time: dt.date = dt.timedelta(days=x)
            tmp_list.append(self.get_day_stats(today - delta_time))            
        return sum(v for v in tmp_list)

    def today_balance(self, date: dt.date) -> float:
        return self.limit - self.get_today_stats()

    def get_day_stats(self, date: dt.date) -> float:
        tmp_list: List = [x.amount for x in self.records if x.date == date]
        return sum(v for v in tmp_list)


class CaloriesCalculator(Calculator):
    """Child class of 'Calculator'. All of this included.
       Added new own method get_calories_remained()"""

    def get_calories_remained(self) -> str:
        """Calculates difference between today_stats and day_limit
           and print first or second message for user"""

        overhead: float = self.today_balance(dt.date.today())
        if overhead > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {overhead} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Child class of 'Calculator'. All of this included.
        Added new own method get_today_cash_remained()"""

    EURO_RATE: float = 87.94
    USD_RATE: float = 73.91

    def get_today_cash_remained(self, currency: str) -> str:
        """From call wait currency name, calculates balance and
           return message with the value in the recalculated form."""
        EURO_RATE: float = 87.94
        USD_RATE: float = 73.91
        RUB_RATE: float = 1.0

        self.currency_attrib: dict = {'rub': 'руб', 'eur': 'Euro',
                                      'usd': 'USD'}
        self.currency_rate: dict = {'rub': RUB_RATE, 'eur': EURO_RATE,
                                    'usd': USD_RATE}

        now_cash: float = self.get_today_stats()

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
                

if __name__ == "__main__":

    """print('date')
    date='08.03.2019'
    print(dt.datetime.strptime(date, LOCAL_DATE_FORMAT))

    #datedate = dt.date.fromisoformat(dt.datetime.strptime(date, LOCAL_DATE_FORMAT))
    datedate = dt.datetime.date(dt.datetime.strptime(date, LOCAL_DATE_FORMAT))
    print(type(datedate))
    print(f'{dt.datetime.date(dt.datetime.strptime(date, LOCAL_DATE_FORMAT))}')"""





    # для CashCalculator 
    r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
    r2 = Record(amount=1568, comment='Наполнение потребительской корзины', date='09.03.2019')
    r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

    # для CaloriesCalculator
    r4 = Record(amount=1186, comment='Кусок тортика. И ещё один.', date='24.02.2019')
    r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
    r6 = Record(amount=1140, comment='Баночка чипсов.', date='24.02.2019') 


    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000, comment='бар в Танин др', date='08.11.2019'))

    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # На сегодня осталось 555 руб 


    """print(cash_calculator.EURO_RATE)
    print(cash_calculator.USD_RATE)
    print(cash_calculator.currency_attrib)
    print(cash_calculator.currency_rate)

    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('eur'))"""


    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)
    
    date='08.11.2019'
    # cash_calculator.get_day_stats('08.11.2019')
    for i in cash_calculator.records:
        print()
