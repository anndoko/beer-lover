import unittest
from main import *

# Database
class TestDatabase(unittest.TestCase):
    def test_style_table(self):
        # Connect to DB
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        # Form the statement to get data from the table
        select_statement = '''
        SELECT *
        FROM Styles
        '''

        # Execute the statement
        results = cur.execute(select_statement)
        result = results.fetchone()
        conn.close()

        # Check the data types
        self.assertIs(type(result[0]), int)
        self.assertIs(type(result[1]), str)

    def test_beer_table(self):
        # Connect to DB
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        # Form the statement to get data from the table
        select_statement = '''
        SELECT *
        FROM Beers
        '''

        # Execute the statement
        results = cur.execute(select_statement)
        result = results.fetchall()
        conn.close()
        # Check if the table contains more than 100 entries
        self.assertGreaterEqual(len(result), 100)
        # Check the data types
        self.assertIs(type(result[0][0]), int)
        self.assertIs(type(result[0][1]), str)
        self.assertIs(type(result[0][2]), str)
        self.assertIs(type(result[0][3]), int)
        self.assertIs(type(result[0][4]), int)
        self.assertIs(type(result[0][5]), int)
        self.assertIs(type(result[0][6]), int)
        self.assertIs(type(result[0][7]), int)
        self.assertIs(type(result[0][8]), str)
        self.assertIs(type(result[0][9]), int)
        self.assertIs(type(result[0][10]), float)
        self.assertIs(type(result[0][11]), float)
        self.assertIs(type(result[0][12]), str)
        self.assertIs(type(result[0][13]), str)
        self.assertIs(type(result[0][14]), str)

# Classes
class TestClasses(unittest.TestCase):
    def test_style_class(self):
        # Test data
        test_dic = {
            'Name': 'test-style',
            'Node': '/test-node'
        }
        # Create Style instance
        result = Style(test_dic)

        # Check if it's an instance of Style
        self.assertIsInstance(result, Style)
        # Check the instance variables/values
        self.assertEqual(result.name, 'test-style')
        self.assertEqual(result.node, '/test-node')

    def test_beer_class(self):
        # Test data
        test_dic = {
            'Name': 'test-beer',
            'Image': 'test-img-link',
            'Rating': 100,
            'Aroma': 1,
            'Appearance': 2,
            'Flavor': 3,
            'Mouthfeel': 4,
            'Style': 'test-style',
            'StyleDetail': 'test-style-detail',
            'ABV': 1.0,
            'IBU': 1.5,
            'AromaComment': 'test-description',
            'FlavorComment': 'test-description',
            'OverallComment': 'test-description',
        }
        # Create Beer instance
        result = Beer(test_dic)


        # Check if it's an instance of Beer
        self.assertIsInstance(result, Beer)
        # Check the instance variables/values
        self.assertEqual(result.name, 'test-beer')
        self.assertEqual(result.image, 'test-img-link')
        self.assertEqual(result.rating, 100)
        self.assertEqual(result.aroma, 1)
        self.assertEqual(result.appearance, 2)
        self.assertEqual(result.flavor, 3)
        self.assertEqual(result.mouthfeel, 4)
        self.assertEqual(result.style, 'test-style')
        self.assertEqual(result.style_detail, 'test-style-detail')
        self.assertEqual(result.abv, 1.0)
        self.assertEqual(result.ibu, 1.5)
        self.assertEqual(result.aroma_comment, 'test-description')
        self.assertEqual(result.flavor_comment, 'test-description')
        self.assertEqual(result.overall_comment, 'test-description')

# Queries
class TestQueries(unittest.TestCase):
    def test_beers_query(arg):
        pass

    def test_style_query(arg):
        pass

unittest.main()
