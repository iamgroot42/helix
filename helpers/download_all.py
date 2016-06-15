import os
import sys


def potato(path):
	files = os.listdir(path)
	for x in files:
		z = []
		name = x.replace(' ','\ ').replace(')','\)').replace('(','\(')
		try:
			f = file(path + name + '/names','r')
			for x in f:
				z.append(x.rstrip())
			g = file(path + name + '/download','w')
			for x in z:
				g.write(x + "\n")
		except:
			os.rmdir(path + name)


def tomato(path):
	files = os.listdir(path)
	for x in files:
		name = x.replace(' ','\ ').replace(')','\)').replace('(','\(')
		os.remove(path + name + '/names')


def avocado(path):
	files = os.listdir(path)
	for x in files:
		os.remove(path + name + '/download')	


if __name__ == "__main__":
	potato(sys.argv[1])
	tomato(sys.argv[1])
	avocado(sys.argv[1])