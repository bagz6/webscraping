## Property Price Webscraping

### Introduction
This coding, about property price webscraping, is intended to ease my repetitive task at looking for property price on the internet. As a credit analyst, I am required to create an appraisal for property that is used as loan collateral. I am looking at multiple resources to find the suitable price such as going around neighborhood where the property is located, discuss with coworkers whether they know appropriate price for the property, and browsing prices on the internet and cross validate the price with the owner of the property. I intended to reduce repetitive task by using Python programming so that I can effectively browsing for price and work faster. After looking at multiple resources and learn for three months on how to scrape web pages and discussing with my former school mate, I finally finish the code for scraping web pages.

### Coding
First thing first, I have to import libraries as follows

```python
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import csv
from tqdm import tqdm
import time
```

- Requests is used to explore web pages
- Json is used to process json-structured data
- Beautifulsoup is used to extract information on the web page developer tools
- pandas is used to create dataframe, so that I can view the data structure and doing data cleaning before confirming that the data extracted is well structured
- csv is used to convert the dataframe to csv
- tqdm is used to view the progress of the web scraping
- time is used to view the time elapsed in scraping

After importing libraries, next I create baseurl and header

```python
baseurl = 'https://www.olx.co.id'
# jualRnA = f'https://www.olx.co.id/bali_g2000002/dijual-rumah-apartemen_c5158?page={x}'    => scraping data rumah dan apartemen yang dijual
# tanah   = f'https://www.olx.co.id/bali_g2000002/tanah_c4827?page={x}'                     => scraping data tanah yang dijual
# jualBK  = f'https://www.olx.co.id/bali_g2000002/dijual-bangunan-komersil_c5154?page={x}'  => scraping data bangunan komersil seperti ruko

headers = {
    'User-Agent':'Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36'
}
```
- ```baseurl``` is a variable to be used later in the code
- ```jualRnA``` is the url to scrape house and apartment price data
- ```tanah``` is the url to scrape landfil price
- ```jualBK``` is the url to scrape commercial building
- ```header``` is used as a cover, so that the webpage scraped thinks that the browsing is done by human, not by robot

```python
productlinks = []
uproductlinks = []
productInfo = []
for x in tqdm(range(0,162)):
    if x % 20 == 0:
        time.sleep(6)
    r = requests.get(f'https://www.olx.co.id/bali_g2000002/dijual-bangunan-komersil_c5154?page={x}',  #mengambil 20 item per halaman
        headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = list(soup.find_all('li', {'class':'EIR5N', 'data-aut-id':'itemBox'}))
    for item in productlist:
      for link in item.find_all('a', href=True):
          links = baseurl + link['href']
          ids   = links[-9:]
          add   = {
              'url_id' : ids,
              'url'    : links
          }
          productlinks.append(add)
```

I created some lists as follows
- ```productlinks``` to store every url assosiated with each product item
- ```uproductlinks``` to store unique url of each product item, because there are lots of duplicate url on the website

- ```range``` in ```tqdm``` is customized based on the item counted in the website
- ```time.sleep``` is giving pause for every step so that the webpage does not detect our scraping code as a robot. I chose to pause for 6 seconds after scraping 20 urls
- ```productlist``` contains item url in every page loaded
the ```for``` loop after that is compiling data url into ```productlinks``` list.

After compiling all the product url, now is the time to filter and look into unique url so that we can scrape efficiently

```python
for element in productlinks:
    if element not in uproductlinks:
        uproductlinks.append(element)
```
The code above provide step to filter for unique url only.

### Main code
The following is the main code to scrape all the information contains in the webpage

