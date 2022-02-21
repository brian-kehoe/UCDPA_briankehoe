import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from os.path import getmtime
import os
import json
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
import geopandas as gpd
import plotly.express as px
import seaborn as sns
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import folium
import branca
#from gmplot import gmplot
#from mpl_toolkits.basemap import Basemap

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

    if csv_age.seconds > 3600:
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


df_aq_data = pd.read_pickle('aq_raw_data.pkl')
np_aq_data = np.array(df_aq_data)

print("")
print("df_aq_data = " + str(type(df_aq_data)))
print(df_aq_data)
print("")
print("df_aq_data['latest_reading'] = " + str(type(df_aq_data['latest_reading'])))
#print(df_aq_data['latest_reading'])
print("")
print("df_aq_data['latest_reading'][0] = " + str(type(df_aq_data['latest_reading'][0])))
print(df_aq_data['latest_reading'][0:96])
print("")
print("df_aq_data['latest_reading'][0]['monitor_id'] = " + str(type(df_aq_data['latest_reading'][0]['monitor_id'])))
print(df_aq_data['latest_reading'][1]['monitor_id'])
print("")
print("df_aq_data['latest_reading'][0]['pm2_5'] = " + str(type(df_aq_data['latest_reading'][0]['pm2_5'])))
print(df_aq_data['latest_reading'][1]['pm10'])

latest_readings = pd.DataFrame(df_aq_data['latest_reading'][0:96])
#print(type(latest_readings))
#print(latest_readings.shape)
#print(latest_readings.head)

json_struct = json.loads(latest_readings.to_json(orient="records"))
df_flat = pd.json_normalize(json_struct)
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

df_cities_lat_lon_aq_data_auto = df_aq_combined_filtered[["label", "location", "latitude", "longitude"]]
df_cities_lat_lon_aq_data_auto.sort_values(by=['label'], inplace=True)
print(df_cities_lat_lon_aq_data_auto)
df_cities_lat_lon_aq_data_auto.to_csv('cities_lat_lon_aq_data_auto.csv')


plt.scatter(df_aq_combined_filtered['location'][:10], df_aq_combined_filtered['latest_reading.pm2_5'][:10])
plt.xticks(rotation=45)
plt.show()
#
# #BBox = ((df_aq_combined_filtered.longitude.min(),   df_aq_combined_filtered.longitude.max(),
# #         df_aq_combined_filtered.latitude.min(), df_aq_combined_filtered.latitude.max()))
#
# BBox = ((-10.844,   -5.405,
#          51.392, 55.417))
#
# irl_map = plt.imread('map.png')
#
# fig, ax = plt.subplots()#figsize=(8.17, 10.15))
# ax.scatter(df_aq_combined_filtered.longitude, df_aq_combined_filtered.latitude, zorder=1, alpha=0.6, c='b', s=df_aq_combined_filtered['latest_reading.pm2_5'])
# ax.set_title('Plotting AQ Data on Ireland Map')
# ax.set_xlim(BBox[0], BBox[1])
# ax.set_ylim(BBox[2], BBox[3])
# ax.imshow(irl_map, zorder=0, extent=BBox, aspect='equal')#1.28)
# #ax.imshow(irl_map, zorder=0, aspect='equal')#1.28)
# #ax.set_aspect(1.5)
# plt.show()
#
# # Read the data
# #df = pd.read_csv("airports.csv")
#
# figure = plt.figure(figsize=(8, 8))
# ax = figure.add_subplot(1, 1, 1, projection=crs.PlateCarree())
# ax.add_feature(cfeature.COASTLINE)
# #ax.add_feature(cfeature.STATES)
# ax.imshow(irl_map, zorder=0, aspect='equal')
# ax.set_extent(
#     [-10.844, -5.405, 51.392, 55.417],
#     crs=crs.PlateCarree()
# )
# # modify the plot by adding a scatterplot over the map
# plt.scatter(
#     x=df_aq_combined_filtered.longitude,
#     y=df_aq_combined_filtered.latitude,
#     color="red",
#     s=4,
#     alpha=1,
#     transform=crs.PlateCarree()
# )
# plt.show()


#data = pd.read_csv("listings.csv")

px.set_mapbox_access_token("pk.eyJ1IjoiYnJpYW5rZWhvZSIsImEiOiJja3pvNjhjeGwxdnhtMm5sbGI2em9uMmVlIn0.WjqVTAdM5dik0MsAMasyGA")

fig = px.scatter_mapbox(df_aq_combined_filtered, lat="latitude", lon="longitude", color="location",
                        size=df_aq_combined_filtered['latest_reading.pm2_5'],
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=6)
fig.show()
