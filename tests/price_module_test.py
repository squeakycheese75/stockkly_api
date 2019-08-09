import json
import unittest
import app


class TestPricesApp(unittest.TestCase):

    def setUp(self):
        self.app = app
        # self.client = self.app.test_client()
        self.data = {
            "tittle": "Religion is all about faith",
            "description": "Some serious and useful content here"
        }
        self.da = {
            "tittle": "UPDATED: Religion is all about faith",
            "description": "UPDATED: Some serious and useful content here"
        }

    def test_posting_a_blog(self):
        # resp = self.client.post(path='/blog', data=json.dumps(self.data), content_type='application/json')
        # self.assertEqual(resp.status_code, 201)
        pass

    def test_getting_all_blogs(self):
        pass

    def test_getting_a_single_blog(self):
        pass

    def test_editing_a_blog(self):
        pass

    def test_deleting_a_blog(self):
        pass


if __name__ == '__main__':
    unittest.main()
