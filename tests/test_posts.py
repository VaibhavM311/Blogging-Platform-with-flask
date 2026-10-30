import unittest
from app import create_app, db
from app.models.user import User
from app.models.post import Post

class PostsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # Create author 1
        self.author1 = User(username='author_one', email='author1@example.com')
        self.author1.set_password('password123')
        db.session.add(self.author1)

        # Create author 2
        self.author2 = User(username='author_two', email='author2@example.com')
        self.author2.set_password('password123')
        db.session.add(self.author2)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, email, password):
        return self.client.post('/auth/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def test_create_post_authenticated(self):
        """Verify logged-in user can create a post."""
        self.login('author1@example.com', 'password123')

        response = self.client.post('/posts/create', data={
            'title': 'First Test Article',
            'content': 'This is the comprehensive body content for testing post creation.'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your post has been published successfully!', response.data)
        self.assertIn(b'First Test Article', response.data)

        # Verify DB entry
        post = Post.query.filter_by(title='First Test Article').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author.username, 'author_one')

    def test_create_post_unauthenticated_redirects(self):
        """Verify unauthenticated user cannot access create post page."""
        response = self.client.get('/posts/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_view_post_detail(self):
        """Verify post detail view renders correctly."""
        post = Post(title='Public Article', content='Detailed technical content.', author=self.author1)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Public Article', response.data)
        self.assertIn(b'Detailed technical content.', response.data)
        self.assertIn(b'author_one', response.data)

    def test_view_nonexistent_post_returns_404(self):
        """Verify 404 is returned for non-existent post."""
        response = self.client.get('/posts/99999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)

    def test_author_can_edit_own_post(self):
        """Verify author can edit their own post."""
        post = Post(title='Original Title', content='Original content body here.', author=self.author1)
        db.session.add(post)
        db.session.commit()

        self.login('author1@example.com', 'password123')

        response = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Updated Title',
            'content': 'Updated content body with revisions.'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your post has been updated successfully!', response.data)
        self.assertIn(b'Updated Title', response.data)

        updated = db.session.get(Post, post.id)
        self.assertEqual(updated.title, 'Updated Title')

    def test_non_author_cannot_edit_post(self):
        """Verify non-author receives 403 Forbidden when attempting to edit someone else's post."""
        post = Post(title='Author1 Private Post', content='Content by author 1.', author=self.author1)
        db.session.add(post)
        db.session.commit()

        # Login as author 2
        self.login('author2@example.com', 'password123')

        # Attempt to access edit page
        get_res = self.client.get(f'/posts/{post.id}/edit')
        self.assertEqual(get_res.status_code, 403)

        # Attempt to submit edit
        post_res = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Hacked Title',
            'content': 'Malicious overwrite content.'
        })
        self.assertEqual(post_res.status_code, 403)

        # Verify DB was NOT modified
        unaltered = db.session.get(Post, post.id)
        self.assertEqual(unaltered.title, 'Author1 Private Post')

    def test_author_can_delete_own_post(self):
        """Verify author can delete their own post."""
        post = Post(title='Post to Delete', content='This post will be deleted.', author=self.author1)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

        self.login('author1@example.com', 'password123')

        response = self.client.post(f'/posts/{post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your post has been deleted.', response.data)

        # Verify post is gone from DB
        deleted = db.session.get(Post, post_id)
        self.assertIsNone(deleted)

    def test_non_author_cannot_delete_post(self):
        """Verify non-author receives 403 Forbidden when attempting to delete someone else's post."""
        post = Post(title='Protected Post', content='Content that must remain.', author=self.author1)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

        # Login as author 2
        self.login('author2@example.com', 'password123')

        response = self.client.post(f'/posts/{post_id}/delete')
        self.assertEqual(response.status_code, 403)

        # Verify post still exists in DB
        surviving = db.session.get(Post, post_id)
        self.assertIsNotNone(surviving)

    def test_user_posts_page(self):
        """Verify author posts page displays only that author's posts."""
        p1 = Post(title='Post by Author 1', content='Content 1 text here.', author=self.author1)
        p2 = Post(title='Post by Author 2', content='Content 2 text here.', author=self.author2)
        db.session.add_all([p1, p2])
        db.session.commit()

        response = self.client.get('/posts/user/author_one')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post by Author 1', response.data)
        self.assertNotIn(b'Post by Author 2', response.data)

if __name__ == '__main__':
    unittest.main()
