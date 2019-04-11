import unittest
import requests
from time import sleep
import random
from datetime import datetime as dt


class FacebookApi(unittest.TestCase):

    ###################################################################################################
    #                                                                                                 #
    #                                           *** SETUP ***                                         #
    #                                                                                                 #
    ###################################################################################################

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):

        self.verificationErrors = []
        self.PAGE_ID = ''  # TODO: ENTER YOUR PAGE ID HERE
        self.TOKEN = '&access_token='  # TODO: ENTER YOUR TOKEN HERE
        self.BASE_URL = 'https://graph.facebook.com/v3.2/'
        self.BGN = self.BASE_URL + self.PAGE_ID + '/'
        self.FIELDS = '?fields='
        self.ID = 'id'
        self.FEED = 'feed'
        self.MSG = '?message='
        self.EXPECTED_POST_ID_LENGTH = 15
        self.SUCCESS = 'success'
        self.TRUE = True
        self.time = dt.now()

        # make sure the token is still active
        page = requests.get(self.BGN + self.FIELDS + self.ID + self.TOKEN).json()
        self.assertEqual(self.PAGE_ID, page[self.ID], 'Token expired')

    ###################################################################################################
    #                                                                                                 #
    #                                           *** STEPS ***                                         #
    #                                                                                                 #
    ###################################################################################################

    def test1_positive_create_post(self):
        print('\nTest positive create post')
        valid_message = 'Message text{} here at{}'.format(random.randint(100, 199), self.time)
        global create_post
        create_post = requests.post(self.BGN + self.FEED + self.MSG + valid_message + self.TOKEN)
        print(create_post.text)
        global page_post_id
        page_post_id = create_post.json()[self.ID] + '/'

        split_response = create_post.json()[self.ID].split('_')
        returned_page_id = split_response[0]
        returned_post_id = split_response[1]

        # validate the returned page id
        self.assertEqual(self.PAGE_ID, returned_page_id, 'Post not created')

        # validate the returned post id
        expected_length = len(returned_post_id) == self.EXPECTED_POST_ID_LENGTH
        are_digits = all(i.isdigit() for i in returned_post_id)
        self.assertTrue(expected_length and are_digits, 'Post not created')

    def test2_negative_create_post(self):
        print('\nTest negative create post')
        invalid_message = ''
        negative_create_post = requests.post(self.BGN + self.FEED + self.MSG + invalid_message + self.TOKEN)
        print(negative_create_post.status_code)

        # verify the response code is 400
        self.assertEqual(400, negative_create_post.status_code, 'Invalid message created')

    def test3_positive_update_post(self):
        print('\nTest positive update post')
        valid_update_message = 'Updated message text{} here at {}'.format(random.randint(200, 299), self.time)
        positive_upd_post = requests.post(self.BASE_URL + page_post_id + self.MSG + valid_update_message + self.TOKEN)
        print(positive_upd_post.text)

        # validate the response
        self.assertEqual(self.TRUE, positive_upd_post.json()[self.SUCCESS], 'Post not updated')

    def test4_repost_updated_post(self):
        print('\nTest repost updated post post')
        valid_repost_message = 'Repost on updated message text{} here at {}'.format(random.randint(300, 399), self.time)
        positive_upd_repost = requests.post(self.BASE_URL + page_post_id + self.MSG + valid_repost_message + self.TOKEN)
        print(positive_upd_repost.text)

        # validate the response
        self.assertEqual(self.TRUE, positive_upd_repost.json()[self.SUCCESS], 'Update not reposted')

    def test5_negative_update_post(self):
        print('\nTest negative update post')
        invalid_update_message = ''
        negative_upd_post = requests.post(self.BASE_URL + page_post_id + self.MSG + invalid_update_message + self.TOKEN)
        print(negative_upd_post.status_code)
        print(negative_upd_post.text)

        # validate the response
        self.assertEqual(400, negative_upd_post.status_code, 'Invalid post update created')

    def test6_delete_post(self):

        print('\nTest delete post')
        delete_post = requests.delete(self.BASE_URL + create_post.json()[self.ID] + '?' + self.TOKEN[1:])
        print(delete_post.text)

        # validate the response
        self.assertEqual(self.TRUE, delete_post.json()[self.SUCCESS], 'Post not deleted')

    ###################################################################################################
    #
    # For better test coverage, the following test should be added in both positive and negative
    # scenarios:
    #
    # - Post URL to a picture
    # - Post URL to a video
    # - Post a .gif
    # - Post with uploading a picture (in all formats), also check for valid resolution and file size
    # - Post with uploading a video (in all formats), also check for valid resolution and file size
    # - Post with emojis
    # - Post with location
    # - Post with check-in
    # - Post wih product mark
    # - Post with a key event
    #
    ###################################################################################################

    ###################################################################################################
    #                                                                                                 #
    #                                       *** SORT THE STEPS ***                                    #
    #                                                                                                 #
    ###################################################################################################

    def _steps(self):
        for name in dir(self):
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))

    ###################################################################################################
    #                                                                                                 #
    #                                        *** VERIFY ERRORS ***                                    #
    #                                                                                                 #
    ###################################################################################################

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        sleep(3)

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
