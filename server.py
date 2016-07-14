# from multiprocessing import Process
from image_analyse import face

from flask import Flask, request

import numpy
import StringIO
from PIL import Image


app = Flask(__name__)

@app.route("/")
def home():
    return "Up!"


@app.route("/analyze",  methods=['POST'])
def analyze():
	# jobs = []
	imagefile = request.files['imagefile']
	img =  imagefile.stream.read()
	print img
	try:
		img_array = numpy.asarray(Image.open(StringIO.StringIO(img)))
		print face.get_sentiment(img, img_array)
	except Exception, e:
		print e
		print "hain?"
	return "len(ex)"
	# return str(tag.tensor_inference(imagefile.stream.read()))
	# Inceptionv3 tag
	# jobs.append(Process(target = tensor_inference, args=(odd, path,"temporary_storage",left,)))


if __name__ == "__main__":
	# Load inception v3 graph into memory
    # tag.ready_graph()
    app.run()
