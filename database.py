import pymongo

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['MyBlog']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_all(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def update(collection, query, new_info):
        return Database.DATABASE[collection].update(query, new_info)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)




