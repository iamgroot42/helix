import json
import sys


def yn(x):
	if x =="no":
		return -1
	return +1


def sign(x):
	return x>=0


def read(fname,rname):
	data = {}
	with open(fname) as data_file:
		for l in data_file:
			ex = json.loads(l.split('\n')[0])
			key = ex['post_image_id']['$oid']
			if key in data:
				data[key]['agree'] += yn(ex['_agree_with_tensor_flow_tag'])
			else:
				data[key] = ex
				data[key]['agree'] = yn(ex['_agree_with_tensor_flow_tag'])

	with open(rname) as data_file:
		for l in data_file:
			try:
				ex = json.loads(l.split('\n')[0])
				data[ex['_id']['$oid']]['filename'] = ex['filename']
				data[ex['_id']['$oid']]['tf_tag'] = ex['tensorflow_tag']
				# if ex['tensorflow_tag'] == "fountain":
				# if ex['tensorflow_tag'] == "obelisk" and sign(data[ex['_id']['$oid']]['agree']):
				# 	print ex['filename']
			except:
				continue

	popu = {}
	topu = {}
	for x in data.keys():
		if not sign(data[x]['agree']):
			popu[data[x]['filename']] = data[x]['agree']
			topu[data[x]['filename']] = data[x]['tf_tag']

	pops = sorted(popu, key = popu.get)
	# print len(data)
	return [pops,topu]


def pops(twins):
	popu = twins[0]
	lookup = twins[1]
	# print len(popu)
	# for x in popu[90:100]:
	# 	print lookup[x]
	# for x in popu:
	# 	if lookup[x] == "monitor":
	# 		print x


if __name__ == "__main__":
	pops(read(sys.argv[1],sys.argv[2]))