```python
for x in tqdm(range(0, len(uproductlinks))):
    if x % 20 == 0:
        time.sleep(5)
    client     = uproductlinks[x]['url']
    jeson      = requests.get(client, headers=headers)
    soup       = BeautifulSoup(jeson.content, 'lxml')
    try:
        target = soup.find_all('script')[7].string.strip()[15:-1]
    except:
        continue
    targetEdt  = target.replace('props:', '"props":')
    targetEdt2 = targetEdt.replace('states:', '"states":')
    targetEdt3 = targetEdt2.replace('config:', '"config":')
    targetEdt4 = targetEdt3.replace('translations:', '"translations":')

    idd        = uproductlinks[x]['url_id']
    idds       = uproductlinks[x]['url']
    data       = json.loads(targetEdt4)

    # userId     = data['states']['users']['elements'][idd]['user_id'] #sudah expired
    userId     = data['states']['items']['elements'][idd]['user_id'] #struktur sekarang
    title      = data['states']['items']['elements'][idd]['title'].replace('\n', ' ')
    deskrips   = data['states']['items']['elements'][idd]['description'].replace('\n', ' ')
    deskripsi  = deskrips.replace('\r', ' ')
    harga      = data['states']['items']['elements'][idd]['price']['value']['display']
    lat        = data['states']['items']['elements'][idd]['locations'][0]['lat']
    lon        = data['states']['items']['elements'][idd]['locations'][0]['lon']
    nama       = data['states']['users']['elements'][userId]['name']

    lb     = ' '
    lt     = ' '
    alamat = ' '
    kontak = ' '
    for isi in data['states']['items']['elements'][idd]['parameters']:
        if isi['key_name'] == "Luas bangunan":
            lb = isi['value']
        if isi['key_name'] == "Luas tanah":
            lt = isi['value']
        if isi['key_name'] == "Alamat lokasi":
            alamat = isi['value'].replace('\n', ' ')
        if isi['key_name'] == "phone":
            konta  = isi['value']
            kontak = konta.replace('+62', '62') 

    articles={
        'userId'       : userId,
        'adId'         : idd,
        'Judul'        : title,
        'LuasBangunan' : lb,
        'LuasTanah'    : lt,
        'Deskripsi'    : deskripsi,
        'Harga'        : harga,
        'Penjual'      : nama,
        'Telpon'       : kontak,
        'Url'          : idds,
        'Lat'          : lat,
        'Lon'          : lon,
        'Alamat'       : alamat,
    }
    productInfo.append(articles)
```
For a more efficient and faster scraping, I use json structure at the webpage source code (by pressing ctrl + u) see: ```target``` variable
After that I extract all the information needed by using corresponding code for json data structure. The rest of the code is compiling all the information I get from the scraping process, and append it to one ```productInfo``` list.

The last but not least, I compile all the data I get  into csv file so that I can then process the data and place it on the map
```python
df = pd.DataFrame(productInfo)

print(df)

df.to_csv('jualRuko20210503.csv')
```
## Putting scraped data into maps
After finish scraping the data, I have to put the data into maps so that it can be much useful and easy to analyze

### Acquiring data location 
I use simple Python code to retrieve every data coordinate using a free Google Maps API key that I get from Google Cloud. The code I use to retrieve the coordinate is as follows
```python
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
```
First I import several libraries, 
- pandas, to manage data in dataframe and later convert it into csv file
- requests, so that I can automatically run the program to connect and getting data from the Internet
- googlemaps, so that the Google Maps API key can be used to retrieve coordinate data

I use ```try except``` in this code, because I want to ignore any error that might happen from the process of retrieving coordinate. The data extracted from the website is not too good to be used for a precise location pinpont, but I want to use the data as it is (as per my early study in this project). After that, I compile the result in a csv file, then I convert the csv file to json file so that it can be used to show it on the map.

### Integrating data using JavaScript
Next, I create JavaScript code to construct the maps and later can be viewed on the web.
```javascript
    //map class initialize
var map = L.map('map').setView([-8.631812, 115.201907], 10);

L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 18,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
}).addTo(map);
```
I need to initialize the map, so that it can be viewed by default. In this case, the default is Bali. We can use any layer for the map, it can be openmap or anything but here I use googlemap layer. Next I add map scale and a feature so that when we hover over the map, it showed the coordinate below the map

