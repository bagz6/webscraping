import pandas as pd 
import requests
import json
import googlemaps

df = pd.read_csv("result-rumah.csv")
gmaps_key = googlemaps.Client(key = "API key")
df['LAT'] = None
df['LON'] = None

for i in range(0, len(df), 1):
    geocode_result = gmaps_key.geocode(df.iat[i,7])
    try:
        lat = geocode_result[0]['geometry']['location']['lat']
        lon = geocode_result[0]['geometry']['location']['lng']
        df.iat[i, df.columns.get_loc('LAT')] = lat
        df.iat[i, df.columns.get_loc('LON')] = lon
    except:
        lat = None
        lon = None

print(df)
df.to_csv('dataSource-rumah.csv')