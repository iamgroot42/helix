from pymongo import MongoClient
import os
from shutil import copyfile

client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags
table2 = db.tags_with_spam

extra = []

tbp = table2.find()

for row in tbp:
	tag = row['filename']
	extra.append(tag)

tbp = table.find()

for row in tbp:
	tag = row['filename']
	extra.remove(tag)	


dst = os.path.expanduser("~/Desktop/Images457/")
src = os.path.expanduser("~/Desktop/Images70K/")

for x in extra:
	copyfile(src + x, dst + x)