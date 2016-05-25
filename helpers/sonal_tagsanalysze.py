import os
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

a = ["charlie","kejriwalInsultsHanuman","Kulkarni","RR","Shani"]
b = ["similar","dissimilar"]

potato = os.path.expanduser("~/Desktop/sonal_analysis.txt")
file = open(potato, "w")

for x in a:
	for y in b:
		count = 0
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
		file.write(x+"_"+y+"\n")
		po1 = sorted(one, key=one.get, reverse=True)[0]
		try:
			po2 = sorted(one, key=one.get, reverse=True)[1]
		except:
			po2 = None
		try:
			po3 = sorted(one, key=one.get, reverse=True)[2]
		except:
			po3 = None
		ta1 = sorted(two, key=two.get, reverse=True)[0]
		try:
			ta2 = sorted(two, key=two.get, reverse=True)[1]
		except:
			ta2 = None
		try:
			ta3 = sorted(two, key=two.get, reverse=True)[2]
		except:
			ta3 = None
		to1 = sorted(three, key=three.get, reverse=True)[0]
		try:
			to2 = sorted(three, key=three.get, reverse=True)[1]
		except:
			to2 = None
		try:
			to3 = sorted(three, key=three.get, reverse=True)[2]
		except:
			to3 = None
		file.write("Images left after removing exact duplicates: "+str(count)+"\n")
		file.write("First in one tag : "+po1+", percentage : "+ str(100*(one[po1]/float(count))) +"\n")
		try:
			file.write("Second in one tag : "+po2+", percentage : "+ str(100*(one[po2]/float(count))) +"\n")
		except:
			pass
		try:
			file.write("Third in one tag : "+po3+", percentage : "+ str(100*(one[po1]/float(count))) +"\n")
		except:
			pass
		file.write("First in two tag : "+ta1+", percentage : "+ str(100*(two[ta1]/float(count))) +"\n")
		try:
			file.write("Second in two tag : "+ta2+", percentage : "+ str(100*(two[ta2]/float(count))) +"\n")
		except:
			pass
		try:
			file.write("Third in two tag : "+ta3+", percentage : "+ str(100*(two[ta3]/float(count))) +"\n")
		except:
			pass
		file.write("First in three tag : "+to1+", percentage : "+ str(100*(three[to1]/float(count))) +"\n")
		try:
			file.write("Second in three tag : "+to2+", percentage : "+ str(100*(three[to2]/float(count))) +"\n")
		except:
			pass
		try:
			file.write("Third in three tag : "+to3+", percentage : "+ str(100*(three[to3]/float(count))) +"\n")
		except:
			pass
		file.write("\n")
		print "Processed ("+x+","+y+")"

file.close()
