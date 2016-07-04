import json

f_name = "post_images.json"

f = open(f_name,'r')

recs = []
for x in f:
	si = json.loads(x.split('\n')[0])
	recs.append(si)

all_dic = {}
dic = {}

replace = {}
replace['radio telescope, radio reflector'] = 'eiffel tower'
replace['stupa, tope']='eiffel tower'
replace['obelisk']='eiffel tower'
replace['church, church building']='eiffel tower'
replace['drilling platform, offshore rig']='eiffel tower'
replace['bolo tie, bolo, bola tie, bola']='peace for paris'
replace['book jacket, dust cover, dust jacket, dust wrapper']='poster' 
replace['envelope']='poster'
replace['crane']='eiffel tower'

def repo(x):
	if x in replace:
		return replace[x]
	return x


for x in recs:
	tag = x['text']
	if repo(tag) in all_dic:
		dic[repo(tag)] += 1
		all_dic[repo(tag)].append(x['filename']) 
	else:
		dic[repo(tag)] = 1
		all_dic[repo(tag)] = [x['filename']]


ka = sorted(dic,key = dic.get, reverse=True)

for x in ka[0:5]:
	print x
	# for y in all_dic[x]:
		# print y
