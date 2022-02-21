#Import libraries
import pandas as pd
import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import folium
import branca

# #read in housing market data--takes a bit, be patient...
# df_raw = pd.read_csv(r'city_market_tracker.tsv000.gz', compression='gzip', sep='\t', quotechar='"')
#
# #Limit the data to past 4 years and 10 cities for single-family properties only
# df = df_raw[(df_raw['period_begin'] >= '2018-01-01') & (df_raw['property_type'] == 'Single Family Residential')]
# df = df[df['region'].isin(['San Francisco, CA', 'Los Angeles, CA', 'Boston, MA', 'Denver, CO', 'Seattle, WA',
#                            'Austin, TX', 'New York, NY', 'Chicago, IL', 'Raleigh, NC', 'Atlanta, GA'])]
# df = df[['region', 'period_begin', 'period_end', 'period_duration', 'daily_mean', 'daily_max']]
# df.to_csv('city_market_tracker.csv')

# df = pd.read_csv('city_market_tracker.csv')
# df['region'] = df['region'].replace(['San Francisco, CA', 'Los Angeles, CA', 'Boston, MA', 'Denver, CO', 'Seattle, WA',
#                                      'Austin, TX', 'New York, NY', 'Chicago, IL', 'Raleigh, NC', 'Atlanta, GA'],
#                                     ['Ennis, Clare', 'Edenderry, Offaly', 'Sligo Town, Sligo', 'Wexford Town, Wexford',
#                                      'Tipperary Town, Tipperary', 'Letterkenny, Donegal', 'Tralee, Kerry',
#                                      'Longford Town, Longford', 'Waterford City, Waterford', 'Macroom, Cork'])
# df.to_csv('city_market_tracker_aq_data.csv')

df = pd.read_csv('top_site_average_max.csv')
print("df.info()")
print(df.info())

#Data Wrangling and Cleaning
df['date'] = pd.to_datetime(df['Date'])
df["daily_mean"] = df["daily mean"].astype('float')
df["daily_max"] = df["daily max"].astype('float')
#df.loc[:, "daily_mean_formatted"] = df["daily_mean"].map('{:,d}'.format)
df.rename({'location': 'city'}, axis=1, inplace=True)
df = df.sort_values("date")

#Create customized tooltip text field
hover_text = []
for index, row in df.iterrows():
    hover_text.append(('<b>{city}</b><br><br>' +
                       'Snapshot Month: {Date}<br>' +
                       'Max PM2.5 Level: {daily_max}<br>' +
                       'Mean PM2.5 Level: {daily_mean}<br>'
                       ).format(
                       city=row['city'],
                       Date=row['Date'],
                       daily_max=row['daily_max'],
                       daily_mean=row['daily_mean']
                      ))
df['text'] = hover_text

figs = {}  # Create an empty figure to which we will add all the plotly figures
city_list = []  # Create an empty list to which we will append all the cities
html_list = []  # Create an empty list to which we will append all the exported html files
cities = df['city'].unique()  # Get the list of city names
for i, city in enumerate(cities, start=0):
    city_list.append(city)
    html_list.append('fig' + str(i) + '.html')
    df_city = df[df['city'] == city]

    #Insert the code (line 2-55) from previous section here. Change line 26 to: title_text="Housing Market Trends:
    # "+cities[i]. Also, when copy-and-paste make sure you place the code within the for-loop (properly indented)######

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(  # Add a bar chart to the figure
        go.Bar(
            x=df_city['date'],
            y=df_city['daily_max'],
            name="Max PM2.5",
            hoverinfo='none'  # Hide the hoverinfo
        ),
        secondary_y=False)  # The bar chart uses the primary y-axis (left)

    fig.add_trace(  # Add the second chart (line chart) to the figure
        go.Scatter(
            x=df_city['date'],
            y=df_city['daily_mean'],
            name="Mean PM2.5 Level",
            mode='lines',
            text=df_city['text'],
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

    #End of paste

    figs['fig' + str(i)] = fig
    fig.write_html('fig' + str(i) + ".html")

df1 = pd.DataFrame(city_list, columns=['city'])
print("df1")
print(df1)
df2 = pd.DataFrame(html_list, columns=['html_file'])
print("df2")
print(df2)
df3 = pd.concat([df1, df2], axis=1)
print("df3")
print(df3)


lat_lon = pd.read_csv(r'cities_lat_lon_aq_data.csv')
# lat_lon['city'] = lat_lon['city'].replace(['San Francisco, CA', 'Los Angeles, CA', 'Boston, MA', 'Denver, CO',
#                                            'Seattle, WA', 'Austin, TX', 'New York, NY', 'Chicago, IL', 'Raleigh, NC',
#                                            'Atlanta, GA'],
#                                           ['Ennis, Clare', 'Edenderry, Offaly', 'Sligo Town, Sligo',
#                                            'Wexford Town, Wexford', 'Tipperary Town, Tipperary', 'Letterkenny, Donegal',
#                                            'Tralee, Kerry', 'Longford Town, Longford', 'Waterford City, Waterford',
#                                            'Macroom, Cork'])
# lat_lon.to_csv('cities_lat_lon_aq_data.csv')

#Add the latitude and longitude for each city so that we can later on add them to markers
df_finalA = df3.merge(lat_lon, on='city', how='left')
print(df_finalA.info())
print(df_finalA)
#df_finalB = df_finalA.drop(columns=['html_file_x'])
df_finalB = df_finalA.rename(columns={"html_file_x": "html_file"})
df_finalB = df_finalB.drop(columns=['Unnamed: 0'])
print(df_finalB.info())
print(df_finalB)
#df_final = df_finalB.rename(columns={"html_file_y": "html_file"})
df_final = df_finalB.drop(columns=['html_file_y'])
df_final #Create a final dataframe that has city names, html file names,  latitude and longitude.
print("df_final")
print(df_final.info())
print(df_final)

location = df_final['Latitude'].mean(), df_final['Longitude'].mean()
m = folium.Map(location=location, zoom_start=7)

for i in range(0, len(df_final)):
    html = """
    <iframe src=\"""" + str(df_final['html_file'][i]) + """\" width="850" height="400"  frameborder="0">
    """

    popup = folium.Popup(folium.Html(html, script=True))
    folium.Marker([df_final['Latitude'].iloc[i], df_final['Longitude'].iloc[i]],
                  popup=popup, icon=folium.Icon(icon='fire', prefix='fa')).add_to(m)

m.save("index.html")
