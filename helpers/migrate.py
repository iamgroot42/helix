from pymongo import MongoClient
import os
import json


client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags_new

path = os.path.expanduser("~/Desktop/")

tbp = table.find()

final = []

for row in tbp:
	entry = row
	idee = entry['_id']
	del entry['_id']
	final.append(entry)


with open(path + "intermediate.json", 'w') as outfile:
    json.dump(final, outfile)
