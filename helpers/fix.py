import os
import sys
from PIL import Image

dirr = os.path.expanduser(sys.argv[1])

mapp = {'JPEG':'jpg','PNG':'png'}

k = 0

for x in os.listdir(dirr):
	paath = dirr + "/" + x
	img = Image.open(paath)
	act = img.format
	named = x.split('.')[1]
	print act,named
	try:
		if mapp[act] != named:
			k += 1
			newn = x.split('.')[0] + "." + mapp[act]
			os.rename(paath, dirr + "/" + newn)
	except:
		continue

print "Fixed",k,"images"
