## precog_testing

### Setting it up

- Prerequisites : `tensorflow` and `opencv 3` 
- `pip install Pillow --upgrade`
- `sudo python setup.py install` to install the package


### cleanse
```python
import Image
import precog_testing.cleanse as c
a = Image.open("path/to/image")
b = Image.open("path/to/image")
# Check if two images are the same (duplicate detection)
c.equal(a,b)
# Remove all duplicate images from folder
c.remove_duplicates("path/to/images")
# Check if an image is in valid .jpeg format (not corrupt)
c.is_image_ok("path/to/file")
# Delete all invalid .jpeg images from folder
c.delete_invalid("path/to/images")
```

### filter_check
```python
import cv2
import precog_testing.filter_check as f
a = cv2.imread("path/to/image")
# Check if given image has a filter of the 'Flag of France' over it
f.has_flag_filter(a,4.5)
```

### populate
```python
import cv2
import precog_testing.populate as p
# Download images from your twitter feed into given folder
p.download("consumer_key", "consumer_secret", "access_token", "access_token_secret", "path/to/folder")
```

### classify_image
```python
import precog_testing.classify_image as c
# Annotate images in given folder and push results into mongoDB (db:analysis, table:tags)
c.run_inference_on_images("path/to/images","database_name","collection_name")
```
