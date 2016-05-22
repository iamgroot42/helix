from pymongo import MongoClient
import os
import Image

client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags_with_spam
table2 = db.tags_with_spam_2

path = os.path.expanduser("~/Desktop/Images1K")

tbp = table.find()

for row in tbp:
	entry = row
	idee = entry['_id']
	del entry['_id']
	img = Image.open(path + "/" + entry['filename'])
	img.show()
	print entry['filename'].split('__')[0]
	x = input()
	if x == -1:
		print "Exiting"
		exit()
	entry["spam"] = x
	# Insert to new DB
	table2.insert_one(entry)
	# Delete from old DB
	table.delete_one({'_id': idee})
