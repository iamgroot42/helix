from PIL import Image, ImageFile
import ImageChops
import os
import imghdr
import sys
import operator
import math

ImageFile.LOAD_TRUNCATED_IMAGES = True

def equal(A, B):
    widtha, heighta = A.size
    widthb, heightb = B.size
    if widtha != widthb or heighta != heightb:
        return False
    A = A.convert('RGB')
    B = B.convert('RGB')
    histA = A.histogram()
    histB = B.histogram()
    rms = math.sqrt(reduce(operator.add,
    map(lambda a,b: (a-b)**2, histA, histB))/len(histA))
    return (rms==0)


def remove_duplicates(path):
    images = os.listdir(path)
    i = 0
    for x in images:
        i += 100
        base = float(len(images))
        counter = 0
        for y in images:
            if x != y:
                try:
                    a = Image.open(path + "/" +x)
                    b = Image.open(path + "/" + y)
                    fsizea = os.path.getsize(path + "/" +x) 
                    fsizeb = os.path.getsize(path + "/" +y) 
                    if fsizea == fsizeb:
                        if equal(a,b):
                            counter += 1
                            if counter > 1:
                                print "Deleting",y
                                os.remove(path + "/" + y)   
                except:
                    continue
        images = os.listdir(path)
    return True


def delete_invalid(path):
    mapp = {'JPEG':'jpg','PNG':'png'}
    images = os.listdir(path)
    for x in images:
        paath = path + "/" + x
        try:
            img = Image.open(paath)
            z = img.format
            if mapp[z] != x.split('.')[1]:
                print x
                newn = x.split('.')[0] + "." + mapp[z]
                os.rename(paath, path + "/" + newn)
            if z != 'JPEG' and z !='PNG':
                os.remove(paath) 
        except:
            os.remove(paath)  
    return True


if __name__ == "__main__":
    path = os.path.expanduser(sys.argv[1])
    delete_invalid(path)
    remove_duplicates(path)
