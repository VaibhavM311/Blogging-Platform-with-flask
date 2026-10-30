import unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_homepage(self):
        client = self.app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to DevBlog', response.data)

    def test_about_page(self):
        client = self.app.test_client()
        response = client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About DevBlog', response.data)

if __name__ == '__main__':
    unittest.main()
