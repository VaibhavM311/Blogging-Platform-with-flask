import unittest
from app import create_app, db
from app.models import User, Post, Comment, Category, Tag

class WeeksFourToSevenTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context(); self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(username='writer', email='writer@example.com'); self.user.set_password('password123')
        db.session.add(self.user); db.session.commit()
        self.post = Post(title='Flask Search Guide', content='Learning Flask and SQLAlchemy is useful.', author=self.user)
        category = Category(name='Technology', slug='technology')
        tag = Tag(name='Flask', slug='flask')
        self.post.category = category; self.post.tags.append(tag)
        db.session.add(self.post); db.session.commit()

    def tearDown(self):
        db.session.remove(); db.drop_all(); self.ctx.pop()

    def login(self):
        return self.client.post('/auth/login', data={'email':'writer@example.com','password':'password123'}, follow_redirects=True)

    def test_post_detail_and_profile_templates(self):
        self.assertEqual(self.client.get(f'/posts/{self.post.id}').status_code, 200)
        self.assertEqual(self.client.get('/posts/user/writer').status_code, 200)

    def test_comment_requires_login(self):
        response = self.client.post(f'/posts/{self.post.id}/comments', data={'body':'Nice post'})
        self.assertIn(response.status_code, (302, 401))

    def test_authenticated_comment(self):
        self.login()
        response = self.client.post(f'/posts/{self.post.id}/comments', data={'body':'Very helpful article'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.query.count(), 1)
        self.assertIn(b'Very helpful article', response.data)

    def test_search_title_and_content(self):
        response = self.client.get('/search?q=SQLAlchemy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask Search Guide', response.data)

    def test_filter_category_and_tag(self):
        self.assertIn(b'Flask Search Guide', self.client.get('/search?category=technology').data)
        self.assertIn(b'Flask Search Guide', self.client.get('/search?tag=flask').data)

if __name__ == '__main__':
    unittest.main()
