import tkinter as tk
from tkinter import simpledialog
from datetime import date
from dateutil.relativedelta import relativedelta


ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askinteger(title="Historical Air Quality Data Collection",
                                  prompt="How many days historical data do you want?:")

yesterday = date.today() + relativedelta(days=-1)
yesterday_day = yesterday.strftime("%d")
yesterday_month = yesterday.strftime("%b")
yesterday_year = yesterday.strftime("%Y")
yesterday = yesterday_day + "+" + yesterday_month + "+" + yesterday_year

user_date = date.today() + relativedelta(days=-USER_INP)
user_date_day = user_date.strftime("%d")
user_date_month = user_date.strftime("%b")
user_date_year = user_date.strftime("%Y")
user_date = user_date_day + "+" + user_date_month + "+" + user_date_year

URL = ('https://airquality.ie/readings?station=' + "EPA-25" + '&dateFrom=09+Mar+2022&dateTo=10+Mar+2022')
URL1 = ('https://airquality.ie/readings?station=' + "EPA-25" + '&dateFrom=' + user_date + '&dateTo=' + yesterday)

# check it out
print("You requested", USER_INP, "days.")
print(URL)
print(URL1)

