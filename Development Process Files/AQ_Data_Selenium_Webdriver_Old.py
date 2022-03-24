from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd

column_names = ['Date and Time', 'SO2', 'PM10', 'PM2.5', 'Site']
df = pd.DataFrame(columns=column_names)
print(df)

chromedriver = "chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.set_window_size(1200, 700)

print("New Chrome window will open automatically for data import")

driver.get('https://airquality.ie/readings?station=EPA-25&dateFrom=01+Nov+2021&dateTo=31+Dec+2021')
print("Opened airquality.ie")
time.sleep(4)    #Just wait for sometime.

wait = WebDriverWait(driver, 1)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="cc-btn cc-allow"]')))
driver.find_element_by_xpath('//*[@class="cc-btn cc-allow"]').click()

# "EPA-54" ,"EPA-78" ,"EPA-25" ,"TNO3947" ,"EPA-60" ,"EPA-30" ,"EPA-72" ,"EPA-104" ,"EPA-10" ,"EPA-67" ,"EPA-82" ,\
# "EPA-56" ,"EPA-21" ,"TNO3955" ,"EPA-64" ,"EPA-27" ,"TNO2579-EPA" ,"EPA-50" ,"TNT1296-EPA" ,"EPA-29" ,"EPA-33" ,\
# "TNO4435-EPA" ,"TNO4323-EPA" ,"EPA-49" ,"TNO4158" ,"TNO4325-EPA" ,"EPA-55" ,"EPA-76" ,"EPA-34" ,"EPA-46" ,\
# "TNO4324-EPA" ,"EPA-47" ,"EPA-69" ,"EPA-48" ,"EPA-17" ,"EPA-22" ,"TNO2162-EPA" ,"EPA-52" ,"EPA-57" ,"EPA-61" ,\
# "EPA-44" ,"TNO2161-EPA" ,"TNT1088-EPA" ,"TNO4436-EPA" ,"EPA-11" ,"EPA-105" ,"EPA-51" ,"TNO4467" ,"EPA-71" ,\
# "EPA-45" ,"TNO4160" ,"EPA-83" ,"TNO3953" ,"EPA-36" ,"TNO4157" ,"EPA-62" ,"TNO3954" ,"EPA-16" ,"EPA-80" ,"TNO3951" ,\
# "EPA-74" ,"TNO3840" ,"EPA-85" ,"TNO3841" ,"TNO3839" ,"EPA-39" ,"EPA-43" ,"EPA-84" ,"EPA-23" ,"TNO4468" ,"EPA-26" ,\
# "EPA-103" ,"EPA-68" ,"EPA-58" ,"TNO3952" ,"TNO4465" ,"EPA-79" ,"EPA-102" ,"TNO3948" ,"EPA-53" ,"EPA-77" ,"EPA-75" ,\
# "A-TNO3957" ,"EPA-66" ,"EPA-59" ,"TNO3946" ,"EPA-70" ,"TNO4159" ,"EPA-28" ,"EPA-24" ,"TNT1677" ,"TNT1516" ,"TNT1506" ,\
# "TNT1505" ,"EPA-63" ,"EPA-13" ,"EPA-101"

sites = ("EPA-54", "EPA-78")

print("Opened airquality.ie - site")
URL = ('https://airquality.ie/readings?station='+'EPA-25'+'&dateFrom=01+Nov+2021&dateTo=31+Dec+2021')
print(URL)
driver.get(URL)
#driver.get('https://airquality.ie/readings?station=EPA-25&dateFrom=01+Nov+2021&dateTo=31+Dec+2021')
print("Opened airquality.ie")
time.sleep(5)    #Just wait for sometime.

button_box = driver.find_element_by_class_name("highcharts-button-symbol")
button_box.click()

for download in driver.find_elements_by_xpath("//li[@class='highcharts-menu-item']"):
    if download.text == "View data table":
        download.click()

df_EPA25 = pd.read_html(driver.page_source)[0]
print('driver.page_source')
print(df_EPA25)
df_EPA25 = df_EPA25[['Date and Time', 'SO2', 'PM10', 'PM2.5']]
print('Copy 4 columns')
print(df_EPA25)
df_EPA25["Site"] = 'EPA-25'
print('Add Site column')
print(df_EPA25)

df = pd.concat([df, df_EPA25], axis=0)
print('Concatenated df')
print(df)

print("Opening new airquality.ie page")
driver.get('https://airquality.ie/readings?station=EPA-55&dateFrom=01+Nov+2021&dateTo=31+Dec+2021')
time.sleep(5)    #Just wait for sometime.
print("Opened new airquality.ie page")

button_box = driver.find_element_by_class_name("highcharts-button-symbol")
button_box.click()

for download in driver.find_elements_by_xpath("//li[@class='highcharts-menu-item']"):
    if download.text == "View data table":
        download.click()

df_EPA55 = pd.read_html(driver.page_source)[0]
print('driver.page_source')
print(df_EPA55)
df_EPA55 = df_EPA55[['Date and Time', 'SO2', 'PM10', 'PM2.5']]
print('Copy 4 columns')
print(df_EPA55)
df_EPA55["Site"] = 'EPA-55'
print('Add Site column')
print(df_EPA55)

df = pd.concat([df, df_EPA55], axis=0)
df.to_csv('aq_concatenated_df.csv')
print('Concatenated df')
print(df)

# button_box = driver.find_element_by_class_name("highcharts-button-symbol")
# button_box.click()
#
# for download in driver.find_elements_by_xpath("//li[@class='highcharts-menu-item']"):
#     if download.text == "Download CSV":
#         download.click()

#"highcharts-menu-item" style="cursor: pointer; View data table
# highcharts-menu-item" style="cursor: pointer;  #View data table
# highcharts-menu-item" style="cursor: pointer; #Download CSV