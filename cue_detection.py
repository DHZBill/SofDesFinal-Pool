import cv2
import numpy as np
import math

class cue(object):
	""" Create a new class to represent the cue"""
	def __init__(self, position, direction):
		self.position = position
		self.direction = direction

def create_mask(frame, lower, upper):
	""" Create mask for specified color threshold """
	#Convert the current frame to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# #Create a binary image, where anything blue and yellow appears white and everything else is black
	mask = cv2.inRange(hsv, lower, upper)
	#Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
	element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	mask = cv2.erode(mask, element, iterations=2)
	mask = cv2.dilate(mask, element, iterations=2)
	mask = cv2.erode(mask, element)
	return mask

def find_object(frame, mask):
	""" Find colored points on the cue"""
	# Create contours
	contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	maximumArea = 0
	bestContour = None
	for contour in contours:
		currentArea = cv2.contourArea(contour)
		if currentArea > maximumArea :
			bestContour = contour
			maximumArea = currentArea

	 #Create a bounding box around the biggest blue and yellow objects
	if bestContour is not None:
		x,y,w,h = cv2.boundingRect(bestContour)
		cv2.rectangle(frame, (x,y),(x+w,y+h), (0,0,255), 3)
		return x,y,w,h
	else:
		return None

def Track_cue(frame):
	""" Track colored points and get their central positions
	Now using blue and yellow."""

	#Define the threshold for finding blue and yellow object with hsv
	lower_blue = np.array([90,50,50])
	upper_blue = np.array([110,255,255])

	lower_yellow = np.array([20,100,100])
	upper_yellow = np.array([30,255, 255])

	# create masks
	mask_blue = create_mask(frame,lower_blue, upper_blue)
	mask_yellow =create_mask(frame, lower_yellow, upper_yellow)        
	mask = mask_blue + mask_yellow
	
	# find biggest colored objects and get their positions
	blue = find_object(frame, mask_blue)
	yellow = find_object(frame, mask_yellow)
	# find the position of two points
	if blue != None and yellow !=None :
		x,y,w,h = blue
		a,b,c,d = yellow
		point1 = np.array([x+w/2, y+h/2])
		point2 = np.array([a+c/2, b+d/2])
		pos = point1
		n = point1-point2
		direction = n / math.sqrt(np.dot(n,n))
		return point1, point2


	