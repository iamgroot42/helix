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


def has_flag_filter(a, threshold):
	one_third = a.shape[1]/3
	left = a[:,:one_third,:]
	middle = a[:,one_third:2*one_third,:]
	right = a[:,2*one_third:,:]
	# 3 thirds of image; BGR values (mean):
	L = [left[:,:,0].mean(), left[:,:,1].mean(), left[:,:,2].mean()]
	M = [middle[:,:,0].mean(), middle[:,:,1].mean(), middle[:,:,2].mean()]
	R = [right[:,:,0].mean(), right[:,:,1].mean(), right[:,:,2].mean()]
	indicator = 0
	# Red should be prominent, other values shouldn't be comparable (close to gray/white) or too high (white):
	if np.argmax(R) == 2 and R[0]<=200 and R[1]<=200 and max(R)-min(R) >= 15:
		indicator += 1
		# Higher value -> more red:
		if max(R) >= 150:
			indicator += 0.5 
	# Blue should be prominent, other values shouldn't be comparable (close to gray/white) or too high (white):
	if np.argmax(L) == 0 and L[1]<=200 and L[2]<=200 and max(L)-min(L) >= 15:
		indicator += 1
		# Higher value -> more blue:
		if max(L) >= 150:
			indicator += 0.5
	# All values should be close together (white/gray):
	if max(M)-min(M) <= 40:
		indicator +=1
		# Higher value -> more white:
		if min(M) >= 150:
			indicator += 0.5
	# return [L,M,R]
	if indicator >= threshold:
		return True
	else:
		return False
