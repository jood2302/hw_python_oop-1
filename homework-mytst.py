# Project: Sprint 2. Calculator calories/money (four classes). Yandex.Praktikum.Python developer.
# Author: Vasiliy Kovylin. Backend, Cohort 16, Student.
#
# Description:
# Need make four classes for two calculators: 
# Class Record
# Class Calculator
# Class CaloriesCalculator
# Class CashCalculator
#
# Methods for Record:                 # first brick in the wall...
# no methods, only data

#
# Methods for Calculator:             # Parent for CaloriesCalculator and CashCalculator, or for another simplest calculators
# add_record()
# get_today_stats()
# get_week_stats()
#
# Methods for CaloriesCalculator:     # Child of Calculator wiht own new method get_calories_remained()
# get_calories_remained()
#
# Methods for CashCalculator:         # Child of Calculator wiht own new method get_today_cash_remained(currency)
# get_today_cash_remained(currency)    



import datetime as dt
#from datetime import datetime, date
#from typing import List

LOCAL_DATE_FORMAT: str = '%d.%m.%Y'
LOCAL_USD_RATE: float = 73.91
LOCAL_EUR_RATE: float = 87.94


class Record:
    """ is object of 3 values: 'amount', 'comment' and 'date'

    """

    def __init__ (self, amount: float, comment: str, date: str = None) -> None: 
        """ Needs 3 named values: 'amount', 'comment' and 'date'
            In call of this, value 'date' may be skipped
            In this case, in the value 'date' should be written the value of current day.

        """
        self.amount: float = amount
        self.comment: str = comment
        
        if date is None:
            self.date: dt.date = dt.datetime.now()
        else:
            self.date: dt.date = dt.datetime.strptime(date, LOCAL_DATE_FORMAT)


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
        today: dt.datetime = dt.datetime.now()
        today_sum: float = 0
        for rec in self.records:
            if rec.date == today:
                today_sum += rec.amount
        return today_sum
        
    def get_week_stats(self) -> float:
        """ calculates sum of field 'amount' in self list 'records' for current date
            and six days ago
        """
        today: dt.datetime = dt.datetime.now()
        #week_ago: dt.datetime = 
        week_sum: float = 0
        for rec in self.records:
            if rec.date > today - dt.timedelta(days=6) and rec.date <= today:
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
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {is_over} кКал'
        else:
            return f'Хватит есть!'

class CashCalculator(Calculator):
    """ Child class of 'Calculator'. All of this included.
        Added new own method

    """
    def get_today_cash_remained(self, currency: str) -> str :  # принимает три значения "rub", "usd" или "eur"
        """ From call wait 1 of 3 currency name, calculates balance and 
            return message with the value in the recalculated form.        

        """
        usd_rate: float = LOCAL_USD_RATE
        eur_rate: float = LOCAL_EUR_RATE
        now_cash: float = self.limit - self.get_today_stats()

        if currency == 'usd':
            multiplier: float = 1 / usd_rate
            currency_name: str = 'USD'
        elif currency == 'eur':
            multiplier: float = 1 / eur_rate
            currency_name: str = 'Euro'
        else:
            multiplier: float = 1
            currency_name: str = 'руб'

        if now_cash == 0:
            return f'Денег нет, держись'

        elif now_cash < 0:
            now_cash *= -1
            return f'Денег нет, держись: твой долг - {now_cash *  multiplier} {currency_name}'
        else:
            return f'На сегодня осталось {now_cash *  multiplier} {currency_name}'
        
        
        # для CashCalculator 
r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='09.03.2019')
r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

# для CaloriesCalculator
r4 = Record(amount=1186,
            comment='Кусок тортика. И ещё один.',
            date='24.02.2019')
r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
r6 = Record(amount=1140, comment='Баночка чипсов.', date='24.02.2019') 


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб 