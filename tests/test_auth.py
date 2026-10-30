import unittest
from app import create_app, db
from app.models.user import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        user = User(username='john', email='john@example.com')
        user.set_password('mysecretpass')
        self.assertTrue(user.check_password('mysecretpass'))
        self.assertFalse(user.check_password('wrongpass'))
        self.assertNotEqual(user.password_hash, 'mysecretpass')

    def test_user_registration_and_login(self):
        # 1. Register
        response = self.client.post('/auth/register', data={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created successfully', response.data)

        # 2. Login with correct credentials
        response = self.client.post('/auth/login', data={
            'email': 'bob@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, bob!', response.data)
        self.assertIn(b'Logout', response.data)

        # 3. Logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)

    def test_duplicate_user_registration(self):
        # Create initial user
        user = User(username='existing', email='existing@example.com')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

        # Attempt to register with same username
        response = self.client.post('/auth/register', data={
            'username': 'existing',
            'email': 'different@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertIn(b'That username is already taken', response.data)

        # Attempt to register with same email
        response = self.client.post('/auth/register', data={
            'username': 'different_user',
            'email': 'existing@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertIn(b'An account with this email already exists', response.data)

if __name__ == '__main__':
    unittest.main()