```javascript
    //add map scale
L.control.scale().addTo(map);

//map coordinate display
map.on('mousemove', function(e){
    console.log(e)
    $('.coordinate').html(`Lat: ${e.latlng.lat} Lng: ${e.latlng.lng}`)
})
```
After that, I create pop-up info when I click on the marker result on the map
```javascript
function info(feature, layer){
    layer.bindPopup(
		"<h1 class='infoHeader'> Hi info </h1> <p class = 'infoHeader'>" + feature.properties.Judul + "</p>"
		+ "<br>" + "<b>" + "Harga : " + "</b>" + feature.properties.Harga +"</br>"
		+ "<br>" + "<b>" + "Deskripsi : " + "</b>" + feature.properties.Deskripsi + "</br>"
		);
};
```
```javascript
var circle
var search_marker

//adding marker to the map from geojson data
var marker = L.markerClusterGroup();

var propt = L.geoJson(db, {
	onEachFeature: info,
	pointToLayer: function(feature, latlng){
		return L.marker(latlng);
	}
}).addTo(marker);
marker.addTo(map);

function kmToMeters(km) {
	return km * 1000;
};

function getLocation(){
	var lat = document.getElementById("latitude").value;
	var lng = document.getElementById("longitude").value;
	var radius = kmToMeters($('#radius-selected').val());

	if(circle) {
        map.removeLayer(circle);
    }

	if (search_marker) {
        map.removeLayer(search_marker);
    }

	map.setView(new L.LatLng(lat, lng), 15);
	
	search_marker = L.marker([lat, lng]).addTo(map)
						.bindPopup('Lokasi yang Dicari')
						.openPopup();

	circle = L.circle({lat:lat, lng:lng},{
				color: 'steelblue',
				radius: radius,
				fillColor: 'steelblue',
				opacity: 0.3}).addTo(map)
	//menghapus isi informasi sebelum dijalankan ulang
	$('#ofi_paf').html('');
	//menghitung hasil marker dalam radius
	if (circle !== undefined){
		circle_lat_long = circle.getLatLng();
		var counter_points_in_circle = 0;
		propt.eachLayer(function(layer){
			layer_lat_long = layer.getLatLng();
			distance_from_layer_circle = layer_lat_long.distanceTo(circle_lat_long);
			//menampilkan informasi d dalam radius
			if (distance_from_layer_circle <= radius) {
				counter_points_in_circle += 1;
				var ofi_paf_html = '<h4>' + counter_points_in_circle +  '. ' + layer.feature.properties.Judul + '</h4>';
				ofi_paf_html += 'Jarak: ' + (distance_from_layer_circle * 0.001).toFixed(2) + 'km';

				$('#ofi_paf').append(ofi_paf_html);
			}
		});
		$('#ofi_paf_results').html(counter_points_in_circle);
	}

};

document.getElementById("getLocation").addEventListener("click",getLocation);
```

My finish work can be viewed [here](gisproper.herokuapp.com)
## Inspiration and Guidance
[Python Web Scraping: JSON in SCRIPT tags](https://www.youtube.com/watch?v=QNLBBGWEQ3Q&t=384s)

[Render Dynamic Pages - Web Scraping Product Links with Python](https://www.youtube.com/watch?v=MeBU-4Xs2RU&t=307s)

[Python Requests Tutorial: Request Web Pages, Download Images, POST Data, Read JSON, and More](https://www.youtube.com/watch?v=tb8gHvYlCFs)

[How To Add A Progress Bar In Python With Just One Line - Python Tutorial](https://www.youtube.com/watch?v=FptVpIPhdpM)

[30 Days of Python - Day 20 - Using Google Maps Geocoding and Places API - Python TUTORIAL](https://www.youtube.com/watch?v=ckPEY2KppHc)

[Leaflet Plugins database](https://leafletjs.com/plugins.html)

[Leaflet formula: Markers within radius v2](https://github.com/csessig86/leaflet-markers-within-radius-v2)

[Leaflet formula: Counting markers within a radius](https://csessig.wordpress.com/2014/06/22/leaflet-solution-counting-markers-within-a-radius/)

[Leaflet-control-geocoder](https://github.com/perliedman/leaflet-control-geocoder)

[Leaflet control geocoder positioning as texfield and icon](https://gis.stackexchange.com/questions/240299/leaflet-control-geocoder-positioning-as-texfield-and-icon)

[Google Maps API - results.geometry.location[0] returning null](https://stackoverflow.com/questions/24719643/google-maps-api-results-geometry-location0-returning-null)

[How can I assign the contents of a geojson file to a variable in Javascript?](https://stackoverflow.com/questions/55966676/how-can-i-assign-the-contents-of-a-geojson-file-to-a-variable-in-javascript)

[Geocoding in Python Using Google Maps API](https://pyshark.com/geocoding-in-python/)
