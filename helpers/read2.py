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
	c = 0
	d = 0
	with open(rname) as data_file:
		for l in data_file:
			ex = json.loads(l.split('\n')[0])
			d += 1
			if len(ex['user_ids']) >= 2:
				try:
					users[ex['_id']['$oid']]["filename"] = ex['filename']
					users[ex['_id']['$oid']]["tag"] = ex['tensorflow_tag']
					c += 1
				except:
					continue
	final = {}
	for k in users.keys():
		su = 0
		for l in users[k]["users"].keys():
			su += users[k]["users"][l]
		users[k]["su"] = su
		if "filename" in users[k]:
			final[k] = users[k]
	e = 0
	f = 0
	for x in final.keys():
		if len(final[x]["users"]) == final[x]["su"]:
			e += 1
		elif len(final[x]["users"]) == -final[x]["su"]:
			f += 1
	print c,"out of",d,"annotated by at least two people"
	print e,"all agree,",f,"all disagree"


if __name__ == "__main__":
	read(sys.argv[1],sys.argv[2])


# radio telescope, radio reflector : 11
# stupa, tope : 32 - 1
# obelisk : 20
# church, church building : 28 - 4
# drilling platform, offshore rig : 17
# bolo tie, bolo, bola tie, bola : 49
# book jacket, dust cover, dust jacket, dust wrapper : 82
# envelope : 13