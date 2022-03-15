import pandas as pd

#Top EPA monitoring sites
top_sites_list = ["EPA-25", "EPA-102", "EPA-77", "EPA-63", "EPA-66", "EPA-64", "EPA-71", "EPA-43", "EPA-59",
                  "EPA-67"]

# top_sites_list = ["EPA-25", "EPA-102", "EPA-77", "EPA-63", "EPA-66", "EPA-64", "EPA-71", "EPA-43", "EPA-59",
#                   "EPA-67", "EPA-24", "EPA-70", "EPA-75", "EPA-79", "EPA-17", "EPA-83", "EPA-49", "EPA-85",
#                   "EPA-22", "EPA-39"]

top_site_location = {"EPA-25": "Ennis, Clare", "EPA-102": "Edenderry, Offaly", "EPA-77": "Sligo Town, Sligo",
 "EPA-63": "Wexford Town, Wexford", "EPA-66": "Tipperary Town, Tipperary", "EPA-64": "Letterkenny, Donegal",
 "EPA-71": "Tralee, Kerry", "EPA-43": "Longford Town, Longford", "EPA-59": "Waterford City, Waterford",
 "EPA-67": "Macroom, Cork"}


#top_sites = pd.DataFrame(top_sites_list, columns=["Site"])

df_aq_data_hist_csv = pd.read_csv('aq_concatenated_df.csv')
#print(df_aq_data_hist_csv)

df_aq_data_hist = df_aq_data_hist_csv[df_aq_data_hist_csv["Site"].isin(top_sites_list)]
#df_aq_data_hist = df_aq_data_hist_csv[df_filtered]

df_aq_data_hist['Date'] = pd.to_datetime(df_aq_data_hist['Date and Time']).dt.date
df_aq_data_hist['Time'] = pd.to_datetime(df_aq_data_hist['Date and Time']).dt.time

print(df_aq_data_hist)
print(df_aq_data_hist.Site.unique())

df_aq_data_hist['daily max'] = df_aq_data_hist.groupby(['Site', 'Date'])['PM2.5'].transform('max')
print(df_aq_data_hist)
df_aq_data_hist.to_csv('top_site_daily_max_all.csv')

df_aq_data_hist_daily_max = df_aq_data_hist[df_aq_data_hist["PM2.5"] == df_aq_data_hist["daily max"]]
print(df_aq_data_hist_daily_max[["Date and Time", "PM2.5", "Site", "daily max"]])


for key in top_site_location:
    print(key, ": ", top_site_location[key])

df_aq_data_hist_daily_max['location'] = df_aq_data_hist_daily_max['Site'].map(top_site_location)
df_aq_data_hist_daily_max.to_csv('top_site_daily_max.csv')
print(df_aq_data_hist_daily_max)

#Top Sites - Naming
# EPA-25	Ennis, Clare
# EPA-102	Edenderry, Offaly
# EPA-77	Sligo Town, Sligo
# EPA-63	Wexford Town, Wexford
# EPA-66	Tipperary Town, Tipperary
# EPA-64	Letterkenny, Donegal
# EPA-71	Tralee, Kerry
# EPA-43	Longford Town, Longford
# EPA-59	Waterford City, Waterford
# EPA-67	Macroom, Cork



# Top Sites
# EPA-25	467.58	Ennis, Co. Clare
# EPA-102	444.73	Edenderry Library, Co. Offaly
# EPA-77	433.49	Sligo Town
# EPA-63	385.13	Wexford Opera House
# EPA-66	379.47	Tipperary Town
# EPA-64	356.95	Letterkenny, Co. Donegal
# EPA-71	343.47	Tralee Library, Co. Kerry
# EPA-43	271.13	Longford Town
# EPA-59	260.39	Brownes Road, Waterford
# EPA-67	211.4	Macroom, Co. Cork
# EPA-24	197.6	Enniscorthy, Co. Wexford
# EPA-70	188.03	Athlone Civic Centre & Library, Co. Westmeath
# EPA-75	173.72	Clonmel, Co. Tipperary
# EPA-79	170.91	Birr, Co. Offaly
# EPA-17	166.54	Ringsend, Dublin 4
# EPA-83	163.53	Naas, Co. Kildare
# EPA-49	154.4	Davitt Road, Inchicore, Dublin 12
# EPA-85	150.14	Henry Street, Limerick
# EPA-22	149.23	Rathmines, Dublin 6
# EPA-39	148.13	People's Park, Limerick
