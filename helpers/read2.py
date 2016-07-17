import json
import sys


def yn(x):
	if x == "no":
		return -1
	return +1


def ge2(x):
	return x >= 2


def read(fname,rname):
	users = {}

	with open(fname) as data_file:
		for l in data_file:
			ex = json.loads(l.split('\n')[0])
			key = ex['user_id']['$oid']
			key2 = ex['post_image_id']['$oid']
			if key2 not in users:
				users[key2] = {}
				users[key2]["users"] = {}
			users[key2]["users"][key] = yn(ex['_agree_with_tensor_flow_tag'])

	with open(rname) as data_file:
		for l in data_file:
			ex = json.loads(l.split('\n')[0])
			if len(ex['user_ids']) >= 2:
				try:
					users["filename"] = ex['filename']
					users["tag"] = ex['tensorflow_tag']
				except:
					continue
	# Continue from here
	exit()
	popu = {}
	topu = {}
	for x in data.keys():
		try:
			if not ge2(data[x]['agree']):
				popu[data[x]['filename']] = data[x]['agree']
				topu[data[x]['filename']] = data[x]['tf_tag']
		except:
			print data[x]
			exit()

	pops = sorted(popu, key = popu.get)
	print len(data)
	return [pops,topu]


def pops(twins):
	popu = twins[0]
	lookup = twins[1]
	print len(popu)
	# for x in popu[90:100]:
	# 	print lookup[x]
	# for x in popu:
	# 	if lookup[x] == "monitor":
	# 		print x


if __name__ == "__main__":
	pops(read(sys.argv[1],sys.argv[2]))
