import numpy as np
import cv2
import os

def mse(imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

path = "Images/"
images = os.listdir(path)


for x in images:
        for y in images:
                if x != y:
                        try:
                                a = cv2.imread(path + x)
                                b = cv2.imread(path + y)
                        except:
                                continue
                        if b is None:
                                print "Weird"
                                try:
                                        os.remove(path+y)
                                except:
                                        print "damn weird"
                        if a is None:
                                print "Weird^2"
                                try:
                                        os.remove(path+x)
                                        images = os.listdir(path)
                                except:
                                        print "mega weird"
                                continue
                        if a.shape == b.shape:
                                a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
                                b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
                                di = mse(a,b)
                                if (di).is_integer and int(di) == 0:
                                        print "Deleting " + y
                                        os.remove(path + y)
        images = os.listdir(path)


print "Done matching images"
