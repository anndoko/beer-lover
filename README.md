# SI 507 - Final Project

## Data Source: [Craft Beer and Brewing Magazine](https://beerandbrewing.com/)
The program crawls and scrapes each beer review page to get the data of beer styles and other details.

- **Styles**
  - Name

- **Beers**
  - Name
  - Image Link
  - Rating
  - Aroma
  - Appearance
  - Flavor
  - Mouthfeel
  - Style
  - ABV
  - IBU
  - Aroma Review
  - Flavor Review
  - Overall Review

## Code Structure

This project contains the following files:

- README.md
- requirements.txt
- cache.json
- beer.db
- menu.txt
- test.py
  - `class TestDatabase`
  - `class TestClasses`
  - `class TestQueries`
- main.py
  - Classes Definitions
  - Caching
  - Web Scraping & Crawling
  - Database Creation & Data Insertion 
  - Data Processing Queries
  - Functions for Interactions

### Main Data Requesting & Processing Functions


- Classes Definitions
  - `class Style`
  - `class Beer`
- Caching
  - `def get_unique_key(url)`
  - `def make_request_using_cache(url)`
- Web Scraping & Crawling
  - `def get_style_data()`
  - `def get_beer_data`
- Database Creation & Data Insertion 
  - `def init_db_tables()`
  - `def init_db_style_data(lst)`
  - `def init_db_beer_data(lst)`
- Data Processing Queries
  - `def beers_query(style='', criteria='rating', sorting_order='top', limit='10')`
  - `def review_query(style='', comment='overall', limit='10')`
  - `def plotly_style()`
  - `def plotly_reviews()`
- Functions for Interactions
  - `def str_output(string_output)`
  - `def process_command(command)`
  - `def process_data(command_dic)`
  - `def load_menu_text()`
  - `def interactive_prompt()`


### Classes Definitions
Two classes `Class Style` and `Class Beer` are defined in this project. 

```python
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
```

### Other
Dictionaries and lists are used frequently in this program. One of the examples is how these two python data types are used to process a command.

```python
def process_command(command):
    # Set if_valid to check if the command is valid
    if_valid = True

    # Lists of valid words
    query_type_lst = ['beers', 'read-review', 'view-styles', 'view-reviews-%', 'exit']
    style_lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    sorting_criteria_lst = ['rating', 'abv']
    sorting_order_lst = ['top', 'bottom']
    comment_type_lst = ['overall', 'aroma', 'flavor']

    # -- Process the command line --
    # Lower case the command & make it a list for processing
    command_lst = command.lower().split()

    command_dic = {
        'query_type': '',
        'style': '',
        'comment': 'overall',
        'criteria': 'rating',
        'sorting_order': 'top',
        'limit': '10',
    }

    for command in command_lst:
        # query type
        if command in query_type_lst:
            command_dic['query_type'] = command
        # criteria
        elif command in sorting_criteria_lst:
            command_dic['criteria'] = command
        elif command in comment_type_lst:
            command_dic['comment'] = command
        # number of matches & specifications
        elif '=' in command:
            lst = command.split('=')
            for ele in lst:
                # top/bottom & limit
                # style
                if ele in style_lst:
                    command_dic['style'] = lst[1]
                elif ele in sorting_order_lst:
                    command_dic['sorting_order'] = lst[0]
                    command_dic['limit'] = lst[1]
        else:
            if_valid = False

    if if_valid == False:
        print('Command not recognized: ', command)

    return command_dic
```


## Interactivity

- **menu:**
  
  Show the query options available.

- **view-styles:** 
  
  Open the Plotly graph in the webbrowser; the bar chart displays the average ABV (Alcohol By Volume), aroma, flavor, and Mouthfeel.  

- **view-reviews-%:** 
  
  Open the Plotly graph in the webbrowser; the pie chart displays the the percentage of each style (number of reviews/total numbers of reviews).  

- **beers:** 
  
  Search for beers. The program allows users to narrow down the search by specify: style, sorting criteria, number of results, etc.

- **read-review:** 
  
  Search for beer reviews. The program allows users to narrow down the search by specify: style, review type (overall, aroma, or flavor), and number of results.

- **exit:** 
  
  Leave the program.
