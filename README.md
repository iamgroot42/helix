## precog_testing

### Setting it up

- Prerequisites : `tensorflow` and `opencv 3` 
- `sudo python setup.py install` to install the package


### 'cleanse'

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
