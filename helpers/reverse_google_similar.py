from bs4 import BeautifulSoup
import os
import requests


def visual_result_link(filepath):
	searchUrl = 'http://www.google.com/searchbyimage/upload'
	multipart = {'encoded_image': (filepath, open(filepath, 'rb')), 'image_content': ''}

	s = requests.Session()
	response = s.post(searchUrl, files = multipart, allow_redirects=False)
	fetchUrl = response.headers['Location']

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
				AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	req = s.get(fetchUrl, headers = headers)

	soup = BeautifulSoup(req.text.encode('utf-8'), "lxml")

	for link in soup.findAll('a', href=True, text='Visually similar images'):
		zelda = link['href']

	return "http://google.com" + zelda


if __name__ == "__main__":
	print visual_result_link('doge.jpeg')
