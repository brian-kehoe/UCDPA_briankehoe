import pandas as pd
import requests
from datetime import datetime
from os.path import getmtime
import os
import matplotlib.pyplot as plt
import plotly.express as px

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
    df_aq_raw_data = pd.read_json(requests.get(url, headers=headers).text)
    df_aq_data_normalised = pd.json_normalize(df_aq_raw_data['latest_reading'])
    df_aq_combined = pd.merge(df_aq_raw_data, df_aq_data_normalised, left_on='monitor_id', right_on='monitor_id')
    df_aq_combined.to_csv('df_aq_combined.csv')


# Check to see if 'aq_raw_data.csv' exists
df_aq_combined_exists = os.path.exists('df_aq_combined.csv')
print("")
print("CSV exists = " + str(df_aq_combined_exists))

# If 'aq_raw_data.csv' does not exist, get data using requests
if not df_aq_combined_exists:
    get_data()
    print("Retrieving data...")
# Else if 'aq_raw_data.csv' does exist, check the age of the file
else:
    csv_age = datetime.now() - datetime.fromtimestamp(getmtime('df_aq_combined.csv'))
    # If 'aq_raw_data.csv' is more than 1 hour old, get data using get_data function
    if csv_age.seconds > 3600:
        csv_stale = True
        print("CSV stale = " + str(csv_stale))
        get_data()
        print("Retrieving data...")
    # Else print "CSV Stale = False"
    else:
        print("CSV stale = False")

# Read data from CSV
df_aq_combined_read = pd.read_csv('df_aq_combined.csv')

# Filter dataframe to only include sites which do not have a status = red and do not have blank pm2_5 data
# Sort data by pm2_5 values in descending order
df_aq_combined_filtered = df_aq_combined_read.copy()
df_aq_combined_filtered = df_aq_combined_filtered[(df_aq_combined_filtered['status'] != 'red')
                                                  & (df_aq_combined_filtered['pm2_5'].notnull())]
df_aq_combined_filtered.sort_values(by=['pm2_5'], inplace=True, ascending=False)
df_aq_combined_filtered.to_csv('aq_current_valid_sites.csv')


# Create filtered list for 'lat_lon_aq_data_auto.csv'
lat_lon_aq_data_auto = df_aq_combined_filtered.copy()
lat_lon_aq_data_auto = lat_lon_aq_data_auto[["label", "location", "latitude", "longitude"]]
lat_lon_aq_data_auto.sort_values(by=['label'], inplace=True)
lat_lon_aq_data_auto.to_csv('lat_lon_aq_data_auto.csv')


# Create scatter plot for top pm2_5 values
print("")
print("Displaying: Top 10 Sites - Scatter Plot")
fig, ax = plt.subplots()
ax.plot(df_aq_combined_filtered['location'][:10], df_aq_combined_filtered['pm2_5'][:10])
ax.set_title("Top 10 PM2.5 Values")
ax.set_xlabel("Town")
plt.xticks(rotation=90)
ax.set_ylabel("PM2.5 level")
plt.tight_layout()
plt.show()


# Create Plotly/Mapbox visualisation of air quality data for locations in Ireland
print("")
print("Opening: Interactive map in browser. Please wait...")
mapbox_access_token = "pk.eyJ1IjoiYnJpYW5rZWhvZSIsImEiOiJja3pvNjhjeGwxdnhtMm5sbGI2em9uMmVlIn0.WjqVTAdM5dik0MsAMasyGA"
px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(df_aq_combined_filtered, lat="latitude", lon="longitude", color="location",
                        size=df_aq_combined_filtered['pm2_5'],
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=6)
fig.show()
