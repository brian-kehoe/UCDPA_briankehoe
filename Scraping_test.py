import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from os.path import getmtime
import os

aq_raw_data_csv_exists = os.path.exists('aq_raw_data.csv')
print("Aq_raw_data_csv_exists = " + str(aq_raw_data_csv_exists))

if aq_raw_data_csv_exists == False:
    URL = "https://airquality.ie/assets/php/get-monitors.php"
    headers = {"Referer": "https://airquality.ie/assets/php"}
    aq_data_txt = requests.get(URL, headers=headers).text
    df_aq_raw_data = pd.read_json(aq_data_txt)
    df_aq_raw_data.to_csv('aq_raw_data.csv')
    df_aq_raw_data.to_pickle('aq_raw_data.pkl')

else:
    csv_timestamp = datetime.fromtimestamp(getmtime('aq_raw_data.csv'))
    now = datetime.now()
    csv_age = now - csv_timestamp

    if csv_age.seconds > 3:
        csv_stale = True
        print("CSV Stale = " + str(csv_stale))
        URL = "https://airquality.ie/assets/php/get-monitors.php"
        headers = {"Referer": "https://airquality.ie/assets/php"}
        aq_data_txt = requests.get(URL, headers=headers).text
        df_aq_raw_data = pd.read_json(aq_data_txt)
        df_aq_raw_data.to_csv('aq_raw_data.csv')
        df_aq_raw_data.to_pickle('aq_raw_data.pkl')
    else:
        print("CSV Stale = False")


df_aq_data = pd.read_csv('aq_raw_data.csv', usecols=['monitor_id', 'label', 'location', 'latitude', 'longitude',
                                                     'latest_reading'])
df_aq_data_pickle = pd.read_pickle('aq_raw_data.pkl')
np_aq_data = np.array(df_aq_data)

print("aq_data_txt = " + str(type(aq_data_txt)))
print("df_aq_raw_data = " + str(type(df_aq_raw_data)))
print("df_aq_raw_data['latest_reading'] = " + str(type(df_aq_raw_data['latest_reading'])))
print(df_aq_raw_data['latest_reading'][0])
print("df_aq_raw_data['latest_reading'][0] = " + str(type(df_aq_raw_data['latest_reading'][0])))

print("df_aq_data['latest_reading'] = " + str(type(df_aq_data['latest_reading'])))
print(df_aq_data['latest_reading'][0])
print("df_aq_data['latest_reading'][0] = " + str(type(df_aq_data['latest_reading'][0])))

print("df_aq_data_pickle['latest_reading'] = " + str(type(df_aq_data_pickle['latest_reading'])))
print(df_aq_data_pickle['latest_reading'][0])
print("df_aq_data_pickle['latest_reading'][0] = " + str(type(df_aq_data_pickle['latest_reading'][0])))

#print(df_aq_data[df_aq_data['latest_reading'].iloc[:6]])

#print(df_aq_data['latest_reading'][0][2:5])

#print('\nValues in this Array     : ', df_aq_data['latest_reading'].values)
#print('Index Values of this Array : ', df_aq_data['latest_reading'].index)
#print(df_aq_data['latest_reading'])

#print(df_aq_data[df_aq_data['latest_reading']])
#print(df_aq_data.dropna()[df_aq_data.dropna()['latest_reading'].str.contains('pm2_5')])
#print(df_aq_data['label'])
#print(df_aq_data[['location', 'latest_reading']])
#print(np_aq_data)


