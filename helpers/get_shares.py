# Author : Prateek
# Modified by : iamgroot42

from pymongo import MongoClient
from multiprocessing import Process
import requests
import json
import time
import sys

from requests.packages import urllib3
urllib3.disable_warnings()

# iOS Messenger token
TOKEN = 'EAADYPcrzZBmcBAApxLbVmdOadj0zkWIZBIBZAjwMTVZCxPqv00yhJYinou3CmsLZAISkoTctrDNdb0GLjl3YK5d712W31chUCyWtOCw5rbbbvgbYXZAVk6MSNNXwzSd5P2ZBTgouiZBuoq90JWDZCrgIuwJA4QTJjEdbVTdexg519tAZDZD'
LIMIT = 1000
USERNAME = ""
PASSWORD = ""

def stalk(fb_id,USERNAME,PASSWORD):
	client = MongoClient()
	client.admin.authenticate(USERNAME,PASSWORD)
	db = client['fb_15k_analysis']
	url = 'https://graph.facebook.com/v2.0/' + str(fb_id) + '/' + 'sharedposts?fields=from&limit=' + str(LIMIT) + '&access_token=' + TOKEN
	resp = json.loads(requests.get(url).text) 
	mine = db[str(fb_id)]
	count = 0
	while resp is not None and count < 10000:
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
			print "damn,son"
			break

		print len(resp['data'])

		for i in resp['data']:
			try:
				uid = i['from']['id']
				mine.insert_one({"ID" : uid})
				count += 1
			except:
				continue

		if 'paging' in resp:
			if 'next' in resp['paging']:
				url = resp['paging']['next']
				resp = json.loads(requests.get(url).text)
			else:
				resp = None
		else:
			resp = None	

	print "Done with",fb_id,":",count


def get_shares(USERNAME,PASSWORD):
	client = MongoClient()
	client.admin.authenticate(USERNAME,PASSWORD)
	db = client['analysis']
	ds = db['data_team_use_2x'].find()
	spam = []
	jobs = []
	for row in ds:
		just_name = row['filename'].split('.')[0]
		spam.append(just_name)
	for idee in spam:
		idee2 = idee.split('__')[0]
		jobs.append(Process(target = stalk, args=(idee2,USERNAME,PASSWORD,)))
	for j in jobs:
		j.start()
	for j in jobs:
		j.join()


if __name__ == "__main__":
	get_shares(sys.argv[1],sys.argv[2])
