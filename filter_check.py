import cv2
import numpy as np


def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err


def satisfy(b,c):
	one_third = c.shape[1]/3
	# Image with filter
	blue = c[:,:one_third,:]
	blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
	white = c[:,one_third:2*one_third,:]
	white = cv2.cvtColor(white, cv2.COLOR_BGR2GRAY)
	red = c[:,2*one_third:,:]
	red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
	# Image without filter
	left = b[:,:one_third,:]
	left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
	middle = b[:,one_third:2*one_third,:]
	middle = cv2.cvtColor(middle, cv2.COLOR_BGR2GRAY)
	right = b[:,2*one_third:,:]
	right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
	# Threshold calculation
	factor = 0
	foo = cv2.equalizeHist(red)
	bar = cv2.equalizeHist(right)
	factor = max(factor,mse(foo,bar))
	foo = cv2.equalizeHist(white)
	bar = cv2.equalizeHist(middle)
	factor = max(factor,mse(foo,bar))
	foo = cv2.equalizeHist(blue)
	bar = cv2.equalizeHist(left)
	factor = max(factor,mse(foo,bar))
	return factor

	
# Tried stuff:
# z = cv2.resize(a,b.shape[:2])

# filtered = cv2.addWeighted(z,0.6,b,0.4,0)


# q = c - filtered

# tt =  b-c
# cv2.imshow('diff',tt)


# p1 = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
# p2 = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

# q =p1-p2

# p1 = q[:,:q.shape[0]/3,:]
# p2 = z[:,:q.shape[0]/3,:]

# OPENCV_METHODS = (
# 	("Correlation", cv2CV_COMP_CORREL),
# 	("Chi-Squared", cv2CV_COMP_CHISQR),
# 	("Intersection", cv2CV_COMP_INTERSECT), 
# 	("Hellinger", cv2CV_COMP_BHATTACHARYYA))

# d = cv2.compareHist(p1, p2, cv2.CV_COMP_CORREL)
# print d

# b,g,r = cv2.split(q)


# b1,g1,r1 = cv2.split(z)
# b2,g2,r2 = cv2.split(q)

# p1 = r1[:,:q.shape[0]/3]
# p2 = r2[:,:q.shape[0]/3]

# p1 = cv2.blur(p1,(9,9))	

# p1[:,:,0] = 0
# p2[:,:,0] = 0

