from bs4 import BeautifulSoup
import time
import os
import requests
import subprocess
import sys
from multiprocessing import Process


def visual_result_link(filepath):
	searchUrl = 'http://www.google.com/searchbyimage/upload'
	multipart = {'encoded_image': (filepath, open(filepath, 'rb')), 'image_content': ''}
	s = requests.Session()
	response = s.post(searchUrl, files = multipart, allow_redirects=False)
	fetchUrl = response.headers['Location']

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
				AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	req = s.get(fetchUrl, headers = headers)
	soup = BeautifulSoup(req.text.encode('utf-8'), "lxml")
	zelda = None
	for link in soup.findAll('a', href=True, text='Visually similar images'):
		zelda = "http://google.com" + link['href']
		break
	return zelda


def list_it(src,dest,scraper_path):
	images = os.listdir(src)
	i = 1
	for x in images:
		path = dest + '.'.join(x.split('.')[:-1])
		argument = visual_result_link(src + x)
		print x
		if argument is None:
			print "Blocked, sleeping for 5 minutes"
			time.sleep(300)
			continue

		os.mkdir(path)
		argument = argument.replace('&','\&')
		path = path.replace(' ','\ ').replace(')','\)').replace('(','\(')
		command = "node " + scraper_path + " " + argument + " > "  + path + "/names"
		os.system(command)
		os.remove(src + x)
		print str(i)
		i += 1


if __name__ == "__main__":
	src = os.path.expanduser(sys.argv[1])
	dest = os.path.expanduser(sys.argv[2])
	scraper_path = os.path.expanduser(sys.argv[3])
	list_it(src,dest,scraper_path)
