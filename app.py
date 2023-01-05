from flask import Flask, session, sessions, render_template, redirect, request
from flask_session import Session
from datetime import datetime
import sqlite3
from datetime import date, datetime
import calendar
from classes import * 

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["TESTING"] = True

app.config["FLASK_ENV"] = "development"
Session(app)

today = date.today()

@app.route("/", methods=["GET"])
def main():
    Database()
    dates = Dates()
    today = dates.get_day()
    month = dates.get_month()
    year = dates.get_year()
    try:
        show_table = dates.show_table()
    except IndexError:
        show_table = [(None, )]
    upcoming_subscriptions = dates.show_later_table()
    total_amount = dates.total_subscriptions_values()[0][0]
    total_later_dates = dates.total_later_months_subscriptions()[0]
    return render_template("index.html", services=show_table,  total=total_amount, date=today, month=month, year=year, upcoming=upcoming_subscriptions, total_later = total_later_dates)


@app.route("/add", methods=["POST"])
def add():
    service = request.form.get("service")
    amount = request.form.get("amount")
    link = request.form.get("link")
    renewal_date = request.form.get("date")
    service = Service(service, amount, link, renewal_date)
    service.insert_service()
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    service_name = request.form.get("service")
    oldservice = request.form.get("oldservice")
    amount = request.form.get("amount")
    link = request.form.get("link")
    date0 = request.form.get("date")
    service = Service(service_name, amount, link, date0, oldservice)
    if 'delete' in request.form:
        service.delete_service()
    else:
        service.update_service()
    return redirect("/")