from pymongo import MongoClient
import os
import Image

client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags
table2 = db.tags_new

path = os.path.expanduser("~/Desktop/Images5K")

tbp = table.find()

for row in tbp:
	entry = row
	idee = entry['_id']
	del entry['_id']
	img = Image.open(path + "/" + entry['filename'])
	img.show()
	# cv2.waitKey()
	print "T: ",entry["tensorflow_tag"],"(",str(entry["tensorflow_confidence"]),")"
	print "D: ",entry["densecap_tag"],"(",str(entry["densecap_confidence"]),")"
	x,y = input()
	if x == -1:
		print "Exiting"
		exit()
	entry["tensorflow_correct"] = x
	entry["densecap_correct"] = y
	# Insert to new DB
	table2.insert_one(entry)
	# Delete from old DB
	table.delete_one({'_id': idee})
