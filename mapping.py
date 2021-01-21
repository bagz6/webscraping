import folium
import csv
import pandas as pd 

locations = []

df = pd.read_csv('dataSource-tanah.csv')
df2= pd.read_csv('dataSource-rumah.csv')
m = folium.Map(location = [-8.673886, 115.213863], zoom_start=15)

x=0
for x in range(0, len(df['LAT'])-1):
    x += 1
    latitude = df['LAT'][x]
    longitude = df['LON'][x]
    folium.Marker(location = [latitude, longitude], icon=folium.Icon(color='green', icon='bolt')).add_to(m)
    m.save('my_map.html')

y=0
for y in range(0, len(df2['LAT'])-1):
    y += 1
    latitude = df2['LAT'][y]
    longitude = df2['LON'][y]
    folium.Marker(location = [latitude, longitude], icon=folium.Icon(color='blue', icon='bolt')).add_to(m)
    m.save('my_map.html')

#circle markers
#folium.Circle(radius= , location=[], color='').add_to(m)