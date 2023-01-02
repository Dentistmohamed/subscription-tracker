from flask import Flask, session, sessions, render_template, redirect, request
from flask_session import Session
from datetime import datetime
import sqlite3
from datetime import date, datetime
import calendar

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["TESTING"] = True
app.config["SECRET_KEY"] = 'c5b57a27320248889d3f893a1529c4bf'
app.config["FLASK_ENV"] = "development"
Session(app)

today = date.today()

@app.route("/", methods=["GET"])
def main():
    today = date.today()
    show_month = str(today).split('-')[0][2:]
    month_name = calendar.month_name[int(str(today).split("-")[1])]
    target_date_db = str(today).split("-")[1]
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM services where strftime('%m', date) = '{target_date_db}'")
    services = cursor.fetchall()
    update_services = []
    if len(services) > 0:
        for service in services:
            show_date = str(service[4]).split("-")
            show_date = f"{show_date[-1]}/{show_date[1]}/{show_date[0][2:]}"
            future = str(service[4]).split('-')
            future = date(int(future[0]),int(future[1]),int(future[2]))
            service1 = service + (str(future - today).replace(', 0:00:00', ''), show_date,)
            update_services.append(service1)

    cursor.execute(f"select sum(amount) from services where strftime('%m', date) = '{target_date_db}'")
    total_amount = cursor.fetchall()
    if len(total_amount) > 0:
        total_amount = total_amount[0][0]
    
    return render_template("index.html", services=update_services, total=total_amount, date=today, month=month_name, year=show_month)


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



