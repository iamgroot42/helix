import os
import imghdr


def is_image_ok(fn):
	if imghdr.what(fn) == 'jpeg':
		return True
	return False

def delete_invalid(path = "Images/"):
	images = os.listdir(path)
	for x in images:
		if not is_image_ok(path+x):
			print "Deleting " + x
			os.remove(path + x)
	return True
