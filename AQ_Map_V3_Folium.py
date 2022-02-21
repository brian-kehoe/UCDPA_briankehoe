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
# df = df[['region', 'period_begin', 'period_end', 'period_duration', 'median_sale_price', 'homes_sold']]
# df.to_csv('city_market_tracker.csv')

df = pd.read_csv('city_market_tracker.csv')

#Data Wrangling and Cleaning
df['snapshot_month'] = pd.to_datetime(df['period_begin'])
df["median_sale_price"] = df["median_sale_price"].astype('int')
df["homes_sold"] = df["homes_sold"].astype('int')
df.loc[:, "median_sale_price_formatted"] = df["median_sale_price"].map('{:,d}'.format)
df.rename({'region': 'city'}, axis=1, inplace=True)
df = df.sort_values("snapshot_month")

#Create customized tooltip text field
hover_text = []
for index, row in df.iterrows():
    hover_text.append(('<b>{city}</b><br><br>' +
                       'Snapshot Month: {period_begin}<br>' +
                       'Homes Sold: {homes_sold}<br>' +
                       'Median Sales Price ($): {median_sale_price_formatted}<br>'
                       ).format(
                       city=row['city'],
                       period_begin=row['period_begin'],
                       homes_sold=row['homes_sold'],
                       median_sale_price_formatted=row['median_sale_price_formatted']
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
            x=df_city['snapshot_month'],
            y=df_city['homes_sold'],
            name="Homes Sold",
            hoverinfo='none'  # Hide the hoverinfo
        ),
        secondary_y=False)  # The bar chart uses the primary y-axis (left)

    fig.add_trace(  # Add the second chart (line chart) to the figure
        go.Scatter(
            x=df_city['snapshot_month'],
            y=df_city['median_sale_price'],
            name="Median Sale Price ($)",
            mode='lines',
            text=df_city['text'],
            hoverinfo='text',  # Pass the 'text' column to the hoverinfo parameter to customize the tooltip
            line=dict(color='firebrick', width=3)  # Specify the color of the line
        ),
        secondary_y=True)  # The line chart uses the secondary y-axis (right)

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  # Change the background color of the tooltip to light gray
                      title_text="Housing Market Trends: "+cities[i],  # Add a chart title
                      title_font_family="Times New Roman",
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
                      yaxis_title='# Homes Sold',
                      yaxis2_title='Median Sales Price ($)')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]))
    )

    #End of paste

    figs['fig' + str(i)] = fig
    fig.write_html('fig' + str(i) + ".html")

df1 = pd.DataFrame(city_list, columns=['city'])
print(df1)
df2 = pd.DataFrame(html_list, columns=['html_file'])
print(df2)
df3 = pd.concat([df1, df2], axis=1)
print(df3)
lat_lon = pd.read_csv(r'cities_lat_lon.csv')  #Add the latitude and longitude for each city so that we can later on add them to markers
df_finalA = df3.merge(lat_lon, on='city', how='left')
df_finalB = df_finalA.drop(columns=['html_file_x'])
df_final = df_finalB.rename(columns={"html_file_y": "html_file"})
df_final #Create a final dataframe that has city names, html file names,  latitude and longitude.
print(df_final)

location = df_final['Latitude'].mean(), df_final['Longitude'].mean()
m = folium.Map(location=location, zoom_start=4)

for i in range(0, len(df_final)):
    html = """
    <iframe src=\"""" + df_final['html_file'][i] + """\" width="850" height="400"  frameborder="0">
    """

    popup = folium.Popup(folium.Html(html, script=True))
    folium.Marker([df_final['Latitude'].iloc[i], df_final['Longitude'].iloc[i]],
                  popup=popup, icon=folium.Icon(icon='home', prefix='fa')).add_to(m)

m.save("index.html")