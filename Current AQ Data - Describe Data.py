import pandas as pd
import requests

url = "https://airquality.ie/assets/php/get-monitors.php"
headers = {"Referer": "https://airquality.ie/assets/php"}
aq_current_raw_data = pd.read_json(requests.get(url, headers=headers).text)
aq_current_latest_reading = pd.json_normalize(aq_current_raw_data['latest_reading'])
aq_current_data = pd.merge(aq_current_raw_data, aq_current_latest_reading, left_on='monitor_id', right_on='monitor_id')

print()
print("aq_current_raw_data.shape")
print(aq_current_raw_data.shape)
print()
print()
print("aq_current_raw_data.info()")
print(aq_current_raw_data.info())
print()
print()
print("Latest Readings")
print(type(aq_current_raw_data['latest_reading']))
print(aq_current_raw_data['latest_reading'][0:2].values.view())
print()
print()
print("Normalise 'latest_reading' column")
print(list(aq_current_latest_reading.columns.values))
print(aq_current_latest_reading.head())
print()
print()
print("Merge normalised df with original df")
print(list(aq_current_data.columns.values))
print(aq_current_data.head())
