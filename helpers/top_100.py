from pymongo import MongoClient
from PIL import Image
from precog_testing import cleanse
import os
import sys

def potato():
	client = MongoClient()
	db = client['analysis']
	ns = db['data_team_2x']
	dic = {}
	for row in ns.find():
		fn = int(row['filename'].split('__')[0])
		if fn in dic:
			print "lolwut"
			dic[fn] += 1
		else:
			dic[fn] = 1


def tomato():
	files = os.listdir("~/Desktop/dealwithit")
	dic = {}
	for x in files:
		fn = row['filename'].split('__')[0]
		if fn in dic:
			print 
			dic[fn] += 1
		else:
			dic[fn] = 1


def avocado():
	# Delete 1609B size files
	dirr = "~/Desktop/dealwithit"
	x = os.listdir(dirr)
	for c in x:
		paath = os.path.expanduser(dirr + "/" + c)
		try:
			size = os.path.getsize(paath) 
			if size == 1609:
				print "Deleting"
				os.remove(paath)  
		except:
			continue
	print "Deleted ? images"

	# Delete images which can't be read
	x = os.listdir(dirr)
	print "Left with ",len(x)
	for c in x:
		paath = os.path.expanduser(dirr + "/" + c)
		try:
			img = Image.open(dirr + "/" + c)
		except:
			os.remove(paath)  
	print "Deleted corrupt images"

	# Delete images which are not JPEG/PNG
	x = os.listdir(dirr)
	print "Left with ",len(x)
	for c in x:
		paath = os.path.expanduser(dirr + "/" + c)
		try:
			img = Image.open(dirr + "/" + c)
			 
		except:
			print "Should't have happened"
			continue
	print "Deleted GIF/other images"

	x = os.listdir(dirr)
	print "Left with ",len(x)

	# Remove similar images
	cleanse.remove_duplicates(os.path.expanduser(dirr))

	x = os.listdir(dirr)
	print "Left with ",len(x)


if __name__ == "__main__":
	avocado()
	tomato()
