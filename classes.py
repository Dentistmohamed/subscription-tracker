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
        cursor.execute(f"SELECT service, amount, link, REPLACE(date, '-', '/'), id FROM Services WHERE strftime('%m', date) = '{this_month}' ORDER BY date")
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

class Service(Dates):
    def __init__(self, name=None, amount=None, link=None, date=None, service_id=None):
        super().__init__()
        self.name = name
        self.amount = amount
        self.link = link
        self.date = date
        self.service_id = service_id
    
    def __str__(self):
        return f"{self.service_id}"

    def insert_service(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO Services (Service, amount, link, date) VALUES ('{self.name}', {self.amount}, '{self.link}', '{self.date}')")
        con.commit()
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, val):
        self._name = val.replace("'", "''")
    
    def update_service(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()        
        cursor.execute(f"UPDATE Services SET service = '{self.name}', amount = {self.amount}, link = '{self.link}', date = '{self.date}' WHERE id = {self.service_id}")
        con.commit()
    def delete_service(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(f"DELETE FROM Services WHERE id = {self.service_id}")
        con.commit()
