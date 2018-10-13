import unittest
from unittest.mock import patch
from categories import fetch_data

class TestCategories(unittest.TestCase):

    @patch('categories.requests.get') # mock the api call
    def test_fetch_data_return_json(self, mock_request):
        mock_request.return_value.json.return_value = [{'id': 1, 'title': 'test'}]
        data = fetch_data()

        self.assertEqual(type(data), list)
        self.assertEqual(data, [{'id': 1, 'title': 'test'}])



if __name__ == '__main__':
    unittest.main()
