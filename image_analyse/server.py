import face, tag

from flask import Flask, request

from PIL import Image
from scipy import misc
import StringIO
import urllib2

app = Flask(__name__)

clf = None
reader = None
predictor = None


@app.route("/analyze_image",  methods=['POST'])
def analyze_image():
	imagefile = request.files['imagefile']
	img =  imagefile.stream.read()
	try:
		ret_json = {}
		img_array = misc.fromimage(Image.open(StringIO.StringIO(img)))
		ret_json['sentiment'] = face.get_sentiment(clf, reader, predictor, img, img_array)
		ret_json['tag'] = tag.tensor_inference(img)
		return str(ret_json)
	except Exception, e:
		print e
	return "Could not process image"


@app.route("/analyze_url",  methods=['GET'])
def analyze_url():
	image_url = request.args['image_url']
	response = urllib2.urlopen(image_url)
	img = response.read()
	try:
		ret_json = {}
		img_array = misc.fromimage(Image.open(StringIO.StringIO(img)))
		ret_json['sentiment'] = face.get_sentiment(clf, reader, predictor, img, img_array)
		ret_json['tag'] = tag.tensor_inference(img)
		return str(ret_json)
	except Exception, e:
		print e
	return "Could not process image"


if __name__ == "__main__":
    clf, reader, predictor = face.ready()
    tag.ready_graph()
    app.run()
