import pandas as pd

# Data Analysis - Current air quality data
print()
print("Running current air quality data analysis...")

# Read data from CSV
aq_current_data_read = pd.read_csv('aq_current_data.csv')

# Filter dataframe to only include sites which do not have a status = red and do not have blank pm2_5 data
# Sort data by pm2_5 values in descending order
# Remove sites with negative 'pm2_5' value
aq_current_valid_sites = aq_current_data_read.copy()
aq_current_valid_sites = aq_current_valid_sites[(aq_current_valid_sites['status'] != 'red')
                                                & (aq_current_valid_sites['pm2_5'].notnull())]
aq_current_valid_sites.sort_values(by=['pm2_5'], inplace=True, ascending=False)
aq_current_valid_sites = aq_current_valid_sites[aq_current_valid_sites['pm2_5'] > 0]
aq_current_valid_sites.to_csv('aq_current_valid_sites.csv')


# Create filtered list for 'lat_lon_aq_data.csv'
lat_lon_aq_data = aq_current_valid_sites.copy()
lat_lon_aq_data = lat_lon_aq_data[["label", "location", "latitude", "longitude"]]
lat_lon_aq_data.sort_values(by=['label'], inplace=True)
lat_lon_aq_data.to_csv('lat_lon_aq_data.csv')

print("Finished current air quality data analysis")


# Data Analysis - Historical air quality data
print()
print("Running historical air quality data analysis...")

# Load aq_current_valid_sites.csv and get the site codes
current_valid_sites = pd.read_csv('aq_current_valid_sites.csv')
sites = current_valid_sites[["code", "location"]]

# Load historical aq data
# Perform merge to add 'location' field
# Drop columns
aq_data_hist_csv = pd.read_csv('aq_historical_data.csv')
aq_data_merge = pd.merge(aq_data_hist_csv, sites, left_on="Site", right_on="code", how="left")
aq_data_merge = aq_data_merge.drop('code', axis=1)
aq_data_merge = aq_data_merge.drop('Unnamed: 0', axis=1)

# Create 'date' and 'time' columns
aq_data_hist = aq_data_merge.copy()
aq_data_hist['date'] = pd.to_datetime(aq_data_hist['Date and Time']).dt.date
aq_data_hist['time'] = pd.to_datetime(aq_data_hist['Date and Time']).dt.time
aq_data_hist.to_csv('aq_data_hist.csv')

# Calculate 'daily mean' and 'daily max' columns
site_daily_average_max = aq_data_hist
site_daily_average_max['daily mean'] = site_daily_average_max.groupby(['Site', 'date'])['PM2.5'].transform('mean')
site_daily_average_max['daily max'] = site_daily_average_max.groupby(['Site', 'date'])['PM2.5'].transform('max')
site_average_all = site_daily_average_max[['Site', 'location', 'date', 'PM2.5', 'daily max', 'daily mean', 'PM10',
                                           'SO2', 'time', 'Date and Time']]
site_daily_average_max.to_csv('site_daily_average_max.csv')

# Filter data to only show 'daily max' values
site_daily_max = site_daily_average_max.copy()
site_daily_max = site_daily_max[site_daily_max["PM2.5"] == site_daily_max["daily max"]]
site_daily_max = site_daily_max.sort_values(by=['Site', 'date'], ascending=True)
site_daily_max.to_csv('site_daily_max.csv')

# Add 'site max mean' column
# Drop duplicates and na values
# Sort by 'site max mean' in descending order
site_total_average_max = site_daily_max.copy()
site_total_average_max['site max mean'] = site_total_average_max.groupby(['Site'])['daily max'].transform('mean')
site_total_average_max = site_total_average_max[["Site", "location", "site max mean"]]
site_total_average_max.drop_duplicates(keep="first", inplace=True)
site_total_average_max = site_total_average_max.dropna()
site_total_average_max = site_total_average_max.sort_values(by=['site max mean'], ascending=False)
site_total_average_max.to_csv('site_total_average_max.csv')

# Select the top 15 sites
top_site_average_max = site_total_average_max.copy()
top_site_average_max = top_site_average_max.head(15)
top_site_average_max.to_csv('top_site_average_max.csv')

# Filter historical data to top 15 sites
top_sites_daily_max_mean = site_daily_max.copy()
top_sites_daily_max_mean = top_sites_daily_max_mean[top_sites_daily_max_mean["Site"].isin(top_site_average_max["Site"])]
top_sites_daily_max_mean.to_csv("top_sites_daily_max_mean.csv")

print("Finished historical air quality data analysis")
