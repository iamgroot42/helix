import os
import classify_image as ce
from pymongo import MongoClient


def push_to_db(path = "/Images/"):
	client = MongoClient('mongodb://localhost:27017/')
	db = client.tensorflow_tags
	table = db.tags

	directory = os.getcwd() + path
	results = {}

	for img in os.listdir(directory):
		x = ce.run_inference_on_image(directory + img,1)
		(tag, confidence), = x.items()
		table.insert_one( { "filename": img, "tag": tag, "confidence": str(confidence)} )
		print "..."

	return True
