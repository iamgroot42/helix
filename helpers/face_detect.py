import dlib
from skimage import io
import sys

detector = dlib.get_frontal_face_detector()

img = io.imread(sys.argv[1])
dets = detector(img, 1)
print len(dets), "faces detected"