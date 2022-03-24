import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import webbrowser
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import seaborn as sns
from tkinter import *


# Pop-up to allow user select location for historical data analysis
print("")
print("Pop-up will open to allow user select location for detailed historical air quality analysis...")

# Read "top_sites_monthly_max_mean.csv"
# Filter to unique list of locations
df_month_max = pd.read_csv("top_sites_monthly_max_mean.csv")
df_location = df_month_max['location'].unique()


window = Tk()
window.title("Historical air quality analysis")
window.geometry('300x90')

frame = LabelFrame(
    window,
    text='Select location:',
    bg='#f0f0f0',
    font=18
)
frame.pack(expand=TRUE, fill=BOTH)

selection = StringVar(window)

w = OptionMenu(window, selection, *df_location)
w.pack()


def ok():
    print("Chosen location is: " + selection.get())
    window.destroy()


button = Button(window, text="OK", command=ok)
button.pack()
mainloop()

# Store user site selection
user_location = selection.get()

# ###### CURRENT AIR QUALITY DATA VISUALISATION ######
print()
print("BEGINNING CURRENT AIR QUALITY DATA VISUALISATION")

# Read data from CSV
aq_current_valid_sites = pd.read_csv('aq_current_valid_sites.csv')


# #### Create plot for top current pm2_5 values ####
print("")
print("Displaying: Top 15 PM2.5 locations - Scatter Plot")
fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(aq_current_valid_sites['location'][:15], aq_current_valid_sites['pm2_5'][:15])
ax.set_title("Top 15 Current PM2.5 Values")
ax.set_xlabel("Location")
plt.xticks(rotation=45, fontsize=7)
ax.set_ylabel("PM2.5 level")
plt.tight_layout()
plt.savefig("Top Current PM2.5 locations.png")
webbrowser.open_new_tab('Top Current PM2.5 locations.png')


# #### Create Plotly/Mapbox visualisation of current air quality data for locations in Ireland ####
print("")
print("Opening: Interactive maps of current air quality in browser. Please wait...")

print("")
print("Opening: Plotly map")
mapbox_access_token = "pk.eyJ1IjoiYnJpYW5rZWhvZSIsImEiOiJja3pvNjhjeGwxdnhtMm5sbGI2em9uMmVlIn0.WjqVTAdM5dik0MsAMasyGA"
px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(aq_current_valid_sites, lat="latitude", lon="longitude", color="pm2_5",
                        title="Current PM2.5 Readings (µg/m³)",
                        size=aq_current_valid_sites['pm2_5'],
                        color_continuous_scale=px.colors.diverging.Portland,
                        size_max=20,
                        zoom=6,
                        hover_data={'latitude': False,  # remove species from hover data
                                    'longitude': False,
                                    'location': True,
                                    'pm2_5': ':.2f'})
fig.show()


# #### Create Folium visualisation of current air quality data for locations in Ireland ####
print()
print("Opening: Folium map")
location = aq_current_valid_sites['latitude'].mean(), aq_current_valid_sites['longitude'].mean()
current_aq_map = folium.Map(location=location, zoom_start=7)

# Conditional column for marker colours - create list of conditions and list of values
conditions = [
    (aq_current_valid_sites['pm2_5'] < 50),
    (aq_current_valid_sites['pm2_5'] >= 51) & (aq_current_valid_sites['pm2_5'] < 100),
    (aq_current_valid_sites['pm2_5'] >= 101) & (aq_current_valid_sites['pm2_5'] < 150),
    (aq_current_valid_sites['pm2_5'] >= 151) & (aq_current_valid_sites['pm2_5'] < 200),
    (aq_current_valid_sites['pm2_5'] >= 201) & (aq_current_valid_sites['pm2_5'] < 300),
    (aq_current_valid_sites['pm2_5'] >= 300)]
values = ['green', 'yellow', 'orange', 'red', 'purple', 'darkpurple']
aq_current_valid_sites['marker_color'] = np.select(conditions, values)


for index, location_info in aq_current_valid_sites.iterrows():
    latitude = location_info['latitude']
    longitude = location_info['longitude']
    location = location_info['location']
    current_pm2_5 = location_info['pm2_5']

    folium.Circle([latitude, longitude],
                  popup=location + "<br>" + "Current PM2.5 : " + str(round(current_pm2_5, 2)),
                  tooltip=location + "<br>" + "Current PM2.5: " + str(round(current_pm2_5, 2)),
                  radius=float(current_pm2_5) * 100,
                  color=location_info['marker_color'],
                  fill_opacity=0.6,
                  fill_color=location_info['marker_color'],
                  fill=True
                  ).add_to(current_aq_map)

current_aq_map.save("current_aq_map.html")
webbrowser.open_new_tab('current_aq_map.html')


