from PIL import Image
import os
import ImageChops
import imghdr


def equal(imageA, imageB):
    return ImageChops.difference(imageA, imageB).getbbox() is None


def remove_duplicates(path):
    images = os.listdir(path)
    for x in images:
        for y in images:
            if x != y:
                try:    
                    a = Image.open(path + x)
                    b = Image.open(path + y)
                except:
                    continue
            if equal(a,b):
                os.remove(path + "/" + y)  
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
            os.remove(path + x)
    return True
