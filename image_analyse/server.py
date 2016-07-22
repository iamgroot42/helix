import face, tag

from flask import Flask, request

from PIL import Image
from scipy import misc
import StringIO
import urllib2
import pytesseract

app = Flask(__name__)


def image_summary(img):
	ret_json = {}
	temp_image = Image.open(StringIO.StringIO(img))
	img_array = misc.fromimage(temp_image)
	ret_json['sentiment'] = face.get_sentiment(img, img_array)
	ret_json['tag'] = tag.tensor_inference(img)
	ret_json['text'] = pytesseract.image_to_string(temp_image, lang = 'eng')
	if not ( ret_json['tag']):
		ret_json = -1
	return handle(ret_json)


def handle(x):
	if x == -1:
		return "Not JPEG/PNG or file size is too big"
	else:
		return x


@app.route("/analyze_image",  methods=['POST'])
def analyze_image():
	imagefile = request.files['imagefile']
	img =  imagefile.stream.read()
	try:
		return str(image_summary(img))
	except Exception, e:
		print e
	return "Could not process image"


@app.route("/analyze_url",  methods=['GET'])
def analyze_url():
	try:
		image_url = request.args['image_url']
		req = urllib2.Request(image_url, headers = {'User-Agent': 'Mozilla/5.0'})
		response = urllib2.urlopen(req)
		img = response.read()
	except Exception,e:
		print e
		return "Error downloading image for analysis."
	try:
		return str(image_summary(img))
	except Exception, e:
		print e
		return "Could not process image"


if __name__ == "__main__":
    face.ready()
    tag.ready_graph()
    app.run(host = '0.0.0.0')
