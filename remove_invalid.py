import numpy as np
import cv2
import os
import imghdr


def is_image_ok(fn):
	print imghdr.what(fn)
	if imghdr.what(fn) == 'jpeg':
		return True
	return False


path = "Images/"
images = os.listdir(path)
print images

for x in images:
		a = cv2.imread(path + x)
		if a is None:
			print "Deleting " + x
			os.remove(path + x)
		if not is_image_ok(path+x):
			print "Deleting " + x
			os.remove(path + x)


print "Done deleting invalid images"
