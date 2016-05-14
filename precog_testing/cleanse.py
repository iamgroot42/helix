from PIL import Image,  ImageFile
import ImageChops
import os
import imghdr
import operator
import math

ImageFile.LOAD_TRUNCATED_IMAGES = True

def equal(A, B):
    histA = A.histogram()
    histB = B.histogram()
    rms = math.sqrt(reduce(operator.add,
    map(lambda a,b: (a-b)**2, histA, histB))/len(histA))
    return (rms==0)


def remove_duplicates(path):
    images = os.listdir(path)
    for x in images:
        for y in images:
            if x != y:
                try:
                    a = Image.open(path + "/" +x)
                    b = Image.open(path + "/" + y)
                    if equal(a,b):
                        print "Deleting " + y
                        os.remove(path + "/" + y)  
                except:
                    continue
        images = os.listdir(path)
    return True


def is_image_ok(fn):
    if imghdr.what(fn) == 'jpeg':
        return True
    return False


def delete_invalid(path):
    images = os.listdir(path)
    for x in images:
        if not is_image_ok(path + "/" + x):
            print "Deleting " + x
            os.remove(path + "/" + x)
    return True
