# import modules
import sqlite3
import requests
import json
from bs4 import BeautifulSoup

# ---------- Classes ----------
class Style:
    def __init__(self, data_dic = None):
        self.name = data_dic['Name']
        self.node = data_dic['Node']

class Beer:
    def __init__(self, data_dic = None):
        self.name = data_dic['Name']
        self.image = data_dic['Image']
        self.rating = data_dic['Rating']
        self.aroma = data_dic['Aroma']
        self.appearance = data_dic['Appearance']
        self.flavor = data_dic['Flavor']
        self.mouthfeel = data_dic['Mouthfeel']
        self.style = data_dic['Style']
        self.style_id = 0
        self.style_detail = data_dic['StyleDetail']
        self.abv = data_dic['ABV']
        self.ibu = data_dic['IBU']
        self.aroma_comment = data_dic['AromaComment']
        self.flavor_comment = data_dic['FlavorComment']
        self.overall_comment = data_dic['OverallComment']

# ---------- Caching ----------
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
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
        fw = open(CACHE_FNAME,'w')
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# ---------- Web Scraping & Crawling ----------
def get_style_data():
    # Craft Beer and Brewing Magazine - Beer Reviews:
    baseurl = 'https://beerandbrewing.com'
    text = make_request_using_cache(baseurl)
    soup = BeautifulSoup(text, 'html.parser')

    # Table 1. Styles: Id, Name
    style_data_lst = []
    menu_items = soup.find_all(class_ = 'pure-menu-item')
    for item in menu_items:

        style_dic = {
            'Name': 'N/A',
            'Node': 'N/A'
        }

        link = item.find('a')['href']
        if 'cbb-beer-reviews' in link:
            style_dic['Name'] = item.find('a').string[4:]
            style_dic['Node'] = item.find('a')['href']
            style_data_lst.append(Style(style_dic))

    return style_data_lst

def get_beer_data(style_data_lst):


    # Table 2. Beers: Id, Name, StyleId, ABV, IBU Rating, Description, Aroma, Appearance, Flavor, Mouthfeel
    review_node_dic = {}
    for style_obj in style_data_lst:
        style_name = style_obj.name
        style_node = style_obj.node

        # Form the link
        baseurl = 'https://beerandbrewing.com'
        url = baseurl + style_node

        # BeautifulSoup
        text = make_request_using_cache(url)
        soup = BeautifulSoup(text, 'html.parser')

        # Get the node & Add to the list

        review_node_lst = []
        article_card_items = soup.find_all('h3')
        for item in article_card_items:
            review_node_lst.append(item.parent['href'])
        review_node_dic[style_name] = review_node_lst

    beer_data_lst = []
    for lst in review_node_dic:
        for node in review_node_dic[lst][:3]:

            # Go to each review page & scrape
            # Form the link
            url = baseurl + node

            # BeautifulSoup
            text = make_request_using_cache(url)
            soup = BeautifulSoup(text, 'html.parser')

            # Scrape the page
            beer_dic = {
                'Name': 'N/A',
                'Image': 'N/A',
                'Rating': 'N/A',
                'Aroma': 'N/A',
                'Appearance': 'N/A',
                'Flavor': 'N/A',
                'Mouthfeel': 'N/A',
                'Style': 'N/A',
                'StyleDetail': 'N/A',
                'ABV': 'N/A',
                'IBU': 'N/A',
                'AromaComment': 'N/A',
                'FlavorComment': 'N/A',
                'OverallComment': 'N/A'
            }

            # Style
            beer_dic["Style"] = lst

            # Name
            beer_dic['Name'] = soup.find('h1').text

            # Image
            try:
                beer_dic['Image'] = 'https:' + soup.find(class_ = 'article-main-image')['src']
            except:
                continue

            # Rating
            beer_dic['Rating'] = int(soup.find(class_ = 'main-score-overall rating').text[0:2])

            # Table: Aroma, Appearance, Flavor, Mouthfeel
            label_items = soup.find_all('tr')
            for item in label_items:
                # label and value
                label = item.find_all(class_ = 'table-label')[0].text.replace(':', '')
                value = item.find_all(class_ = 'table-label')[1].text[0:2].replace('\n', '')

                if label == 'Aroma':
                    beer_dic['Aroma'] = int(value)
                elif label == 'Appearance':
                    beer_dic['Appearance'] = int(value)
                elif label == 'Flavor':
                    beer_dic['Flavor'] = int(value)
                elif label == 'Mouthfeel':
                    beer_dic['Mouthfeel'] = int(value)

            # StyleDetail, ABV, IBU, Descriptions (Aroma, Flavor, Overall)
            strong_items = soup.find_all('strong')
            for item in strong_items:
                if item.string == 'Style:':
                    beer_dic['StyleDetail'] = item.parent.text.replace('Style: ', '')
                elif item.string == 'ABV:':
                    beer_dic['ABV'] = float(item.parent.text.replace('\n', '').split()[1])
                elif item.string == 'IBU:':
                    beer_dic['IBU'] = float(item.parent.text.replace('\n', '').split()[3])
                elif item.string == 'Aroma:':
                    try:
                        beer_dic['AromaComment'] = item.parent.text
                    except:
                        continue
                elif item.string == 'Flavor:':
                    try:
                        beer_dic['FlavorComment'] = item.parent.text
                    except:
                        continue
                elif item.string == 'Overall:':
                    try:
                        beer_dic['OverallComment'] = item.parent.text
                    except:
                        continue

            beer_data_lst.append(Beer(beer_dic))

    return beer_data_lst

