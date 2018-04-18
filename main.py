# import modules
import sqlite3
import requests
import json
from bs4 import BeautifulSoup

# ---------- Caching ----------
CACHE_FNAME = "cache.json"
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # access the existing data
        return CACHE_DICTION[unique_ident]
    else:
        # make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text # only store the html
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# ---------- Web Scraping & Crawling ----------
# Craft Beer and Brewing Magazine - Beer Reviews:
all_reviews_url = "https://beerandbrewing.com/cbb-beer-reviews/top/IPA"

text = make_request_using_cache(all_reviews_url)
soup = BeautifulSoup(text, "html.parser")

# Table 1. Styles: Id, Name
node_lst = []

menu_items = soup.find_all(class_ = "pure-menu-item")
for item in menu_items:
    link = item.find("a")["href"]
    if "cbb-beer-reviews" in link:
        category_node = item.find("a")["href"]
        category_name = item.find("a").string[4:]
        node_lst.append(category_node)

# Table 2. Beers: Id, Name, StyleId, ABV, IBU Rating, Description, Aroma, Appearance, Flavor, Mouthfeel
