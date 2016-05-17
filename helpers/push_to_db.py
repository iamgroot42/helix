import os
import precog_testing.classify_image as c

path = os.path.expanduser("~/Desktop/Images5K")
json = os.path.expanduser("~/Desktop/results.json")

print c.run_inference_on_images(path,json)