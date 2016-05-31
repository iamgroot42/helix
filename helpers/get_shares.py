# Author : Prateek
# Modified by : iamgroot42

from pymongo import MongoClient
from multiprocessing import Process
import requests
import json
import time

from requests.packages import urllib3
urllib3.disable_warnings()

# Confosn token: never expires
TOKEN = 'CAAHKAhIiZA9UBAEEbihPGG5kCgd66GUgHYxlGPDz5YFBgCOoE9nLIsZA7rmmwt31R7bI89ppnZBzBdG0gNO8zikyfcqnIQkSZA8aVK9KZBKrUDNg7IeBVZC1tOq9uj6QrHQE0rQMrs8osZBWZAzScx3WywjS8XZCCY1tKUU8NshIZClanNH6cLZAEItzLt7aGSrr7oZD'
LIMIT = 300


def stalk(fb_id):
	client = MongoClient()
	db = client['fb_analysis']
	url = 'https://graph.facebook.com/v2.0/' + str(fb_id) + '/' + 'sharedposts?limit=' + str(LIMIT) + '&access_token=' + TOKEN
	resp = json.loads(requests.get(url).text) 
	mine = db[str(fb_id)]
	count = 0
	while resp is not None and count < 50000:
			if 'error' in resp:
				if resp['error']['code'] == 100:
					break

			if 'data' not in resp:
				if 'error' in resp:
					if resp['error']['code'] == 12:
						break
				time.sleep(180)
				resp = json.loads(requests.get(url).text)
				continue

			if len(resp['data']) == 0:
				break

			for i in resp['data']:
				uid = i['from']['id']
				mine.insert_one({"ID" : uid})
				count += 1

			if 'paging' in resp:
				if 'next' in resp['paging']:
					url = resp['paging']['next']
					resp = json.loads(requests.get(url).text)
				else:
					resp = None
			else:
				resp = None	
	print "Done with",fb_id


def get_shares():
	client = MongoClient()
	db = client['analysis']
	ds = db['tags_with_spam_2'].find()
	spam = []
	jobs = []
	for row in ds:
		if row['spam'] == 1:
			just_name = row['filename'].split('.')[0]
			spam.append(just_name)
	for idee in spam:
		idee2 = idee.split('__')[0]
		jobs.append(Process(target = stalk, args=(idee2,)))
	for j in jobs:
		j.start()
	for j in jobs:
		j.join()


if __name__ == "__main__":
	get_shares()
