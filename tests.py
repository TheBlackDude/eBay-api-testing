import os
import unittest
from unittest.mock import patch
from categories import get_arguments, fetch_data, build_db, render_categories
from db_functions import (create_db, save_categories,
                          get_all_categories, get_category_by_id)

class TestCategories(unittest.TestCase):

    # make the xml mock data
    fake_data = '''
    <?xml version="1.0" encoding="utf-8"?>
    <GetCategoriesResponse xmlns="urn:ebay:apis:eBLBaseComponents">
      <CategoryArray>
       <Category>
        <CategoryID>2</CategoryID>
        <CategoryName>test1</CategoryName>
        <CategoryLevel>2</CategoryLevel>
        <BestOfferEnabled>true</BestOfferEnabled>
        <CategoryParentID>1</CategoryParentID>
       </Category>
      </CategoryArray>
    </GetCategoriesResponse>
    '''

    @patch('categories.sys.argv', ['file', '--render']) # mock the command-line args
    def test_get_arguments_return_command_line_args(self):
        arg, msg = get_arguments()

        self.assertIsNone(msg)
        self.assertEqual(arg, ['--render'])


    @patch('categories.sys.argv', ['file'])
    def test_get_arguments_return_message_if_no_args_passed(self):
        arg, msg = get_arguments()

        self.assertIsNone(arg)
        self.assertEqual(msg, '############ You need to pass an argument #########')


    @unittest.skip("not running this test")
    @patch('categories.requests.post') # mock the api call
    def test_fetch_data_return_list_of_dics(self, mock_request):
        mock_request.return_value = self.fake_data
        data = fetch_data()

        self.assertEqual(type(data), list)
        # self.assertEqual(data, [{
        #     'id': 1, 'name': 'test1', 'level': 2,
        #     'offer': 'true', 'parentId': 3
        # }])


    def test_create_db(self):
        create_db()

        self.assertTrue('categories.db' in os.listdir())


    def test_save_categories_save_given_categories(self):
        create_db()
        # make sure db is empty
        self.assertEqual(len(get_all_categories()), 0)
        # save some posts
        data = [
            {'id': 1, 'name': 'test1', 'level': 2,
             'offer': 'true', 'parentId': 3},
            {'id': 2, 'name': 'test2', 'level': 3,
             'offer': 'true', 'parentId': 3}
        ]
        save_categories(data)
        self.assertEqual(len(get_all_categories()), 2)


    def test_get_category_by_id_return_categories_with_given_parent_id(self):
        data = [
            {'id': 1, 'name': 'test1', 'level': 2,
             'offer': 'true', 'parentId': 3},
            {'id': 2, 'name': 'test2', 'level': 3,
             'offer': 'true', 'parentId': 3},
            {'id': 3, 'name': 'test3', 'level': 4,
             'offer': 'true', 'parentId': 5},
        ]
        save_categories(data)

        self.assertEqual(len(get_category_by_id(3)), 2)
        self.assertEqual(get_category_by_id(3)[0][1], data[0].get('name'))


    @unittest.skip("not running this test")
    @patch('categories.requests.post')
    def test_build_db_return_success_message_if_correct_arg_is_passed(self,
                                                                      mock_request):
        mock_request.return_value = self.fake_data
        message = build_db('--rebuild')

        self.assertEqual(message, 'categories saved successfully')
        # self.assertEqual(len(get_all_categories()), 2)

        bad_arg_msg = build_db('render')
        self.assertEqual(bad_arg_msg, '##### Please pass the argument "--rebuild" #####')


    def test_render_post_generate_html_if_correct_arg_passed_and_id_found(self):
        create_db()
        data = [
            {'id': 1, 'name': 'test1', 'level': 2,
             'offer': 'true', 'parentId': 3},
            {'id': 2, 'name': 'test2', 'level': 3,
             'offer': 'true', 'parentId': 3},
            {'id': 3, 'name': 'test3', 'level': 4,
             'offer': 'true', 'parentId': 5},
        ]
        save_categories(data)
        msg = render_categories(['--render', '3'])
        self.assertEqual(msg, '##### html generated successfully #####')
        bad_category_id = render_categories(['--render', '1000'])
        self.assertEqual(bad_category_id, '##### Category not found #####')



if __name__ == '__main__':
    unittest.main()
