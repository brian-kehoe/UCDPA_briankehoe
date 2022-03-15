#Import libraries
import pandas as pd
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import folium
import webbrowser

# #Limit the data to past 4 years and 10 cities for single-family properties only
# df = df_raw[(df_raw['period_begin'] >= '2018-01-01') & (df_raw['property_type'] == 'Single Family Residential')]
# df = df[df['region'].isin(['San Francisco, CA', 'Los Angeles, CA', 'Boston, MA', 'Denver, CO', 'Seattle, WA',
#                            'Austin, TX', 'New York, NY', 'Chicago, IL', 'Raleigh, NC', 'Atlanta, GA'])]
# df = df[['region', 'period_begin', 'period_end', 'period_duration', 'daily_mean', 'daily_max']]

df = pd.read_csv('top_site_average_max.csv')
print("df.info()")
print(df.info())

#Data Wrangling and Cleaning
df['date'] = pd.to_datetime(df['Date'])
#df['date'] = df["date"].dt.strftime("%m/%d/%y")
df["daily_mean"] = round(df["daily mean"], 2)
df["daily_max"] = df["daily max"].astype('float')
#df.rename({'location': 'location'}, axis=1, inplace=True)
df = df.sort_values("date")

#Create customized tooltip text field
hover_text = []
for index, row in df.iterrows():
    hover_text.append(('<b>{location}</b><br><br>' +
                       'Date: {Date}<br>' +
                       'Max PM2.5 Level: {daily_max}<br>' +
                       'Mean PM2.5 Level: {daily_mean}<br>'
                       ).format(
                       location=row['location'],
                       Date=row['Date'],
                       daily_max=row['daily_max'],
                       daily_mean=row['daily_mean']
                      ))
df['text'] = hover_text

figs = {}  # Create an empty figure to which we will add all the plotly figures
location_list = []  # Create an empty list to which we will append all the cities
html_list = []  # Create an empty list to which we will append all the exported html files
cities = df['location'].unique()  # Get the list of location names
for i, location in enumerate(cities, start=0):
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
                      title_text="Air Quality Trends: "+str(cities[i]),  # Add a chart title
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
print("df1")
print(df1)
df2 = pd.DataFrame(html_list, columns=['html_file'])
print("df2")
print(df2)
df3 = pd.concat([df1, df2], axis=1)
print("df3")
print(df3)


lat_lon = pd.read_csv(r'lat_lon_aq_data.csv')

#Add the latitude and longitude for each location so that we can later on add them to markers
df_finalA = df3.merge(lat_lon, on='location', how='left')
print(df_finalA.info())
print(df_finalA)

df_finalB = df_finalA.rename(columns={"html_file_x": "html_file"})
df_finalB = df_finalB.drop(columns=['Unnamed: 0'])
print(df_finalB.info())
print(df_finalB)

df_final = df_finalB.drop(columns=['html_file_y'])
df_final #Create a final dataframe that has location names, html file names,  latitude and longitude.
print("df_final")
print(df_final.info())
print(df_final)

df_latest = df.copy()
df_latest = df_latest.groupby(['location']).last()
df_latest = df_latest.drop(columns=['Unnamed: 0', 'daily max', 'daily mean', 'PM10', 'SO2', 'Time',
                                    'Date and Time', 'date', 'daily_mean', 'daily_max', 'text'])
print(df_latest.info())
print(df_latest[['Site', 'PM2.5', 'Date']])

df_final_latest = df_final.merge(df_latest, on='location', how='left')
print(df_final_latest.info())
print(df_final_latest)

#df_final_latest = df_final(df_latest, on='location', how='left')

location = df_final_latest['Latitude'].mean(), df_final_latest['Longitude'].mean()
m = folium.Map(location=location, zoom_start=7)

for i in range(0, len(df_final_latest)):
    html = """
    <iframe src=\"""" + str(df_final_latest['html_file'][i]) + """\" width="850" height="400"  frameborder="0">
    """

    #popup = folium.Popup(folium.Html(html, script=True))
    # folium.Marker([df_final_latest['Latitude'].iloc[i], df_final_latest['Longitude'].iloc[i]],
    #               popup=popup, icon=folium.Icon(icon='fire', prefix='fa')
    #               ).add_to(m)

    folium.Circle(location=[df_final_latest['Latitude'].iloc[i], df_final_latest['Longitude'].iloc[i]],
                  radius=float(df_final_latest.iloc[i]['PM2.5'])*1000,
                  color='crimson',
                  fill_opacity=0.6,
                  fill_color='crimson',
                  fill=True).add_child(folium.Popup(folium.Html(html, script=True))
                   ).add_to(m)

m.save("index.html")
webbrowser.open_new_tab('index.html')
