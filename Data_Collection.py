import pandas as pd
import requests
from datetime import datetime
from os.path import getmtime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import tkinter as tk
from tkinter import simpledialog
from datetime import date
from dateutil.relativedelta import relativedelta


print()
print("Beginning current data import process")


# Define function to retrieve data from Airquality.ie website
# Function will set the Referer in the headers to allow the data to be accessed
# Normalise raw JSON data
# Normalise 'latest_reading' dictionary data
# Merge both dataframes
# Save combined dataframe to CSV
def get_data():
    url = "https://airquality.ie/assets/php/get-monitors.php"
    headers = {"Referer": "https://airquality.ie/assets/php"}
    aq_current_raw_data = pd.read_json(requests.get(url, headers=headers).text)
    aq_current_latest_reading = pd.json_normalize(aq_current_raw_data['latest_reading'])
    aq_current_data = pd.merge(aq_current_raw_data, aq_current_latest_reading, left_on='monitor_id', right_on='monitor_id')
    aq_current_data.to_csv('aq_current_data.csv')


# Check to see if 'aq_raw_data.csv' exists
aq_current_data_exists = os.path.exists('aq_current_data.csv')
print("")
print("CSV exists = " + str(aq_current_data_exists))

# If 'aq_raw_data.csv' does not exist, get data using requests
if not aq_current_data_exists:
    get_data()
    print("Retrieving current air quality data...")
# Else if 'aq_raw_data.csv' does exist, check the age of the file
else:
    csv_age = datetime.now() - datetime.fromtimestamp(getmtime('aq_current_data.csv'))
    # If 'aq_raw_data.csv' is more than 1 hour old, get data using get_data function
    if csv_age.seconds > 3600:
        csv_stale = True
        print("CSV stale = " + str(csv_stale))
        get_data()
        print("Retrieving current air quality data...")
    # Else print "CSV Stale = False"
    else:
        print("CSV stale = False")


print()
print("Finished collecting current air quality data")


# Historic data collection - Selenium Webdriver/Chromedriver
print()
print()
print("Beginning historic data collection process")


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


# Load aq_current_valid_sites.csv and get the site codes
current_valid_sites = pd.read_csv('aq_current_valid_sites.csv')
sites = current_valid_sites["code"]
sites_count = len(sites)  # Count number of sites

# Set column names and create empty dataframe
column_names = ['Date and Time', 'PM10', 'PM2.5', 'SO2', 'Site']
aq_historical_data = pd.DataFrame(columns=column_names)


print()
print("New chromedriver window will open automatically for data import")
print()


# Configure chromedriver
chromedriver = "chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.set_window_size(1200, 700)


# Load initial page
driver.get('https://airquality.ie/readings?station=' + "EPA-25" + '&dateFrom=' + yesterday + '&dateTo=' + yesterday)
# driver.get('https://airquality.ie/readings?station=EPA-25&dateFrom=01+Feb+2022&dateTo=02+Feb+2022')
print("Opened airquality.ie")
time.sleep(1)  # Wait 1 second

# Accept Cookies
print("Accept Cookies")
print()
wait = WebDriverWait(driver, 1)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="cc-btn cc-allow"]')))
driver.find_element_by_xpath('//*[@class="cc-btn cc-allow"]').click()


print("Begin collecting data from " + str(sites_count) + " sites")
# Initialise progress counter
progress = 0

# For loop - Open each site URL
for i in sites:
    URL = ('https://airquality.ie/readings?station=' + i + '&dateFrom=' + user_date + '&dateTo=' + yesterday)
    # URL = ('https://airquality.ie/readings?station=' + i + '&dateFrom=09+Mar+2022&dateTo=10+Mar+2022')
    # URL = ('https://airquality.ie/readings?station=' + i + '&dateFrom=01+Sep+2021&dateTo=28+Feb+2022')
    driver.get(URL)
    print("Opened " + URL)
    print("Retrieving data...")
    time.sleep(1)  # Wait 2 seconds

    # Error handling - No data
    if driver.find_elements_by_xpath("//div[@class='alert fade show g-bg-red-opacity-0_1 g-color-lightred rounded-0 g-mt-10']"):
        print("No data for site")
    else:
        hamburger_button = driver.find_element_by_class_name("highcharts-button-symbol")
        hamburger_button.click()  # Click highcharts hamburger button
        for menu_item in driver.find_elements_by_xpath("//li[@class='highcharts-menu-item']"):
            if menu_item.text == "View data table":
                menu_item.click()  # Click "View data table"

        df_loop_read = pd.read_html(driver.page_source)[0]  # Read HTML table into dataframe
        df_loop = df_loop_read[['Date and Time']]  # Add 'Date and Time' column to df_loop

        # Add 'PM10', 'PM2.5' and 'SO2' to df_loop if they are present, otherwise add no data
        if 'PM10' not in df_loop_read:
            df_loop['PM10'] = None
        else:
            df_loop = pd.concat([df_loop, df_loop_read[['PM10']]], axis=1)

        if 'PM2.5' not in df_loop_read:
            df_loop['PM2.5'] = None
        else:
            df_loop = pd.concat([df_loop, df_loop_read[['PM2.5']]], axis=1)

        if 'SO2' not in df_loop_read:
            df_loop['SO2'] = None
        else:
            df_loop = pd.concat([df_loop, df_loop_read[['SO2']]], axis=1)

        df_loop["Site"] = i  # Add 'Site' value to df_loop
        aq_historical_data = pd.concat([aq_historical_data, df_loop], axis=0)  # Add df_loop data to df

        # Print first and last 5 rows of updated dataframe
        with pd.option_context('display.max_rows', 10):
            print(aq_historical_data)

        progress = progress + 1  # Increment progress
        percent = (progress / sites_count) * 100  # Calculate progress %
        # Print progress
        print("Collected data from " + str(progress) + " of " + str(sites_count) + " sites. " + str(
            round(percent, 1)) + "% Complete")
        print("")

print('Finished collection historical air quality data')
aq_historical_data.to_csv('aq_historical_data.csv')

# Close chromedriver window
driver.quit()


