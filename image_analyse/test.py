import face
from scipy import misc
from PIL import Image

import StringIO
y = Image.open("a.jpg")

output = StringIO.StringIO()

y.save(output, format='jpeg')

contents = output.getvalue()

output.close()

edx = misc.imread("a.jpg")
# print edx

print edx.shape

print "yo _v_"
face.ready_sentigraph()

# print contents
# print dir(y)

print face.get_sentiment(contents, edx)