import pandas as pd

#Top EPA monitoring sites
top_sites_list = ["EPA-25", "EPA-102", "EPA-77", "EPA-63", "EPA-66", "EPA-64", "EPA-71", "EPA-43", "EPA-59",
                  "EPA-67"]

top_site_location = {"EPA-25": "Ennis, Clare", "EPA-102": "Edenderry, Offaly", "EPA-77": "Sligo Town, Sligo",
 "EPA-63": "Wexford Town, Wexford", "EPA-66": "Tipperary Town, Tipperary", "EPA-64": "Letterkenny, Donegal",
 "EPA-71": "Tralee, Kerry", "EPA-43": "Longford Town, Longford", "EPA-59": "Waterford City, Waterford",
 "EPA-67": "Macroom, Cork"}

df_aq_data_hist_csv = pd.read_csv('aq_concatenated_df.csv')
df_aq_data_hist_csv['location'] = df_aq_data_hist_csv['Site'].map(top_site_location)
df_aq_data_hist = df_aq_data_hist_csv.copy()
df_aq_data_hist = df_aq_data_hist[df_aq_data_hist_csv["Site"].isin(top_sites_list)]
df_aq_data_hist['Date'] = pd.to_datetime(df_aq_data_hist['Date and Time']).dt.date
df_aq_data_hist['Time'] = pd.to_datetime(df_aq_data_hist['Date and Time']).dt.time
df_aq_data_hist['daily max'] = df_aq_data_hist.groupby(['Site', 'Date'])['PM2.5'].transform('max')


top_site_average_all = df_aq_data_hist
top_site_average_all = top_site_average_all.drop(columns=['Unnamed: 0'])
top_site_average_all['daily mean'] = top_site_average_all.groupby(['Site', 'Date'])['PM2.5'].transform('mean')
top_site_average_all = top_site_average_all[['Site', 'location', 'Date', 'PM2.5', 'daily max', 'daily mean', 'PM10',
                                             'SO2', 'Time', 'Date and Time']]

print("top_site_average_all")
print(top_site_average_all[['Site', 'location', 'Date', 'PM2.5', 'daily max', 'daily mean']])
print(top_site_average_all.info())
print(top_site_average_all.head())
top_site_average_all.to_csv('top_site_average_all.csv')

top_site_average_max = top_site_average_all.copy()
top_site_average_max = top_site_average_max[top_site_average_max["PM2.5"] == top_site_average_max["daily max"]]
top_site_average_max = top_site_average_max.sort_values(by=['Site', 'Date'], ascending=True)
top_site_average_max.to_csv('top_site_average_max.csv')
print(top_site_average_max.info())
print(top_site_average_max)

