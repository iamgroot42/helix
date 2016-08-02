import face, tag

from flask import Flask, request
from multiprocessing import Process, Manager
from pymongo import MongoClient

from PIL import Image
from scipy import misc
import StringIO
import urllib2
import pytesseract
import sys
import datetime
import hashlib
import json


app = Flask(__name__)
USERNAME = ''
PASSWORD = ''


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
	if temp_image.format == "PNG":
		return -1
	elif temp_image.format != "JPEG":
		return -1
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
	return handle(d)


def handle(x):
	if not (x['tag']):
		return -1
	else:
		return x


# @app.route("/analyze_image",  methods=['POST'])
# def analyze_image():
# 	imagefile = request.files['imagefile']
# 	img =  imagefile.stream.read()
# 	try:
# 		return str(image_summary(img))
# 	except Exception, e:
# 		print e
# 	return "JPEG/PNG expected", 400


@app.route("/analyze_url",  methods=['GET'])
def analyze_url():
	received = datetime.datetime.now()
	client = MongoClient()
	db = client['image_api']
	db.authenticate(USERNAME, PASSWORD) 
	ds = db['v1.0']
	try:
		image_url = request.args['image_url']
		req = urllib2.Request(image_url, headers = {'User-Agent': 'Mozilla/5.0'})
		response = urllib2.urlopen(req)
		img = response.read()
		cache = ds.find({'_id': image_url})
		# Check if result is available in cache
		if cache.count():
			if cache[0]['size'] == len(img) and cache[0]['md5'] == hashlib.md5(img).hexdigest():
				print "cache hit"
				return cache[0]['result']
	except Exception,e:
		print "Error in server.py:",e
		return "Error downloading image for analysis", 401
	try:
		result = image_summary(img)
		if result == "-1":
			return "JPEG/PNG expected", 400
		else:
			cache_it = json.dumps(result.copy())
			md5_hash = hashlib.md5(img).hexdigest()
			now = datetime.datetime.now()
			data_entry = {
				'_id': image_url, 'size': len(img), 'result': cache_it,
				'timestamp': received, 'md5': md5_hash, 'headers':request.headers['User-Agent'],
				'time taken': (now-received).total_seconds() * 1000.0
			}
			ds.insert_one(data_entry)
			return cache_it
	except Exception, e:
		print "Error in server.py:",e
		return "Unexpected error", 402


if __name__ == "__main__":
	try:
		USERNAME,PASSWORD = sys.argv[1], sys.argv[2]
	except:
		print "python " + sys.argv[0] + " <USERNAME> <PASSWORD>"
		exit()
	app.run(host = '0.0.0.0', processes = 10)
