import datetime
import random
from flask import session
from database import Database

__author__ = 'Gennadii'


class User(object):
    def __init__(self, email, password, _id=None):
        self.name = email
        self.password = password
        self._id = random.randint(1,100) if _id is None else _id


    @classmethod
    def get_by_email(cls, email):
        data = Database.find("users", {"email": email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls, _id):
        data = Database.find("users", {"_id": _id})
        if data is not None:
            return cls(**data)


    def get_data(self):
        return self


    @staticmethod
    def login_valid(email, password):
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False


    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        return False


    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email


    @staticmethod
    def logout():
        session['email'] = None


    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }
        

    def save_to_mongo(self):
        Database.insert("users", self.json())


