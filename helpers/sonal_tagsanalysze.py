import os
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

a = ["charlie","kejriwalInsultsHanuman","Kulkarni","RR","Shani"]
b = ["similar","dissimilar"]

for x in a:
	for y in b:
		count = 0
		potato = os.path.expanduser("~/Desktop/sonal_analysis.txt")
		db = client[x]
		table = db[y]
		items = table.find()
		one = {}
		two = {}
		three = {}
		for z in items:
			count += 1
			first,second,third = z["tensorflow_tag"]
			# First 1 tag
			if first in one:
				one[first] += 1
			else:
				one[first] = 0
			# First 2 tags
			if first in two:
				two[first] += 1
			else:
				two[first] = 0
			if second in two:
				two[second] += 1
			else:
				two[second] = 0
			# First 3 tags
			if first in three:
				three[first] += 1
			else:
				three[first] = 0
			if second in three:
				three[second] += 1
			else:
				three[second] = 0
			if third in three:
				three[third] += 1
			else:
				three[third] = 0
		file = open(potato, "a")
		file.write(x+"_"+y+"\n")
		po = sorted(one, key=one.get, reverse=True)[0]
		ta = sorted(two, key=two.get, reverse=True)[0]
		to = sorted(three, key=three.get, reverse=True)[0]
		file.write("Images left after removing exact duplicates: "+str(count)+"\n")
		file.write("Top in one tag : "+po+", percentage : "+ str(100*(one[po]/float(count))) +"\n")
		file.write("Top in two tag : "+ta+", percentage : "+ str(100*(two[ta]/float(count))) +"\n")
		file.write("Top in three tag : "+to+", percentage : "+ str(100*(three[to]/float(count))) +"\n")
		file.write("\n")
		print "Processed"