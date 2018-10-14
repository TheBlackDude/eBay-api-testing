import os
import unittest
from unittest.mock import patch
from posts import get_arguments, fetch_data
from db_functions import create_db, save_posts, get_all_posts, get_post_by_id

class TestCategories(unittest.TestCase):

    @patch('posts.sys.argv', ['file', '--render']) # mock the command-line args
    def test_get_arguments_return_command_line_args(self):
        arg, msg = get_arguments()

        self.assertIsNone(msg)
        self.assertEqual(arg, ['--render'])


    @patch('posts.sys.argv', ['file'])
    def test_get_arguments_return_message_if_no_args_passed(self):
        arg, msg = get_arguments()

        self.assertIsNone(arg)
        self.assertEqual(msg, '############ You need to pass an argument #########')
    

    @patch('posts.requests.get') # mock the api call
    def test_fetch_data_return_json(self, mock_request):
        mock_request.return_value.json.return_value = [{'id': 1, 'title': 'test'}]
        data = fetch_data()

        self.assertEqual(type(data), list)
        self.assertEqual(data, [{'id': 1, 'title': 'test'}])


    def test_create_db(self):
        create_db()

        self.assertTrue('posts.db' in os.listdir())


    def test_save_posts_save_given_posts(self):
        create_db()
        # make sure db is empty
        self.assertEqual(len(get_all_posts()), 0)
        # save some posts
        data = [
            {'id': 1, 'title': 'test1', 'body': 'am the champ'},
            {'id': 2, 'title': 'test2', 'body': 'yeh am the real champ'}
        ]
        for post in data:
            save_posts(post.get('id'), post.get('title'), post.get('body'))
        self.assertEqual(len(get_all_posts()), 2)


    def test_get_post_by_id_return_post_with_given_id(self):
        new_post = {'id': 3, 'title': 'test3', 'body': 'yeh for real'}
        save_posts(new_post.get('id'), new_post.get('title'), new_post.get('body'))

        self.assertNotEqual(get_post_by_id(3)[0], 1)
        self.assertEqual(get_post_by_id(3)[1], 'test3')



if __name__ == '__main__':
    unittest.main()
