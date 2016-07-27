import face, tag

from flask import Flask, request
from multiprocessing import Process, Manager
from pymongo import MongoClient

from PIL import Image
from scipy import misc
import StringIO
import urllib2
import pytesseract

app = Flask(__name__)
USERNAME = 'anshumans'
PASSWORD = '@nshumaN'

def senti_part(img, img_array, dictio):
	senti_graph = face.ready()
	dictio['sentiment'] = face.get_sentiment(senti_graph, img, img_array)


def tag_part(img, dictio):
	tag_graph = tag.ready_graph()
	dictio['tag'] = tag.tensor_inference(tag_graph, img)


def text_part(temp_image, dictio):
	dictio['text'] = pytesseract.image_to_string(temp_image, lang = 'eng').replace('\n',' ')


def image_summary(img):
	temp_image = Image.open(StringIO.StringIO(img))
	img_array = misc.fromimage(temp_image)
	# Shared dictionary
	manager = Manager()
	d = manager.dict()
	p1 = Process(target = senti_part, args = (img, img_array, d,))
	p2 = Process(target = tag_part, args = (img, d,))
	p3 = Process(target = text_part, args = (temp_image, d,))
	# Start all processes
	p1.start()
	p2.start()
	p3.start()
	# Join all processes
	p1.join()
	p2.join()
	p3.join()
	# if not ( ret_json['tag']):
		# ret_json = -1
	return d
	# return handle(ret_json)


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
	client = MongoClient()
	db = client['image_api']
	# db.authenticate(USERNAME, PASSWORD) 
	ds = db['v1.0']
	try:
		image_url = request.args['image_url']
		req = urllib2.Request(image_url, headers = {'User-Agent': 'Mozilla/5.0'})
		response = urllib2.urlopen(req)
		img = response.read()
		cache = ds.find({'_id':image_url})
		# Check if result is available in cache
		if cache.count():
			if cache[0]['size'] == len(img):
				return cache[0]['result']
	except Exception,e:
		print e
		return "Error downloading image for analysis."
	try:
		cache_it = str(image_summary(img))
		ds.insert_one({'_id':image_url, 'size':len(img), 'result': cache_it})
		return cache_it
	except Exception, e:
		print e
		return "Could not process image"


if __name__ == "__main__":
	app.run(host = '0.0.0.0')
