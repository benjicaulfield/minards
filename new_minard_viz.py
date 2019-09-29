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

def draw_polygons(mapobj):
    
    for i, row in gdf_troops.iterrows():
        
        if i == len(gdf_troops) - 1:
            pass
        
        else:
            
            x1, y1 = coords[i]
            x2, y2 = coords[i+1]

            if x2 - x1 != 0:
                #slope of line
                slope = (y2 - y1) / (x2 - x1)
                #negative inverse slope (perpindicular angle)
                slope_inv = (-1 / slope)
            else:
                slope_inv = 0

            #cosine, sine to find x, y coordinates of polygon corners
            c = 1 / math.sqrt(1 + (slope_inv**2))
            s = m_inv / math.sqrt(1 + (slope_inv**2))

            #find width of polygon (magnitude of survivors)
            gdf_survivors = gdf_troops['survivors']
            buffer = (gdf_survivors[i] / 34000) *.03

            x1u, y1u = (x1 + (buffer*c)), (y1 + (buffer*s))
            x1d, y1d = (x1 - (buffer*c)), (y1 - (buffer*s))
            x2u, y2u = (x2 + (buffer*c)), (y2 + (buffer*s))
            x2d, y2d = (x2 - (buffer*c)), (y2 - (buffer*s))

            lat_point_list = [(x1 + (buffer*c)), (x1 - (buffer*c)), (x2 - (buffer*c)), (x2 + (buffer*c))]
            lon_point_list = [(y1 + (buffer*s)), (y1 - (buffer*s)), (y2 - (buffer*s)), (y2 + (buffer*s))]     


            geometry = Polygon(zip(lon_point_list, lat_point_list))
            poly = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[geometry])       

            folium.GeoJson(poly).add_to(mapobj)





    return mapobj
    
    
