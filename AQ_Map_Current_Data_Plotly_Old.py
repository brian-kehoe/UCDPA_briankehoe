import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from os.path import getmtime
import os
import json
import matplotlib.pyplot as plt
import plotly.express as px

#Check to see if 'aq_raw_data.csv' exists
aq_raw_data_csv_exists = os.path.exists('aq_raw_data.csv')
print("Aq_raw_data_csv_exists = " + str(aq_raw_data_csv_exists))

#If 'aq_raw_data.csv' does not exist, get data using requests
if aq_raw_data_csv_exists == False:
    URL = "https://airquality.ie/assets/php/get-monitors.php"
    headers = {"Referer": "https://airquality.ie/assets/php"}
    aq_data_txt = requests.get(URL, headers=headers).text
    df_aq_raw_data = pd.read_json(aq_data_txt)
    df_aq_raw_data.to_csv('aq_raw_data.csv')
    df_aq_raw_data.to_pickle('aq_raw_data.pkl')

# Else if 'aq_raw_data.csv' does exist, check the age of the file
else:
    csv_timestamp = datetime.fromtimestamp(getmtime('aq_raw_data.csv'))
    now = datetime.now()
    csv_age = now - csv_timestamp

    #If 'aq_raw_data.csv' is more than 1 hour old, get data using requests
    if csv_age.seconds > 3600:
        csv_stale = True
        print("CSV Stale = " + str(csv_stale))
        URL = "https://airquality.ie/assets/php/get-monitors.php"
        headers = {"Referer": "https://airquality.ie/assets/php"}
        aq_data_txt = requests.get(URL, headers=headers).text
        df_aq_raw_data = pd.read_json(aq_data_txt)
        df_aq_raw_data.to_csv('aq_raw_data.csv')
        df_aq_raw_data.to_pickle('aq_raw_data.pkl')
    # Else print "CSV Stale = False"
    else:
        print("CSV Stale = False")


df_aq_data = pd.read_pickle('aq_raw_data.pkl')
# np_aq_data = np.array(df_aq_data)
#
# print("")
print("df_aq_data = " + str(type(df_aq_data)))
print(df_aq_data)
# print("")
# print("df_aq_data['latest_reading'] = " + str(type(df_aq_data['latest_reading'])))
# #print(df_aq_data['latest_reading'])
# print("")
# print("df_aq_data['latest_reading'][0] = " + str(type(df_aq_data['latest_reading'][0])))
# print(df_aq_data['latest_reading'][0:96])
# print("")
# print("df_aq_data['latest_reading'][0]['monitor_id'] = " + str(type(df_aq_data['latest_reading'][0]['monitor_id'])))
# print(df_aq_data['latest_reading'][1]['monitor_id'])
# print("")
# print("df_aq_data['latest_reading'][0]['pm2_5'] = " + str(type(df_aq_data['latest_reading'][0]['pm2_5'])))
# print(df_aq_data['latest_reading'][1]['pm10'])

latest_readings = pd.DataFrame(df_aq_data['latest_reading'][0:96])
#print(type(latest_readings))
#print(latest_readings.shape)
print("latest_reading.head()")
print(latest_readings.head())

json_struct = json.loads(latest_readings.to_json(orient="records"))
print("json_struct")
print(json_struct)

df_flat = pd.json_normalize(json_struct)
print("df_flat")
print(df_flat)

print(df_flat[['latest_reading.monitor_id', 'latest_reading.pm2_5']])
print("")

df_flat.sort_values(by=['latest_reading.pm2_5'], inplace=True)
print(df_flat[['latest_reading.monitor_id', 'latest_reading.pm2_5']])
print("")

df_aq_combined = pd.merge(df_aq_data, df_flat, left_on='monitor_id', right_on='latest_reading.monitor_id')
print("df_aq_combined.info()")
print(df_aq_combined.info())
print("")

df_aq_combined_filtered = df_aq_combined[(df_aq_combined['latest_reading.status'] != 'red')
                                         & (df_aq_combined['latest_reading.pm2_5'].notnull())]
print("df_aq_combined_filtered.info()")
print(df_aq_combined_filtered.info())
print("")

print("df_aq_combined[['label', 'latest_reading.pm2_5']]")
print(df_aq_combined_filtered[['label', 'latest_reading.pm2_5']])
print("")

df_aq_combined_filtered.sort_values(by=['latest_reading.pm2_5'], inplace=True, ascending=False)
print(df_aq_combined_filtered[['location', 'latest_reading.pm2_5']])

# Create filtered list for 'cities_lat_lon_aq_data_auto.csv'
df_cities_lat_lon_aq_data_auto = df_aq_combined_filtered[["label", "location", "latitude", "longitude"]]
df_cities_lat_lon_aq_data_auto.sort_values(by=['label'], inplace=True)
print(df_cities_lat_lon_aq_data_auto)
df_cities_lat_lon_aq_data_auto.to_csv('cities_lat_lon_aq_data_auto.csv')


plt.scatter(df_aq_combined_filtered['location'][:10], df_aq_combined_filtered['latest_reading.pm2_5'][:10])
plt.xticks(rotation=45)
plt.show()


px.set_mapbox_access_token("pk.eyJ1IjoiYnJpYW5rZWhvZSIsImEiOiJja3pvNjhjeGwxdnhtMm5sbGI2em9uMmVlIn0.WjqVTAdM5dik0MsAMasyGA")
fig = px.scatter_mapbox(df_aq_combined_filtered, lat="latitude", lon="longitude", color="location",
                        size=df_aq_combined_filtered['latest_reading.pm2_5'],
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=6)
fig.show()
