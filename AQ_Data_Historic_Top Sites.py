import pandas as pd


# Load aq_current_valid_sites.csv and get the site codes
current_valid_sites = pd.read_csv('aq_current_valid_sites.csv')
sites = current_valid_sites[["code", "location"]]

# Load historical aq data
df_aq_data_hist_csv = pd.read_csv('aq_historical_data.csv')
df_aq_data_merge = pd.merge(df_aq_data_hist_csv, sites, left_on="Site", right_on="code", how="left")
df_aq_data_merge = df_aq_data_merge.drop('code', axis=1)
df_aq_data_merge = df_aq_data_merge.drop('Unnamed: 0', axis=1)
df_aq_data_merge.to_csv('df_aq_data_merge.csv')
df_aq_data_hist = df_aq_data_merge.copy()
df_aq_data_hist['date'] = pd.to_datetime(df_aq_data_hist['Date and Time']).dt.date
df_aq_data_hist['time'] = pd.to_datetime(df_aq_data_hist['Date and Time']).dt.time
df_aq_data_hist.to_csv('df_aq_data_hist.csv')


site_daily_average_max = df_aq_data_hist
site_daily_average_max['daily mean'] = site_daily_average_max.groupby(['Site', 'date'])['PM2.5'].transform('mean')
site_daily_average_max['daily max'] = site_daily_average_max.groupby(['Site', 'date'])['PM2.5'].transform('max')
site_average_all = site_daily_average_max[['Site', 'location', 'date', 'PM2.5', 'daily max', 'daily mean', 'PM10',
                                             'SO2', 'time', 'Date and Time']]
site_daily_average_max.to_csv('site_daily_average_max.csv')

site_daily_max = site_daily_average_max.copy()
site_daily_max = site_daily_max[site_daily_max["PM2.5"] == site_daily_max["daily max"]]
site_daily_max = site_daily_max.sort_values(by=['Site', 'date'], ascending=True)
site_daily_max.to_csv('site_daily_max.csv')


site_total_average_max = site_daily_max.copy()
site_total_average_max['site max mean'] = site_total_average_max.groupby(['Site'])['daily max'].transform('mean')
site_total_average_max = site_total_average_max[["Site", "location", "site max mean"]]
site_total_average_max.drop_duplicates(keep="first", inplace=True)
site_total_average_max = site_total_average_max.sort_values(by=['site max mean'], ascending=False)
site_total_average_max = site_total_average_max.dropna()
site_total_average_max.to_csv('site_total_average_max.csv')


top_site_average_max = site_total_average_max.copy()
top_site_average_max = top_site_average_max.head(15)
top_site_average_max.to_csv('top_site_average_max.csv')

top_sites_daily_max_mean = site_daily_max.copy()
top_sites_daily_max_mean = top_sites_daily_max_mean[top_sites_daily_max_mean["Site"].isin(top_site_average_max["Site"])]
top_sites_daily_max_mean.to_csv("top_sites_daily_max_mean.csv")
