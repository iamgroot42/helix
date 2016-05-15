import cv2
import numpy as np


def has_flag_filter(a, threshold = 4.5):
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
	if max(M)-min(M) <= 70:
		indicator +=1
		# Higher value -> more white:
		if min(M) >= 150:
			indicator += 0.5
	print indicator
	if indicator >= threshold:
		return True
	else:
		return False
