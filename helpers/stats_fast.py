from pymongo import MongoClient
from PIL import Image, ImageFile
import sys
import os
import ImageChops
import imghdr
import operator
import math


ImageFile.LOAD_TRUNCATED_IMAGES = True


def equal_fast(A, B, histA, histB):
    widtha, heighta = A.size
    widthb, heightb = B.size
    if widtha != widthb or heighta != heightb:
        return False
    rms = math.sqrt(reduce(operator.add,
    map(lambda a,b: (a-b)**2, histA, histB))/len(histA))
    return (rms==0)


def statistics(USERNAME,PASSWORD,fpath):
	client = MongoClient()
	client.admin.authenticate(USERNAME,PASSWORD)
	db = client['analysis']
	table = db['data_team_use_2x']
	table2 = db['nyan']
	rows = table.find()
	unique_fnames = {}

	for row in rows:
		unique_fnames[row['filename']] = []

	dirlist = os.listdir(fpath)

	print "Pass one"
	k = 0
	den = len(unique_fnames)
	for image in unique_fnames:
		print (k*100.0)/float(den),"%"
		k += 1
		try:
			for x in dirlist:
				if x != image:
					if x.split('_')[0] == image.split('_')[0]:
						unique_fnames[image].append(x)
						os.remove(fpath + "/" + x)
		except:
			continue
		dirlist = os.listdir(fpath)

	print "Middleman",
	histograms = {}
	for img in os.listdir(fpath):
		a = Image.open(fpath + "/" + img)
		a = a.convert('RGB')
		histograms[img] = a.histogram()
	print "done"

	print "Pass two"
	k = 0
	den = len(unique_fnames)
	for image in unique_fnames:
		print (k*100.0)/float(den),"%"
		k += 1
		try:
			a = Image.open(fpath + "/" + image)
			fsizea = os.path.getsize(fpath + "/" + image) 
			for x in dirlist:
				b = Image.open(fpath + "/" + x)
				if x != image:
					fsizeb = os.path.getsize(fpath + "/" + x)
					if fsizea == fsizeb:
						if equal_fast(a,b,histograms[image],histograms[x]):	
							unique_fnames[image].append(x)
							os.remove(fpath + "/" + x)   
		except:
			continue
		dirlist = os.listdir(fpath)

	i = 0
	for x in unique_fnames.keys():
		temp = unique_fnames[x]
		temp.append(x)
		count = len(temp)
		i += count
		table2.insert_one({"image_identifier":x, "all_instances":temp, "count": count})
	print i


if __name__ == "__main__":
	statistics("anshumans","@nshumaN","fbparis_images")
	print "Done"
