import numpy as np
import cv2
import os
import filter_check


path = "Images/"
images = os.listdir(path)


for x in images:
        b = cv2.imread(path + x)
        for y in images:
        	if x != y:
        		c = cv2.imread(path + y)
        		if b.shape == c.shape:
        			zeta = filter_check.satisfy(b,c)
        			if zeta < 150:
        				print "Superb"
        				print x," and ",y
        			elif zeta < 200:
        				print "K"
        				print x," and ",y
        			elif zeta < 250:
        				print "Meh"
        				print x," and ",y

print "Done"
