from PIL import Image
# from precog_testing import cleanse
import os
import sys

dirr = sys.argv[1]

# Delete 1609B size files
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


# # Delete duplicates based on object-IDs
# dictio = {}
# x = os.listdir(dirr)
# print "Left with ",len(x)
# for c in x:
# 	paath = os.path.expanduser(dirr + "/" + c)
# 	dictio[c.split('__')[0]] = c
# for c in x:
# 	paath = os.path.expanduser(dirr + "/" + c)
# 	keyy = c.split('__')[0]
# 	if dictio[keyy] != c:
# 		os.remove(paath)
# print "Deleted duplicate images"


# x = os.listdir(dirr)
# print "Left with ",len(x)

# # Remove similar images
# cleanse.remove_duplicates(os.path.expanduser(dirr))

x = os.listdir(dirr)
print "Left with ",len(x)