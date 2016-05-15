from pymongo import MongoClient
import os
import json


client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags_new

path = os.path.expanduser("~/Desktop/")

with open(path + "intermediate.json") as data_file:    
    data = json.load(data_file)

for x in data:
	table.insert_one(x)

print "done"