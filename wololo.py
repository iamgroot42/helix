import precog_testing.classify_image as c
import sys
import os

dirr = os.path.expanduser(sys.argv[1])

print c.run_inference_on_images(dirr,"oh","wello")
