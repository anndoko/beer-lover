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
baseurl = "https://beerandbrewing.com"

text = make_request_using_cache(baseurl)
soup = BeautifulSoup(text, "html.parser")

# Table 1. Styles: Id, Name
style_dic = {}
menu_items = soup.find_all(class_ = "pure-menu-item")
for item in menu_items:
    link = item.find("a")["href"]
    if "cbb-beer-reviews" in link:
        style_node = item.find("a")["href"]
        style_name = item.find("a").string[4:]
        style_dic[style_name] = style_node


# Table 2. Beers: Id, Name, StyleId, ABV, IBU Rating, Description, Aroma, Appearance, Flavor, Mouthfeel
review_node_lst = []
for style in style_dic:
    style_node = style_dic[style]

    # Form the link
    url = baseurl + style_node

    # BeautifulSoup
    text = make_request_using_cache(url)
    soup = BeautifulSoup(text, "html.parser")

    # Get the node & Add to the list
    article_card_items = soup.find_all("h3")
    for item in article_card_items:
        review_node_lst.append(item.parent["href"])

# Go to each review page & scrape
for node in review_node_lst[:20]:
    # Form the link
    url = baseurl + node

    # BeautifulSoup
    text = make_request_using_cache(url)
    soup = BeautifulSoup(text, "html.parser")

    # Scrape the page
    beer_dic = {}

    # Name
    beer_dic["Name"] = soup.find("h1").text

    # Rating
    beer_dic["Rating"] = int(soup.find(class_ = "main-score-overall rating").text[0:2])

    # Table: Aroma, Appearance, Flavor, Mouthfeel
    table = soup.find_all("tr")

    for row in table:
        # label and value
        label = row.find_all(class_ = "table-label")[0].text.replace(":", "")
        value = row.find_all(class_ = "table-label")[1].text[0:2].replace("\n", "")

        if label == "Aroma":
            beer_dic["Aroma"] = value
        elif label == "Appearance":
            beer_dic["Appearance"] = value
        elif label == "Flavor":
            beer_dic["Flavor"] = value
        elif label == "Mouthfeel":
            beer_dic["Mouthfeel"] = value

    # Style, ABV, IBU, Descriptions (Aroma, Flavor, Overall)
    strong_item = soup.find_all("strong")
    for item in strong_item:
        if item.string == "Style:":
            beer_dic["Style"] = item.parent.text.replace("Style: ", "")
        elif item.string == "ABV:":
            beer_dic["ABV"] = item.parent.text.replace("\n", "").split()[1]
        elif item.string == "IBU:":
            beer_dic["IBU"] = item.parent.text.replace("\n", "").split()[3]
        elif item.string == "Aroma:":
            beer_dic["AromaComment"] = item.parent.text
        elif item.string == "Flavor:":
            beer_dic["FlavorComment"] = item.parent.text
        elif item.string == "Overall:":
            beer_dic["OverallComment"] = item.parent.text

    print(beer_dic)
    print("-"*10)
