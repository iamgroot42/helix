import requests
import urllib
from bs4 import BeautifulSoup

url = "http://www.free-ocr.com/"

data = {}
data['userfile_url'] = "https://s-media-cache-ak0.pinimg.com/564x/3a/67/95/3a6795d08de2258767b0956f5e6a356c.jpg"
data['user_screen_width'] = '980'


r = requests.post(url, data = data, proxies=urllib.getproxies())
soup = BeautifulSoup(r.text, 'html.parser')
x = ""
for y in soup.findAll('script'):
	if str(y).find("/FW/") != -1:
		x = str(y)
		break

x = x[x.find("'")+1:]
x = x[:x.find("'")]

hit_url = url + x
while True:
	print "Polling"
	r = requests.get(hit_url)
	if r.text.find("Download as text file: ") != -1:
		break

text = BeautifulSoup(r.text, 'html.parser')
print text.find(id = 'resultarea').text
