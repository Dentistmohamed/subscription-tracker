from flask import current_app
from datetime import date, datetime
import sqlite3
import calendar

class Dates:
    # init class with today date
    def __init__(self):
        self.today = date.today()


    def __str__(self):
        return f"{self.today}"
    
    def month_number(self):
        month_number = int(str(self.today).split("-")[1])
        return month_number

    # get today date
    def get_day(self):
        return self.today
    # get current month
    def get_month(self):
        month = calendar.month_name[self.month_number()]
        return month

    # get current year
    def get_year(self):
        year = str(self.today).split("-")[0]
        return year[2:]

    # search for all subscriptions
    def show_subscriptions(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()

        # add leading zero for month to search in db
        this_month  = str(self.month_number()).zfill(2)

        # search in db for subscriptions ends this month
        cursor.execute(f"SELECT service, amount, link, REPLACE(date, '-', '/') FROM Services WHERE strftime('%m', date) = '{this_month}' ORDER BY date")
        results = cursor.fetchall()
        if len(results) < 1:
            raise IndexError("No subscriptions were found")
        return results
    
    def show_table(self):
        found_subscriptions = self.show_subscriptions()
        subscriptions_list = []
        for service in found_subscriptions:
            renewal_date = datetime.strptime(service[3], "%Y/%m/%d").date()
            remaining_days = abs((renewal_date - self.today).days)
            new_column = service + (remaining_days,)
            subscriptions_list.append(new_column)
        return subscriptions_list

    @staticmethod
    def add_leading_zero(value):
        new_value = str(value).zfill(2)
        return new_value
    
    def total_subscriptions_values(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(f"SELECT SUM(amount) FROM Services WHERE strftime('%m', date) = '{self.add_leading_zero(self.month_number())}'")
        total_amount = cursor.fetchall()
        if not total_amount[0][0]:
            total_amount = [('0', )]
        return total_amount

