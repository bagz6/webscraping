# url = 'https://www.olx.co.id/bali_g2000002/properti_c88?page=1'

import requests
import json
from bs4 import BeautifulSoup
# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import sys
# import creds
import pandas as pd
import csv
import random
from tqdm import tqdm
import time

baseurl = 'https://www.olx.co.id'
# jualRnA = f'https://www.olx.co.id/bali_g2000002/dijual-rumah-apartemen_c5158?page={x}'    => scraping data rumah dan apartemen yang dijual
# tanah   = f'https://www.olx.co.id/bali_g2000002/tanah_c4827?page={x}'                     => scraping data tanah yang dijual
# jualBK  = f'https://www.olx.co.id/bali_g2000002/dijual-bangunan-komersil_c5154?page={x}'  => scraping data bangunan komersil seperti ruko

headers = {
    'User-Agent':'Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36'
}

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

for element in productlinks:
    if element not in uproductlinks:
        uproductlinks.append(element)

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

df = pd.DataFrame(productInfo)

print(df)

df.to_csv('jualRuko20210503.csv')