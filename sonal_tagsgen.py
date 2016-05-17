import os
import precog_testing.classify_image as c

a = ["charlie","kejriwalInsultsHanuman","Kulkarni","RR","Shani"]
b = ["similar","dissimilar"]

for x in a:
	for y in b:
		potato = os.path.expanduser("~/Desktop/images_sonal/"+x+"/"+y)
		print c.run_inference_on_images(path=potato,db_name=x,collection_name=y,num_top_predictions=3)