# ###### HISTORICAL AIR QUALITY DATA VISUALISATION ######
print("")
print("BEGINNING HISTORICAL DATA VISUALISATION")


# #### Create plots for historical data for selected location ####


# Read historical data
df_read = pd.read_csv('aq_data_merge.csv')

# Filter historical data to user_location selection
df = df_read.copy()
df['date'] = pd.to_datetime(df['Date and Time'], format="%d/%m/%Y %H:%M")
df = df[df['location'] == user_location]
df = df.drop(columns=['Unnamed: 0', 'PM10', 'SO2', 'Date and Time'])
df = df.dropna()

# Set categorical order for months
df_month = df_month_max.copy()
df_month = df_month[df_month['location'] == user_location]
df_month['month'] = pd.Categorical(df_month['month'], categories=[7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6], ordered=True)
df_month.sort_values('month', inplace=True)

# Define xticklabels
day_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months = ['jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']


# Creating graphs of pollutant concentrations by hour, month and day of week
fig, axes = plt.subplots(1, 3, sharex=False, figsize=(18, 5))  # creating subplots, side by side
sns.set_style('whitegrid')

# PM2.5 concentration vs hour
axes[0] = sns.lineplot(ax=axes[0],
                       data=df,
                       x=df['date'].dt.hour,
                       y=df['PM2.5'],
                       color='red',
                       linewidth=1.5,
                       palette="hls")
axes[0].set(xticks=([0, 6, 12, 18, 24]))
axes[0].set_yticklabels(axes[0].get_yticks(), fontsize=13)
axes[0].set_xlabel('hour', fontsize=15)
axes[0].set_ylabel('PM2.5', fontsize=15)

# PM2.5 concentration vs month
axes[1] = sns.pointplot(ax=axes[1],
                        data=df_month,
                        x='month',
                        y='monthly max mean',
                        color='red',
                        scale=0.6,
                        markers='',
                        order=df_month['month'])
axes[1].set_xticklabels(months, fontsize=13)
axes[1].set_yticklabels(axes[1].get_yticks(), fontsize=13)
axes[1].set_xlabel('month', fontsize=15)
axes[1].set_ylabel('')
axes[1].set_title(user_location, fontsize=18)

# PM2.5 concentration vs day of week
pollutant_daily_max = max(df.groupby(df['date'].dt.dayofweek)['PM2.5'].mean()) * 1.3 # setting the lim of y due to max mean
axes[2] = sns.lineplot(ax=axes[2],
                       data=df,
                       x=df['date'].dt.dayofweek,
                       y=df['PM2.5'],
                       color='red',
                       linewidth=1.5,
                       palette="hls")
axes[2].set_xticks(np.arange(0, 7, 1))
axes[2].set_xticklabels(day_of_week, fontsize=13)
axes[2].set_ylim(0, pollutant_daily_max)
axes[2].set_xlabel('day of week', fontsize=15)
axes[2].set_ylabel('')
plt.savefig("Hourly-Monthly-Weekly historical PM2.5 charts.png")
webbrowser.open_new_tab('Hourly-Monthly-Weekly historical PM2.5 charts.png')

# PM2.5 concentration vs hour by day of week
fig2, axes2 = plt.subplots(1, 7, sharex=True, figsize=(18, 2.25))  # subplots for each day of week

# Plots
pollutant_max = max(df.groupby(df['date'].dt.hour)['PM2.5'].mean()) * 1.35  # setting the lim of y due to max mean
pollutant_max_round5 = 2.5 * round(pollutant_max/2.5)
for i in range(7):
    axes2[i] = sns.lineplot(ax=axes2[i], data=df,
                            x=df[df.date.dt.dayofweek == i]['date'].dt.hour,
                            y=df['PM2.5'],
                            color='red',
                            linewidth=1,
                            palette="hls",
                            ci=None)
    axes2[i].set_xlabel('hour', fontsize=6)
    if i == 0:
        axes2[i].set_ylabel('PM2.5', fontsize=12)
    else:
        axes2[i].set_ylabel('')
        axes2[i].set_yticklabels('')
    if i == 3:
        axes2[i].set_title(user_location)
    else:
        pass
    axes2[i].set_ylim(0, pollutant_max_round5)
    axes2[i].set(xticks=([0, 8, 16, 24]))
    axes2[i].legend(loc='upper left').set_title(day_of_week[i])

plt.savefig("Daily historical PM2.5 charts.png")
webbrowser.open_new_tab('Daily historical PM2.5 charts.png')


print("")
print("Opening: Interactive maps of historical air quality in browser. Please wait...")


df = pd.read_csv('top_sites_daily_max_mean.csv')

# Data Wrangling and Cleaning
df["daily_mean"] = round(df["daily mean"], 2)
df["daily_max"] = df["daily max"].astype('float')
df = df.sort_values("date")


