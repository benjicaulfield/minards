import folium
import json
import math
import pandas as pd
import numpy as np 
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import matplotlib.pyplot as plt 

cities = pd.read_csv("data/cities.csv", sep=" ", names=["lon", "lat", "city"])
temperatures = pd.read_csv("data/temperature.txt", sep=" ", names=["lon", "temp", "days", "day"])
troops = pd.read_csv("data/troops.txt", sep=" ", names=["lon", "lat", "survivors", "direction", "division"])

df_troops = pd.DataFrame(troops)
geometry = [Point(xy) for xy in zip(df_troops.lon, df_troops.lat)]
crs = {'init': 'epsg:4326'}
gdf_troops = gpd.GeoDataFrame(troops, crs=crs, geometry=geometry)

coords = []
for i, row in gdf_troops.iterrows():
    coords.append([row.geometry.y, row.geometry.x])
​
m = folium.Map(location=[54,31],
               tiles='OpenStreetMap',
               zoom_start=5,
               control_scale=True)

def draw_troops(mapobj, df):
    coords = []
    for i, row in gdf_troops.iterrows():
        coords.append([row.geometry.y, row.geometry.x])
    for coord in coords:
        folium.CircleMarker(location = coord,
                            radius = 2.5,
                            fill = True,
                            fill_color = 'black',
                            fill_opacity = 0.75,
                            color = 'whitesmoke',
                            weight = 0.5).add_to(mapobj)
        folium.PolyLine(coords, color="black", weight=1.0).add_to(mapobj)
    
    return mapobj

def draw_polygons(mapobj):
    
    m = folium.Map(location=[54,31],
               tiles='OpenStreetMap',
               zoom_start=5,
               control_scale=True)
    
    
    for i, row in gdf_troops.iterrows():
        while i == len(gdf_troops) - 1:
            x1, y1 = coords[i]
            x2, y2 = coords[i+1]


            if x2 - x1 != 0:
                m = (y2 - y1) / (x2 - x1)
                #negative inverse slope (perpindicular angle)
                m_inv = (-1 / m)
            else:
                m_inv = 0

            c = 1 / math.sqrt(1 + (m_inv**2))
            s = m_inv / math.sqrt(1 + (m_inv**2))

            gdf_survivors = gdf_troops['survivors']
            gdf_direction = gdf_troops['direction']
            buffer = (gdf_survivors[i] / 34000) *.03
            
            x1u, y1u = (x1 + (buffer*c)), (y1 + (buffer*s))
            x1d, y1d = (x1 - (buffer*c)), (y1 - (buffer*s))
            x2u, y2u = (x2 + (buffer*c)), (y2 + (buffer*s))
            x2d, y2d = (x2 - (buffer*c)), (y2 - (buffer*s))

            lat_point_list = [x1u, x1d, x2d, x2u]
            lon_point_list = [y1u, y1d, y2d, y2u]

            polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
            crs = {'init': 'epsg:4326'}
              
            polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
            

        return mapobj
    
