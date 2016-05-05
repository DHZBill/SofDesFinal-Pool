# import numpy as np
# import cv2
# img = cv2.imread('withcue.JPG')
# imgray = cv2.imread('withcue.JPG',0)
# img_filt = cv2.medianBlur(imgray, 7)
# img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(img, contours, -1, (255,120,255), 1)
# cv2.imwrite('pool_table_contours.jpg', img)
# # cv2.imwrite('cuecontours.jpg', img_th)

import cv2
import numpy as np
import math

class cue(object):
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

def Track_cue():
	""" Track colored points and get their central positions
	Now using blue and yellow."""
	camera_feed = cv2.VideoCapture(0)

	while(1):

		_,frame = camera_feed.read()

		#Define the threshold for finding blue and yellow object with hsv
		lower_blue = np.array([90,50,50])
		upper_blue = np.array([110,255,255])

		lower_yellow = np.array([20,100,100])
		upper_yellow = np.array([30,255, 255])

		# create masks
		mask_blue = create_mask(frame,lower_blue, upper_blue)
		mask_yellow =create_mask(frame, lower_yellow, upper_yellow)        
		mask = mask_blue + mask_yellow
		
		#find biggest colored objects and get their positions
		blue = find_object(frame, mask_blue)
		yellow = find_object(frame, mask_yellow)
		if blue != None and yellow !=None :
			x,y,w,h = blue
			a,b,c,d = yellow
		# find the two points
			point1 = np.array([x+w/2, y+h/2])
			point2 = np.array([a+c/2, b+d/2])
			pos = point1
			n = point1-point2
			direction = n / math.sqrt(np.dot(n,n))
			# print pos, direction
			CUE = cue(pos,direction)
			print CUE.position, CUE.direction

		#Show the original camera feed with a bounding box overlayed 
		cv2.imshow('frame',frame)
		#Show the contours in a seperate window
		cv2.imshow('mask',mask)
		#Use this command to prevent freezes in the feed
		k = cv2.waitKey(5) & 0xFF
		#If escape is pressed close all windows
		if k == 27:
			break

	cv2.destroyAllWindows() 



if __name__ == '__main__':
	Track_cue()