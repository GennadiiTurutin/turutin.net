import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='Nadia', email='email@gmail.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_password_setter(self):
        u = User(username='Nadia', email='email@gmail.com')
        u.set_password('cat')
        self.assertTrue(u.password_hash is not None)

    def test_check_password(self):
        u = User(username='Nadia', email='email@gmail.com')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_valid_confirmation_token(self):
        u = User(username='Nadia', email='email@gmail.com')
        u.set_password('cat')
        db.session.add(u)
        db.session.commit()
        token = u.get_token()
        self.assertTrue(u.check_token(token))


if __name__ == '__main__':
    unittest.main(verbosity=2)


