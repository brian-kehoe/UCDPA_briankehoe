import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import webbrowser
from plotly import graph_objects as go
from plotly.subplots import make_subplots


# Current air quality data visualisation
print()
print("Current air quality data visualisation")

# Read data from CSV
aq_current_valid_sites = pd.read_csv('aq_current_valid_sites.csv')


# Create scatter plot for top pm2_5 values
print("")
print("Displaying: Top 15 Sites - Scatter Plot")
fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(aq_current_valid_sites['location'][:15], aq_current_valid_sites['pm2_5'][:15])
ax.set_title("Top 15 PM2.5 Values")
ax.set_xlabel("Town")
plt.xticks(rotation=45, fontsize=7)
ax.set_ylabel("PM2.5 level")
plt.tight_layout()
fig.figure.savefig("axplot.png")
plt.show()








# # Create Plotly/Mapbox visualisation of air quality data for locations in Ireland
print("")
print("Opening: Interactive map in browser. Please wait...")
mapbox_access_token = "pk.eyJ1IjoiYnJpYW5rZWhvZSIsImEiOiJja3pvNjhjeGwxdnhtMm5sbGI2em9uMmVlIn0.WjqVTAdM5dik0MsAMasyGA"
px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(aq_current_valid_sites, lat="latitude", lon="longitude", color="pm2_5",
                        size=aq_current_valid_sites['pm2_5'],
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=20, zoom=6)
fig.show()


print()
print("Opening folium map")
location = aq_current_valid_sites['latitude'].mean(), aq_current_valid_sites['longitude'].mean()
current_aq_map = folium.Map(location=location, zoom_start=7)

for index, location_info in aq_current_valid_sites.iterrows():
    folium.Circle([location_info["latitude"], location_info["longitude"]],
                  popup=location_info["location"],
                  radius=float(location_info['pm2_5']) * 100,
                  color='crimson',
                  fill_opacity=0.6,
                  fill_color='crimson',
                  fill=True
                  ).add_to(current_aq_map)

current_aq_map.save("current_aq_map.html")
webbrowser.open_new_tab('current_aq_map.html')


# Historical air quality data visualisation
print("Beginning historical data visualisation")

print("")
print("Opening: Interactive map in browser. Please wait...")

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
df_final = df3.merge(lat_lon, on='location', how='left')
df_final = df_final.drop(columns=['Unnamed: 0'])


df_latest = df.copy()
df_latest = df_latest.groupby(['location']).last()
df_latest = df_latest.drop(columns=['Unnamed: 0', 'daily max', 'daily mean', 'PM10', 'SO2', 'time',
                                    'Date and Time', 'daily_mean', 'daily_max', 'text'])
df_final_latest = df_final.merge(df_latest, on='location', how='left')


location = df_final_latest['latitude'].mean(), df_final_latest['longitude'].mean()
historical_aq_map = folium.Map(location=location, zoom_start=7)

for i in range(0, len(df_final_latest)):
    html = """
    <iframe src=\"""" + str(df_final_latest['html_file'][i]) + """\" width="850" height="400"  frameborder="0">
    """

    #popup = folium.Popup(folium.Html(html, script=True))
    # folium.Marker([df_final_latest['Latitude'].iloc[i], df_final_latest['Longitude'].iloc[i]],
    #               popup=popup, icon=folium.Icon(icon='fire', prefix='fa')
    #               ).add_to(m)

    folium.Circle(location=[df_final_latest['latitude'].iloc[i], df_final_latest['longitude'].iloc[i]],
                  radius=float(df_final_latest.iloc[i]['PM2.5'])*100,
                  color='crimson',
                  fill_opacity=0.6,
                  fill_color='crimson',
                  fill=True).add_child(folium.Popup(folium.Html(html, script=True))
                                       ).add_to(historical_aq_map)

historical_aq_map.save("historical_aq_map.html")
webbrowser.open_new_tab('historical_aq_map.html')
