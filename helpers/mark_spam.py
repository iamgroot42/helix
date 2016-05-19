from pymongo import MongoClient
import os
import Image

client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags_with_spam

path = os.path.expanduser("~/Desktop/ImagesK")

tbp = table.find()

count = 1

for row in tbp:
	entry = row
	idee = entry['_id']
	del entry['_id']
	del entry['spam']
	print entry['filename']
	img = Image.open(path + "/" + entry['filename'])
	img.show()
	# cv2.waitKey()
	x = input("Spam : ")
	if x == -1:
		print "Exiting"
		exit()
	entry["spam"] = x
	# Delete from old DB
	table.delete_one({'_id': idee})
	# Insert to new DB
	table.insert_one(entry)
	print count
	count += 1
