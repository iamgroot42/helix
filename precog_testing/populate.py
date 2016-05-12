import tweepy
import requests
import os


def download(consumer_key, consumer_secret, access_token, access_token_secret, path):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	public_tweets = api.home_timeline()
	j = 1
	for tweet in public_tweets:
		try:
			link = tweet.entities['media'][0]['media_url']
			r = requests.get(link)
			i = Image.open(StringIO(r.content))
			i.save(path + "/twitter_" + str(j) + ".jpeg")
			j += 1
		except:
			continue
	return True
