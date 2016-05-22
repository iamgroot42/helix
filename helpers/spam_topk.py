from pymongo import MongoClient
from PIL import Image, ImageFile
from precog_testing import cleanse
from sets import Set
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

client = MongoClient('mongodb://localhost:27017/')

db = client.analysis
table = db.tags_with_spam_2

tbp = table.find({"spam":1})

final = {}

# Store any one file's name
for row in tbp:
	name = row["filename"]
	final[name.split('__')[0]] = name


print "Spam images: ", len(final)
path = os.path.expanduser("~/Desktop/fbparis_images")
save = os.path.expanduser("~/Desktop")

finale = []

# Direct matches:
for x in os.listdir(path):
	if x.split('__')[0] in final:
		finale.append(x)

print len(finale)
finale2 = []

i = 1
# Image-matching based matches:
for x in final.keys():
	a = Image.open(path + "/" + final[x])
	print i
	for y in os.listdir(path):
		if final[x] != y:
			b = Image.open(path + "/" + y)
			if cleanse.equal(a.convert('RGB'),b.convert('RGB')):
				finale2.append(y)
	i += 1

last = Set(finale2)
for x in finale:
	last.add(x)

f = open("actual_spam_fast.txt",'w')
for x in last:
	f.write(x + "\n")

f.close()
print "Done"