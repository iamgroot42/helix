import face, tag

from flask import Flask, request, make_response, current_app
from multiprocessing import Process, Manager
from pymongo import MongoClient
from datetime import timedelta
from functools import update_wrapper
from textblob import TextBlob


from PIL import Image
from scipy import misc
import StringIO
import urllib2
import pytesseract
import sys
import datetime
import hashlib
import json
import urlparse


app = Flask(__name__)
USERNAME = ''
PASSWORD = ''
ACCESS_TOKEN = 'EAADYPcrzZBmcBAJq6A9p3KjwzTwYRwfCVB1UbUdZBZAPneE3Sa6qAF2c57LwdzFLASWTf1Mg8SkAVaWwWzabkfddAfKE6s3EG8QyO4MnIngdA5eID48PQxZAd0CIZAMC8bwU6NK0nThhvqxQSkLfuCbrm7gxVrMzkv139BPg7RAZDZD'

# Error codes mapping
# 100 : error downloading image
# 101 : not JPEG image
# 102 : unexpected error, contact admin
# 104 : requested FB ID isn't that of an image

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def senti_part(img, img_array, dictio):
	senti_graph = face.ready()
	dictio['sentiment'] = face.get_sentiment(senti_graph, img, img_array)


def tag_part(img, dictio):
	tag_graph = tag.ready_graph()
	dictio['tag'] = tag.tensor_inference(tag_graph, img)


def text_part(temp_image, dictio):
	text = pytesseract.image_to_string(temp_image, lang = 'eng').replace('\n',' ')
	blob = TextBlob(text)
	sentiment = {}
	try:
		if blob.detect_language() == 'en':
			sentiment['Positive'] = (blob.sentiment.polarity + 1.0)/2.0
			sentiment['Negative'] = 1.0 - sentiment['Positive']
	except:
		sentiment = {}	
	dictio['text'] = {'text': text,	'sentiment': sentiment}


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


@app.route("/analyze_image",  methods=['POST'])
def analyze_image():
	try:
		imagefile = request.files['imagefile']
		img =  imagefile.stream.read()
		try:
			return json.dumps(image_summary(img).copy())
		except Exception, e:
			print "Error in server.py:",e
			return json.dumps({"error": 101})
	except Exception, e:
		print "Error in server.py:",e
		return json.dumps({"error": 100})


@app.route("/analyze_fbid",  methods=['GET'])
@crossdomain(origin='*')
def analyze_fbid():
	received = datetime.datetime.now()
	client = MongoClient()
	db = client['image_api']
	db.authenticate(USERNAME, PASSWORD) 
	ds = db['v1.0']
	try:
		fb_id = request.args['id']
		image_url = ""
		graph_url = "https://graph.facebook.com/v2.3/" + fb_id + "?fields=source&access_token=" + ACCESS_TOKEN
		try:
			graph_req = urllib2.Request(graph_url, headers = {'User-Agent': 'Mozilla/5.0'})				
			graph_response = urllib2.urlopen(graph_req)
			graph_obj = json.loads(graph_response.read())
			image_url = graph_obj['source']
			k = image_url.rfind(".png") 
			# If png, request jpg
			if k != -1:
				image_url = image_url[:k] + ".jpg" + image_url[k+1:]
		except Exception,e:
			# Link to external source, extract preview image
			try:
				graph_url = "https://graph.facebook.com/v2.3/" + fb_id + "?fields=picture&access_token=" + ACCESS_TOKEN
				graph_req = urllib2.Request(graph_url, headers = {'User-Agent': 'Mozilla/5.0'})				
				graph_response = urllib2.urlopen(graph_req)
				graph_obj = json.loads(graph_response.read())
				image_url = graph_obj['picture']
				image_url = urlparse.parse_qs(urlparse.urlparse(image_url).query)['url'][0]
			except Exception,e:
				print "Error in server.py:",e
				return json.dumps({"error": 104})
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
		return json.dumps({"error": 100})
	try:
		result = image_summary(img)
		if result == -1:
			return json.dumps({"error": 101})
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
		return json.dumps({"error": 102})


@app.route("/analyze_url",  methods=['GET'])
@crossdomain(origin='*')
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
		return json.dumps({"error": 100})
	try:
		result = image_summary(img)
		if result == -1:
			return json.dumps({"error": 101})
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
		return json.dumps({"error": 102})


if __name__ == "__main__":
	try:
		USERNAME,PASSWORD = sys.argv[1], sys.argv[2]
	except:
		print "python " + sys.argv[0] + " <USERNAME> <PASSWORD>"
		exit()
	app.run(host = '0.0.0.0', processes = 10)
