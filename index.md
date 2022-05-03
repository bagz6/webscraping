## Property Price Webscraping

### Introduction
This coding about property price webscraping is intended to ease my repetitive task at looking for property price on the internet. As a credit analyst, I am required to create an appraisal for property that is used as loan collateral. I am looking at multiple resources to find the suitable price such as going around neighborhood where the property is located, discuss with coworkers whether they know appropriate price for the property, and browsing prices on the internet and cross validate the price with the owner of the property. I intended to reduce repetitive task by using Python programming so that I can effectively browsing for price and work faster. After looking at multiple resources and learn for three months on how to scrape web pages and discussing with my former school mate, I finally finish the code for scraping web pages.

### Coding
First thing first, I have to import packages as follows

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
- pandas is used to create dataframe, so that I can view the data structure before confirming that the data extracted is well structured
- csv is used to convert the dataframe to csv
- tqdm is used to view the progress of the web scraping
- time is used to view the time elapsed in scraping

After importing packages, next I create baseurl and header

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

```python

```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/bagz6/webscraping/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
