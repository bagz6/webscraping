import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

#categoryID = 4827 : tanah
#categoryID = 88   : property
#categoryID = 5158 : rumah

# https://www.olx.co.id/api/relevance/search?category=4827&facet_limit=100&location=2000002&location_facet_limit=20&page={start}
# https://www.olx.co.id/api/relevance/search?category=5158&facet_limit=100&location=2000002&location_facet_limit=20&page={start}&type=rumah

start = 0
all_properti = []
user_id = []
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
userApi = 'https://www.olx.co.id/item/'
page = 16
while start <= page:
	start += 1
	resp = requests.get("https://www.olx.co.id/api/relevance/v2/search",
		headers=headers,
		params ={"category" : 88, "facet_limit" : 100, "location" : 2000002, "location_facet_limit" : 2000002, "page" : start}).json()

	for item in resp['data']:
		iid 	  = item['id']
		uid 	  = item['user_id']
		judul     = item['title']
		category  = item['category_id']
		harga     = item['price']['value']['display']
		deskripsi = item['description'].replace('\n', ' ')
		try:
			alamat	  = item['parameters'][-1]['value']
		except:
			alamat= ' '
		kecamatan = item['locations_resolved']['SUBLOCALITY_LEVEL_1_name']
		kab_kota  = item['locations_resolved']['ADMIN_LEVEL_3_name']

		add={
		'Ad_id'       : iid,
		'User_id'     : uid,
		'Judul'       : judul,
		'Kategori'	  : category,
		'Harga'       : harga,
		'Deskripsi'   : deskripsi,
		'Alamat'	  : alamat,
		'Kecamatan'   : kecamatan,
		'Kab/Kota'    : kab_kota
		}

		all_properti.append(add)


df = pd.DataFrame(all_properti)
print(df)

df.to_csv('result4.csv')











