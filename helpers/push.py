from pymongo import MongoClient
import os

client = MongoClient()
client.admin.authenticate("anshumans","@nshumaN")
db = client['analysis']
ds = db['fb_15k_analysis']

z = os.listdir("/home/anshumans/Desktop/FB15K/")
i = 1

for x in z:
	f = open("/home/anshumans/Desktop/FB15K/"+x,'r')
	wololo = []
	for y in f:
		wololo.append(y.split('\n')[0])
	ds.insert_one({"origin":x,"shares":wololo})
	print i
	i += 1