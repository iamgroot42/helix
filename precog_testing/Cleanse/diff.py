from PIL import Image
import os
import ImageChops


def equal(imageA, imageB):
    return ImageChops.difference(imageA, imageB).getbbox() is None


def remove_duplicates(path = "Images/"):
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
                os.remove(path + y)  
        images = os.listdir(path)
    return True
