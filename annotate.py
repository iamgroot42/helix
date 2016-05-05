import tweepy
import requests
import os
from argparse import ArgumentParser
from PIL import Image
from StringIO import StringIO
# Local import :
import classify_image as ce


consumer_key = "nHrvcQR1ge7RCtjyiKa2iGHZV"
consumer_secret = "hTQRfDNm7b49whxPmfScd5Tyn636IyFZynWrWRE3gELG4ALBu4"

access_token = "364720387-mmYxkg0rMDHvRm7P0DAwIImSeJZuDgdUaUHhzPej"
access_token_secret = "6kPzmtoPg5WHijCofSrIDYdKMy3x8E03wpo9ktCxpXzMM"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


parser = ArgumentParser()
parser.add_argument('-d', action='store_true')
args = parser.parse_args()


if args.d:
	public_tweets = api.home_timeline()
	j = 1
	for tweet in public_tweets:
		try:
			link = tweet.entities['media'][0]['media_url']
			r = requests.get(link)
			i = Image.open(StringIO(r.content))
			i.save("Images/"+str(j)+".jpeg")
			j += 1
		except:
			continue

directory = os.getcwd() + "/Images/"
results = {}

for img in os.listdir(directory):
	x = ce.run_inference_on_image(directory + img,1)
	results[img] = x
	print "..."

for x in results:
	print x,":",
	print results[x]
