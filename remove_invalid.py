import numpy as np
import cv2
import os

path = "Images/"
images = os.listdir(path)

for x in images:
        a = cv2.imread(path + x)
        if a is None:
                print "Deleting " + x
                os.remove(path + x)

print "Done deleting invalid images"

