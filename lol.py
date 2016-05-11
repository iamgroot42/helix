import numpy as np
import cv2
import os
import sys
import filter_check

path = sys.argv[1]

x = cv2.imread(path)

results = filter_check.has_flag_filter(x, 4)
left = results[0]
middle = results[1]
right = results[2]
print "Left: ",left
print "Middle: ",middle
print "Right: ",right