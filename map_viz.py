import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon


def viz_results(red, yellow, blue, radius, output_filename):
    street_map = gpd.read_file('data/dubai.shp')

    filename = "UAE_Emirate.geojson"
    file = open(filename)
    emirates_map = gpd.read_file(file)

    polygon = Polygon([(55.0, 24.8), (55.0, 25.4), (55.5, 25.4), (55.5, 24.8), (55.0, 24.8)])
    street_map = gpd.clip(street_map, polygon)
    emirates_map = gpd.clip(emirates_map, polygon)

    fig = plt.figure(figsize=(16, 12), dpi=160)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Draw new build sites
    with open(red) as f:
        lines = f.readlines()

    points = []
    lats = []
    longs = []
    for line in lines:
        temp = line.split()
        points.append(temp[0])
        lats.append(temp[-2])
        longs.append(temp[-1])

    df = pd.DataFrame({'TYPE': ['build site'] * len(points), 'Latitude': lats, 'Longitude': longs})

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    gdf.plot(ax=ax, color='r', zorder=10)

    # Draw radius around new build sites
    new_df = gdf.copy()
    new_df['geometry'] = new_df['geometry'].buffer(radius / 111)
    new_df.plot(ax=ax, color='r', alpha=0.1, zorder=9)

    # Draw not selected build sites
    with open(blue) as f:
        lines = f.readlines()

    points = []
    lats = []
    longs = []
    for line in lines:
        temp = line.split()
        points.append(temp[0])
        lats.append(temp[-2])
        longs.append(temp[-1])

    df = pd.DataFrame({'TYPE': ['no build site'] * len(points), 'Latitude': lats, 'Longitude': longs})

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    gdf.plot(ax=ax, color='b', zorder=10)

    # Draw existing chargers
    with open(yellow) as f:
        lines = f.readlines()

    points = []
    lats = []
    longs = []
    for line in lines:
        temp = line.split()
        points.append(temp[0])
        lats.append(temp[-2])
        longs.append(temp[-1])

    df_charger = pd.DataFrame({'TYPE': ['charger'] * len(points), 'Latitude': lats, 'Longitude': longs})

    gdf_charger = gpd.GeoDataFrame(
        df_charger, geometry=gpd.points_from_xy(df_charger.Longitude, df_charger.Latitude))

    gdf_charger.plot(ax=ax, color='y', zorder=8)

    # Draw radius around chargers
    new_df = gdf_charger.copy()
    new_df['geometry'] = new_df['geometry'].buffer(radius / 111)
    new_df.plot(ax=ax, color='y', alpha=0.1, zorder=7)

    street_map.plot(ax=ax, color='#545454', zorder=5, linewidth=0.5)
    emirates_map.plot(ax=ax, color='#d3d3d3', zorder=0)

    plt.savefig(output_filename)


if __name__ == '__main__':
    viz_results(red='soln.txt', yellow='existing.txt', blue="non_soln.txt", radius=5, output_filename='map.png')
