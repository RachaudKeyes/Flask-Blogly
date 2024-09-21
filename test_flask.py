from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


DEFAULT_IMAGE_URL = "https://cdn.vectorstock.com/i/500p/53/42/user-member-avatar-face-profile-icon-vector-22965342.jpg"

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/")
            
            self.assertEqual(resp.status_code, 302)

    def test_users_index(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_users_new_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)

    def test_users_new(self):
        with app.test_client() as client:
            d = {"first_name": "Test2", "last_name": "User2", "image_url": DEFAULT_IMAGE_URL}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2 User2", html)

    def test_users_show(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_users_edit(self):
         with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit a user</h1>", html)

    def test_users_update(self):
        with app.test_client() as client:
            d = {"first_name": "Testing", "last_name": "User1", "image_url": DEFAULT_IMAGE_URL}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testing User1", html)

    def test_users_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test User", html)        


