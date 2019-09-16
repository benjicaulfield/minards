import os
import folium
from folium.plugins import CircleMarker
import json
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString, MultiLineString
import geopandas as gpd
import matplotlib.pyplot as plt

cities = pd.read_csv("data/cities.csv", sep=" ", names=["lon", "lat", "city"])
temperatures = pd.read_csv("data/temperature.txt", sep=" ", names=["lon", "temp", "days", "day"])
troops = pd.read_csv("data/troops.txt", sep=" ", names=["lon", "lat", "survivor"])

df = pd.DataFrame(cities)
m = folium.Map(location=[54,31],
               tiles='Stamen Toner',
               zoom_start=10,
               control_scale=True)

geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(cities, crs=crs, geometry=geometry)
gdf['geoid'] = gdf.index.astype(str)

gdf.rename(columns={'field_1': 'lon', 'field_2': 'lat', 'field_3': 'city'})

jsontxt = gdf.to_json()

def add_markers(mapobj, gdf):
    coords = []
    for i, row in gdf.iterrows():
        coords.append([row.geometry.y, row.geometry.x])
    for coord in coords:
        folium.CircleMarker(location = coord,
                            radius = 2.5,
                            fill = True,
                            fill_color = black,
                            fill_opacity = 0.75,
                            color = 'whitesmoke',
                            weight = 0.5).add_to(mapobj)
    return mapobj

f = folium.Figure(height = 400)
m.add_to(f)

def make_lines(gdf, df_out, i, geometry='geometry'):
    geom0 = gdf.loc[i][geometry]
    geom1 = gdf.loc[i+1][geometry]

    start, end = [(geom0.x, geom0.y), (geom1.x, geom1.y)]
    line = LineString([start, end])

    data = {'id': i,
            'geometry': [line]}
    df_line = pd.DataFrame(data, columns = ['id', 'geometry'])

    df_out = pd.concat([df_out, df_line])

    return df_out

df = pd.DataFrame(columns = ['id', 'geometry'])

x = 0
while x < len(gdf) - 1:
    df = make_lines(gdf, df, x)
    x += 1

gdf_line = GeoDataFrame(df, crs=crs)

folium.GeoJson(gdf_line).add_to(m)

def export_gdf(gdf, fn):
    try:
        os.remove(filename)
    except OSError:
        pass
    gdf.to_file('output.geojson', driver = "GeoJSON")

export_gdf(gdf, 'output.geojson')