# ---------- Database ----------
DBNAME = 'beer.db'

# Create DB & tables
def init_db_tables():
    # Create db
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print('Failure. Please try again.')

    # Drop the table if it exists
    statement = '''
        DROP TABLE IF EXISTS 'Styles';
    '''
    cur.execute(statement)
    conn.commit()

    # Create table: Styles
    statement = '''
        CREATE TABLE 'Styles' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL
        );
    '''
    try:
        cur.execute(statement)
    except:
        print('Failure. Please try again.')
    conn.commit()

    # Drop the table if it exists
    statement = '''
        DROP TABLE IF EXISTS 'Beers';
    '''
    cur.execute(statement)
    conn.commit()

    # Create table: Beers
    statement = '''
        CREATE TABLE 'Beers' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Image' TEXT,
            'Rating' INTEGER,
            'Aroma' INTEGER,
            'Appearance' INTEGER,
            'Flavor' INTEGER,
            'Mouthfeel' INTEGER,
            'Style' TEXT,
            'StyleId' INTEGER,
            'ABV' INTEGER,
            'IBU' INTEGER,
            'AromaComment' TEXT,
            'FlavorComment' TEXT,
            'OverallComment' TEXT
        );
    '''
    try:
        cur.execute(statement)
    except:
        print('Failure. Please try again.')
    conn.commit()

# Insert data into the Style table
def init_db_style_data(lst):
    for style in lst:
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
        except:
            print('Failure. Please try again.')

        statement = '''
            INSERT INTO Styles(Name) VALUES (?);
        '''

        cur.execute(statement, [style.name])
        conn.commit()

# Insert data into the Beer table
def init_db_beer_data(lst):
    for beer in lst:
        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
        except:
            print('Failure. Please try again.')

        statement = '''
            SELECT Id, Name
            FROM Styles
        '''
        style_data = cur.execute(statement).fetchall()
        for style in style_data:
            if beer.style == style[1]:
                beer.style_id = style[0]


        statement = '''
            INSERT INTO Beers(Name, Image, Rating, Aroma, Appearance, Flavor, Mouthfeel, Style, StyleId, ABV, IBU, AromaComment, FlavorComment, OverallComment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        cur.execute(statement, [beer.name, beer.image, beer.rating, beer.aroma, beer.appearance, beer.flavor, beer.mouthfeel, beer.style_detail, beer.style_id, beer.abv, beer.ibu, beer.aroma_comment, beer.flavor_comment, beer.overall_comment])
        conn.commit()

# ---------- Queries ----------



# ---------- Interactive ----------
# Process the command
def process_command(command):
    # Set if_valid to check if the command is valid
    if_valid = True

    # Lists of valid words
    query_type_lst = ["beers", "read-more"]
    style_lst = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    sorting_criteria_lst = ["rating", "abv"]
    sorting_order_lst = ["top", "bottom"]

    # -- Process the command line --
    # Lower case the command & make it a list for processing
    command_lst = command.lower().split()

    command_dic = {
        "query_type": "",
        "style": "",
        "criteria": "ratings",
        "sorting_order": "top",
        "limit": "10",
    }

    for command in command_lst:
        # query type
        if command in query_type_lst:
            command_dic["query_type"] = command
        # style
        elif command in style_lst:
            command_dic["style"] = command
        # criteria
        elif command in sorting_criteria_lst:
            command_dic["criteria"] = command
        # number of matches & specifications
        elif "=" in command:
            lst = command.split("=")
            for ele in lst:
                # top/bottom & limit
                if ele in sorting_order_lst:
                    command_dic["sorting_order"] = lst[0]
                    command_dic["limit"] = lst[1]
        else:
            if_valid = False

    if if_valid == False:
        print("Command not recognized: ", command)
    else:
        return command_dic

# Show the menu
def load_menu_text():
    with open('menu.txt') as f:
        return f.read()

# Interaction
def interactive_prompt():
    menu_text = load_menu_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')
        results = process_command(response)

        if response == 'menu':
            print(menu_text)
            continue

# ---------- Program ----------
if __name__=="__main__":
    # # Run the functions to crawl & scrape the website
    # style_data = get_style_data()
    # beer_data = get_beer_data(style_data)
    #
    # # Run the function to create database
    # init_db_tables()
    #
    # # Run the functions to insert data
    # init_db_style_data(style_data)
    # init_db_beer_data(beer_data)

    # Start the interaction
    interactive_prompt()