# Create customized tooltip text field
hover_text = []
for index, row in df.iterrows():
    hover_text.append(('<b>{location}</b><br><br>' +
                       'Date: {Date}<br>' +
                       'Max PM2.5 Level: {daily_max}<br>' +
                       'Mean PM2.5 Level: {daily_mean}<br>'
                       ).format(
                       location=row['location'],
                       Date=row['date'],
                       daily_max=row['daily_max'],
                       daily_mean=row['daily_mean']
                      ))
df['text'] = hover_text

figs = {}  # Create an empty figure to which we will add all the plotly figures
location_list = []  # Create an empty list to which we will append all the locations
html_list = []  # Create an empty list to which we will append all the exported html files
locations = df['location'].unique()  # Get the list of location names
for i, location in enumerate(locations, start=0):
    location_list.append(location)
    html_list.append('fig' + str(i) + '.html')
    df_location = df[df['location'] == location]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(  # Add a bar chart to the figure
        go.Bar(
            x=df_location['date'],
            y=df_location['daily_max'],
            name="Max PM2.5",
            hoverinfo='none'  # Hide the hoverinfo
        ),
        secondary_y=False)  # The bar chart uses the primary y-axis (left)

    fig.add_trace(  # Add the second chart (line chart) to the figure
        go.Scatter(
            x=df_location['date'],
            y=df_location['daily_mean'],
            name="Mean PM2.5 Level",
            mode='lines',
            text=df_location['text'],
            hoverinfo='text',  # Pass the 'text' column to the hoverinfo parameter to customize the tooltip
            line=dict(color='firebrick', width=3)  # Specify the color of the line
        ),
        secondary_y=False)  # The line chart uses the secondary y-axis (right)

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  # Change the background color of the tooltip to light gray
                      title_text="Air Quality Trends: "+str(locations[i]),  # Add a chart title
                      title_font_family="Tahoma",
                      title_font_size=20,
                      title_font_color="darkblue",  # Specify font color of the title
                      title_x=0.5,  # Specify the title position
                      xaxis=dict(
                          tickfont_size=10,
                          tickangle=270,
                          showgrid=True,
                          zeroline=True,
                          showline=True,
                          showticklabels=True,
                          dtick="M1",  # Change the x-axis ticks to be monthly
                          tickformat="%b\n%Y"
                      ),
                      legend=dict(orientation='h', xanchor="center", x=0.72, y=1),  # Adjust legend position
                      yaxis_title='PM2.5 Level',
                      yaxis2_title='Mean PM2.5 Level')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ]))
    )

    figs['fig' + str(i)] = fig
    fig.write_html('fig' + str(i) + ".html")

df1 = pd.DataFrame(location_list, columns=['location'])
df2 = pd.DataFrame(html_list, columns=['html_file'])
df3 = pd.concat([df1, df2], axis=1)

# Load latitude and longitude data
lat_lon = pd.read_csv(r'lat_lon_aq_data.csv')

# Add the latitude and longitude for each location so that we can later on add them to markers
# Contains (location, html_file, label, latitude, longitude)
df_final = df3.merge(lat_lon, on='location', how='left')
df_final = df_final.drop(columns=['Unnamed: 0'])

# Join top_sites_daily_max_mean
df_daily_max_mean = df.copy()
df_daily_max_mean = df_daily_max_mean.groupby(['location']).last()
df_daily_max_mean = df_daily_max_mean.drop(columns=['Unnamed: 0', 'daily max', 'daily mean', 'PM10', 'SO2', 'time',
                                                    'Date and Time', 'daily_mean', 'daily_max', 'text'])
df_final_max = df_final.merge(df_daily_max_mean, on='location', how='left')

# Set location for map centre
location = df_final_max['latitude'].mean(), df_final_max['longitude'].mean()
historical_aq_map = folium.Map(location=location, zoom_start=7)

for i in range(0, len(df_final_max)):
    html = """
    <iframe src=\"""" + str(df_final_max['html_file'][i]) + """\" width="850" height="400"  frameborder="0">
    """
    latitude = df_final_max['latitude'].iloc[i]
    longitude = df_final_max['longitude'].iloc[i]
    location = df_final_max.iloc[i]['location']
    daily_max_mean = df_final_max.iloc[i]['daily max mean']

    folium.Circle(location=[latitude, longitude],
                  radius=float(daily_max_mean)*100,
                  color='crimson',
                  fill_opacity=0.6,
                  fill_color='crimson',
                  tooltip=location + "<br>" + "Max Daily PM2.5 (Mean): " + str(round(daily_max_mean, 2)),
                  fill=True).add_child(folium.Popup(folium.Html(html, script=True))
                                       ).add_to(historical_aq_map)

print("Opening: Folium map")
historical_aq_map.save("historical_aq_map.html")
webbrowser.open_new_tab('historical_aq_map.html')


