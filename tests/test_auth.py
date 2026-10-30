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

    def test_protected_routes_require_login(self):
        """Verify unauthenticated requests to protected routes redirect to login."""
        response = self.client.get('/auth/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify redirected to login page and flash message shown
        self.assertIn(b'Please log in to access this page.', response.data)
        self.assertIn(b'Sign In', response.data)

    def test_profile_and_edit_profile(self):
        """Verify authenticated session access to profile and editing details."""
        # 1. Create and login user
        user = User(username='clara', email='clara@example.com', bio='Original bio')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

        self.client.post('/auth/login', data={'email': 'clara@example.com', 'password': 'pass123'}, follow_redirects=True)

        # 2. View profile
        resp = self.client.get('/auth/profile')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'clara', resp.data)
        self.assertIn(b'Original bio', resp.data)
        self.assertIn(b'Active Session', resp.data)

        # 3. Edit profile
        edit_resp = self.client.post('/auth/edit-profile', data={
            'username': 'clara_updated',
            'email': 'clara_new@example.com',
            'bio': 'Updated professional author bio.'
        }, follow_redirects=True)
        self.assertEqual(edit_resp.status_code, 200)
        self.assertIn(b'Your profile has been updated successfully!', edit_resp.data)
        self.assertIn(b'clara_updated', edit_resp.data)
        self.assertIn(b'Updated professional author bio.', edit_resp.data)

        # 4. Check database directly
        updated_user = db.session.get(User, user.id)
        self.assertEqual(updated_user.username, 'clara_updated')
        self.assertEqual(updated_user.email, 'clara_new@example.com')
        self.assertEqual(updated_user.bio, 'Updated professional author bio.')

if __name__ == '__main__':
    unittest.main()
