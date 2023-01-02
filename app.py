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
    dates = Dates()
    today = dates.get_day()
    month = dates.get_month()
    year = dates.get_year()
    try:
        show_table = dates.show_table()
    except IndexError:
        show_table = [(None, )]
    total_amount = dates.total_subscriptions_values()[0][0]
    
    return render_template("index.html", services=show_table,  total=total_amount, date=today, month=month, year=year)


@app.route("/add", methods=["POST"])
def add():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    today = date.today()
    service = request.form.get("service")
    service = service.replace("'", "''")
    amount = request.form.get("amount")
    link = request.form.get("link")
    link = link.replace("'", "''")
    date1 = request.form.get("date")
    if not date1:
        date1 = today
    cursor.execute(f"INSERT OR IGNORE INTO services (service, amount, link, date) values ('{service}', '{amount}', '{link}', '{date1}')")
    con.commit()
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    today = date.today()
    service = request.form.get("service")
    service = service.replace("'", "''")
    oldservice = request.form.get("oldservice")
    amount = request.form.get("amount")
    link = request.form.get("link")
    link = link.replace("'", "''")
    date1 = request.form.get("date")
    if not date1:
        date1 = today
    if 'edit' in request.form:
        cursor.execute(f"update services set service = '{service}', amount = '{amount}', link = '{link}', date = '{date1}' where service = '{oldservice}'")
    elif 'delete' in request.form:
        cursor.execute(f"delete from services where service = '{oldservice}'")
    con.commit()
    return redirect("/")