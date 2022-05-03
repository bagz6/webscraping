## Property Price Webscraping

### Introduction
This coding about property price webscraping is intended to ease my repetitive task at looking for property price on the internet. As a credit analyst, I am required to create an appraisal for property that is used as loan collateral. I am looking at multiple resources to find the suitable price such as going around neighborhood where the property is located, discuss with coworkers whether they know appropriate price for the property, and browsing prices on the internet and cross validate the price with the owner of the property. I intended to reduce repetitive task by using Python programming so that I can effectively browsing for price and work faster. After looking at multiple resources and learn for three months on how to scrape web pages and discussing with my former school mate, I finally finish the code for scraping web pages.

### Coding
First thing first, I have to import library as follows

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



For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/bagz6/webscraping/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
