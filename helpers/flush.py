from pymongo import MongoClient

client = MongoClient()
db = client['image_api']
target = db['backup']

target.drop()

print target.find().count()