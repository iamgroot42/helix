from collections import Counter
from sets import Set
from PIL import Image
import precog_testing.cleanse as c
import os

ims = os.listdir('fbparis_images')
disc = {}
lolol = {}

# Get objectIDs from folder
for row in ims:
	key = row.split('__')[0]
	lolol[key] = row
	if key in disc:
		disc[key] += 1
	else:
		disc[key] = 1


wololo = 1
# Club same images together
for k in disc.keys():
	print wololo
	wololo += 1
	for p in disc.keys():
		oh = Image.open('fbparis_images/' + lolol[k])
		ho = Image.open('fbparis_images/' + lolol[p])
		if k == p:
			continue
		if c.equal(oh,ho):
			# Remove duplicate
			disc[k] += disc[p]
			del disc[p]

# Sort by frequency
c = sorted(disc, key = disc.get, reverse = True)[:1000]
lel = 0
for k,v in c:
	lel += v

f = open('actual_spam_fast.txt','r')

z = Set()
for x in f:
	z.add(x.split('__')[0])

f.close()
c1 = c2 = 0
for k,v in c:
	if k in z:
		print k
		c1 += 1
		c2 += v

print "\n"
print "Spam images out of 1000 ",c1
print "Spam images out of ",lel," ",c2

f2 = open('topk.txt','w')

for k,v in c:
	f2.write(k + "\n")

f2.close()
