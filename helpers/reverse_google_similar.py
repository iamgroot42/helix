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
	# Google may block
	time.sleep(3)
	fetchUrl = response.headers['Location']

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)\
				Chrome/41.0.2228.0 Safari/537.36'}

	req = s.get(fetchUrl, headers = headers)

	soup = BeautifulSoup(req.text.encode('utf-8'), "lxml")

	for link in soup.findAll('a', href=True, text='Visually similar images'):
		zelda = link['href']
	try:
		return "http://google.com" + zelda
	except:
		return None


def list_it(src,dest,scraper_path,images):
	for x in images:
		path = dest + '.'.join(x.split('.')[:-1])
		os.mkdir(path)
		argument = visual_result_link(src + x)
		if argument is None:
			print x
			continue
		argument = argument.replace('&','\&')
		path = path.replace(' ','\ ').replace(')','\)').replace('(','\(')
		command = "node " + scraper_path + " " + argument + " > "  + path + "/names"
		os.system(command)
		time.sleep(3)


if __name__ == "__main__":
	src = os.path.expanduser(sys.argv[1])
	dest = os.path.expanduser(sys.argv[2])
	scraper_path = os.path.expanduser(sys.argv[3])

	ncores = 10
	jobs = []
	images = os.listdir(src)
	csize = len(images)/ncores
	for i in range(0, len(images), csize):
		chunk = images[i:i + csize]
		jobs.append(Process(target = list_it, args=(src,dest,scraper_path,chunk)))

	for j in jobs:
		j.start()

	for j in jobs:
		j.join()

	print "Done"
