import datetime
from flask import session
from database import Database
import random


class Blog(object):

    def __init__(self, title, subtitle, author, content, _id=None):
        self._id = random.randint(1,100) if _id is None else _id
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.content = content

    def add(self): 
        Database.insert("blogs", self.json())

    @staticmethod
    def get_all_posts():
        posts = Database.find_all("blogs", {})
        return posts

    @classmethod
    def get_by_id(cls, _id):
        post = Database.find("blogs", {"_id": _id})
        if post is not None:
            return post

    @classmethod
    def get_by_title(cls, title):
        post = Database.find("blogs", {"title": title})
        if post is not None:
            return post
    

    def json(self):
        return {
            "_id": self._id,
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "content": self.content   
        }
    
    @classmethod
    def delete(cls, _id):
        Database.remove("blogs", {"_id": _id})
        pass
    
    @classmethod
    def edit(cls, _id, title, subtitle, author, content):
        Database.update("blogs", {"_id": _id}, {"title":title, "subtitle":subtitle, "author":author, "content":content})





