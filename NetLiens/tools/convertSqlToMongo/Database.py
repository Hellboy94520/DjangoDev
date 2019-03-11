from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)

db = client.test_database

collection = db.text_collection

post = {"author": "Mike",
        "text"  : "My First Blog !",
        "tags"  : ["mongodb", "python", "pymongo"],
        "date"  : datetime.datetime.utcnow()}

post_id = collection.insert_one(post).inserted_id
print(post_id)