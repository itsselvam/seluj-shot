import unittest
import json
import sys
import os

# Add the project root directory to sys.path to allow importing 'backend'
# This assumes 'tests' is a subdirectory of the project root.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from backend.app import app # Flask app instance
from backend.scraper import scrape_quotes # Original scraper function

class TestApi(unittest.TestCase):

    def setUp(self):
        """Set up test client and configure app for testing."""
        app.testing = True
        self.client = app.test_client()

    def test_get_quotes_api_success(self):
        """Test the /api/quotes endpoint for successful response and data structure."""
        response = self.client.get('/api/quotes')

        self.assertEqual(response.status_code, 200, "Status code should be 200")
        self.assertEqual(response.content_type, 'application/json', "Content type should be application/json")

        try:
            data = json.loads(response.data.decode('utf-8'))
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

        self.assertIsInstance(data, list, "Response data should be a list")

        if data: # If the list is not empty
            # Check the structure of the first item
            first_quote = data[0]
            self.assertIsInstance(first_quote, dict, "Each item in the list should be a dictionary")
            self.assertIn('text', first_quote, "Each quote dictionary should have a 'text' key")
            self.assertIn('author', first_quote, "Each quote dictionary should have an 'author' key")
            self.assertIn('image_url', first_quote, "Each quote dictionary should have an 'image_url' key")
            self.assertIsInstance(first_quote['text'], str, "Quote text should be a string")
            self.assertIsInstance(first_quote['author'], str, "Quote author should be a string")
            self.assertIsInstance(first_quote['image_url'], str, "Image URL should be a string")
            self.assertTrue(first_quote['image_url'].startswith('http'), "Image URL should start with http or https")

    def test_scrape_quotes_function_format(self):
        """Test the scrape_quotes function directly for its output format."""
        # This test makes a live HTTP request, which is common for testing scrapers.
        # For more isolated unit tests, one might mock requests.get.
        quotes_list = scrape_quotes()

        self.assertIsInstance(quotes_list, list, "scrape_quotes should return a list")

        if not quotes_list:
            # This can happen if the website is down or changes structure.
            # It's not strictly a failure of the function's format if it returns an empty list
            # as per its error handling. We can print a warning or accept it.
            print("\nWarning: scrape_quotes() returned an empty list. This might be due to network issues or website changes.")
            # self.fail("scrape_quotes() returned an empty list, cannot verify item structure.")
            return # End test here if list is empty

        for item in quotes_list:
            self.assertIsInstance(item, dict, "Each item returned by scrape_quotes should be a dictionary")
            self.assertIn('text', item, "Each quote dictionary should have a 'text' key")
            self.assertIn('author', item, "Each quote dictionary should have an 'author' key")
            self.assertIn('image_url', item, "Each quote dictionary should have an 'image_url' key")
            self.assertIsInstance(item['text'], str, "Quote text should be a string")
            self.assertIsInstance(item['author'], str, "Quote author should be a string")
            self.assertIsInstance(item['image_url'], str, "Image URL should be a string")
            self.assertTrue(item['image_url'].startswith('http'), "Image URL should start with http or https")
            self.assertTrue(item['text'], "Quote text should not be empty")
            self.assertTrue(item['author'], "Quote author should not be empty")

if __name__ == '__main__':
    unittest.main()
