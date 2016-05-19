import random
import os
from shutil import copyfile

src = "/home/anshuman/Desktop/Images70K"
dst = "/home/anshuman/Desktop/Images457"

x = os.listdir(src)

y = random.sample(x,457)

for img in y:
	copyfile(src+"/"+img, dst+"/"+img)

print "Done"