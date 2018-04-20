import unittest
from main import *

# Database
class TestDatabase(unittest.TestCase):
    def test_style_table(self):
        pass

    def test_beer_table(self):
        pass

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

        # Check the instance and instance variables/values
        self.assertIsInstance(result, Style) # check if it's an instance of Style
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

        # Check the instance and instance variables/values
        self.assertIsInstance(result, Beer) # check if it's an instance of Beer
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
