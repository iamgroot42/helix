import precog_testing.cleanse as c
from multiprocessing import Process


def adele(fol, x):
	c.remove_duplicates("/home/anshumans/Desktop/anshudata/" + fol + "/" + x)
	print "Done for ",fol," : ",x


if __name__ == "__main__":
	z = ['Christ', 'Col', 'Eiffel', 'Pyramid', 'Statue', 'Sydney', 'Taj', 'Tower']
	jobs = []
	for x in z:
		jobs.append(Process(target = adele, args=('Google',x,)))
		jobs.append(Process(target = adele, args=('Bing',x,)))

	for j in jobs:
		j.start()

	for j in jobs:
		j.join()

	print "Done"
