from pymongo import MongoClient

def potato():
	lime = {}
	client = MongoClient()
	db = client['fb_analysis']
	ns = db.collection_names()
	ns.remove('system.indexes')
	print "Spam images:",len(ns)
	for source in ns:
		ds = db[source].find()
		for row in ds:
			shid = row['ID']
			if shid in lime:
				lime[shid] += 1
			else:
				lime[shid] = 1
	count = 0
	for x in lime.keys():
		count += lime[x]
	print "Users:",len(lime.keys())
	print "Total:",count

	zee = sorted(lime, key=lime.get, reverse=True)
	i = 0
	for x in zee:
		if lime[x] == 1:
			break
		print lime[x]
		i += 1
	print "Not one",i


if __name__ == "__main__":
	potato()
