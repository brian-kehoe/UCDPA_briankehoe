import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

# Initialize the figure
figure = plt.figure(figsize=(8,6))
# use the Mercator projection
ax = figure.add_subplot(1,1,1, projection=crs.Mercator())
# Add feature to the map
ax.stock_img()
plt.show()

figure = plt.figure(figsize=(8,6))
ax = figure.add_subplot(1,1,1, projection=crs.Mercator())
# adds a stock image as a background
ax.stock_img()
# adds national borders
ax.add_feature(cfeature.BORDERS)
# add coastlines
ax.add_feature(cfeature.COASTLINE)
plt.show()

figure = plt.figure(figsize=(8,6))
ax = figure.add_subplot(1,1,1, projection=crs.Mercator())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)
# Zoom in on the US by setting longitude/latitude parameters
ax.set_extent(
    [
        -135, # minimum latitude
        -60, # min longitude
        20, # max latitude
        55 # max longitude
    ],
    crs=crs.PlateCarree()
)
plt.show()


# Read the data
df = pd.read_csv("airports.csv")

figure = plt.figure(figsize=(8,6))
ax = figure.add_subplot(1,1,1, projection=crs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)
ax.set_extent(
    [-135, -60, 20, 55],
    crs=crs.PlateCarree()
)
# modify the plot by adding a scatterplot over the map
plt.scatter(
    x=df["LONGITUDE"],
    y=df["LATITUDE"],
    color="red",
    s=4,
    alpha=1,
    transform=crs.PlateCarree()
)
plt.show()
