import cv2
import os
import filter_check

path = "Images/"
images = os.listdir(path)

for x in images:
	b = cv2.imread(path + x)
	if filter_check.has_flag_filter(b, 4.5):
		print path + x

