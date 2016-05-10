import numpy as np
import cv2
import os
import Image


def is_image_ok(fn):
    try:
        Image.open(fn)
        return True
    except:
        return False


path = "Images/"
images = os.listdir(path)

for x in images:
		a = cv2.imread(path + x)
		if a is None:
			print "Deleting " + x
			os.remove(path + x)
		if not is_image_ok(path+x):
			print "Deleting " + x
			os.remove(path + x)


print "Done deleting invalid images"
