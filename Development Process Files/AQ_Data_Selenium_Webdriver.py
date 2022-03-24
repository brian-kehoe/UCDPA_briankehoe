from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd

#Set column names and create empty dataframe
column_names = ['Date and Time', 'PM10', 'PM2.5', 'SO2', 'Site']
df = pd.DataFrame(columns=column_names)
#print(df)

chromedriver = "chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.set_window_size(1200, 700)

print("New Chrome window will open automatically for data import")

#Load initial page
driver.get('https://airquality.ie/readings?station=EPA-25&dateFrom=01+Feb+2022&dateTo=02+Feb+2022')
print("Opened airquality.ie")
time.sleep(1)    #Just wait for sometime.

#Accept Cookies
print("Accept Cookies")
wait = WebDriverWait(driver, 1)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="cc-btn cc-allow"]')))
driver.find_element_by_xpath('//*[@class="cc-btn cc-allow"]').click()

#EPA monitoring sites
sites = ("EPA-54", "EPA-78", "EPA-25", "TNO3947", "EPA-60", "EPA-30", "EPA-72", "EPA-104", "EPA-10", "EPA-67", "EPA-82",
         "EPA-56", "EPA-21", "TNO3955", "EPA-64", "EPA-27", "TNO2579-EPA", "EPA-50", "TNT1296-EPA", "EPA-29", "EPA-33",
         "TNO4435-EPA", "TNO4323-EPA", "EPA-49", "TNO4158", "TNO4325-EPA", "EPA-55", "EPA-76", "EPA-34", "EPA-46",
         "TNO4324-EPA", "EPA-47", "EPA-69", "EPA-48", "EPA-17", "EPA-22", "TNO2162-EPA", "EPA-52", "EPA-57", "EPA-61",
         "EPA-44", "TNO2161-EPA", "TNT1088-EPA", "TNO4436-EPA", "EPA-11", "EPA-105", "EPA-51", "TNO4467", "EPA-71",
         "EPA-45", "TNO4160", "EPA-83", "TNO3953", "EPA-36", "TNO4157", "EPA-62", "TNO3954", "EPA-16", "EPA-80",
         "TNO3951", "EPA-74", "TNO3840", "EPA-85", "TNO3841", "TNO3839", "EPA-39", "EPA-43", "EPA-84", "EPA-23",
         "TNO4468", "EPA-26", "EPA-103", "EPA-68", "EPA-58", "TNO3952", "TNO4465", "EPA-79", "EPA-102", "TNO3948",
         "EPA-53", "EPA-77", "EPA-75", "A-TNO3957", "EPA-66", "EPA-59", "TNO3946", "EPA-70", "TNO4159", "EPA-28",
         "EPA-24", "TNT1677", "TNT1516", "TNT1506", "TNT1505", "EPA-63", "EPA-13", "EPA-101")

#sites = ('EPA-25', 'EPA-55')

sites_count = len(sites)
print("Collecting data from " + str(sites_count) + " sites")

progress = 0

#For loop - Open each site URL
for i in sites:
    URL = ('https://airquality.ie/readings?station=' + i + '&dateFrom=01+Sep+2021&dateTo=19+Feb+2022')
    driver.get(URL)
    print("Opened " + URL)
    time.sleep(2)    #Just wait for sometime.

    #Error handling - No data
    if driver.find_elements_by_xpath("//div[@class='alert fade show g-bg-red-opacity-0_1 g-color-lightred rounded-0 g-mt-10']"):
        print("No Data")
    #Expand highcharts hamburger button
    else:
        button_box = driver.find_element_by_class_name("highcharts-button-symbol")
        button_box.click()
        #Click "View data table"
        for download in driver.find_elements_by_xpath("//li[@class='highcharts-menu-item']"):
            if download.text == "View data table":
                download.click()

        #Read HTML table into dataframe
        df_loop_read = pd.read_html(driver.page_source)[0]

        #print('driver.page_source')
        #print(df_loop_read)

        #Add 'Date and Time' column to df_loop
        df_loop = df_loop_read[['Date and Time']]

        #Add 'PM10', 'PM2.5' and 'SO2' to df_loop if they are present, otherwise add no data
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

        #print('Copy 4 columns')
        #print(df_loop)

        #Add 'Site' value to df_loop
        df_loop["Site"] = i

        #print('Add Site column')
        #print(df_loop)

        #Add df_loop data to df_loop
        df = pd.concat([df, df_loop], axis=0)
        #print('Concatenated df')
        #df.to_csv('aq_concatenated_df_test_loop.csv')
        #print(df.head())
        with pd.option_context('display.max_rows', 10):
            print(df)

        progress = progress + 1
        percent = (progress / sites_count) * 100
        print("Collected data from " + str(progress) + " of " + str(sites_count) + " sites. " + str(
            round(percent, 1)) + "% Complete")

print('After loop - Print df')
df.to_csv('aq_concatenated_df.csv')
print(df)
