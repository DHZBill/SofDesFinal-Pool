"detects balls on the pool table"
import numpy as np
from ball import ball
import cv2

class Image_Detection(object):
	'''
	detects balls and walls
	returns x and y coords of balls in ball_list
	returns x coord of left and right walls in lr_walls
	returns y coord of top and bottom walls in tb_walls
	'''
	def __init__(self):
		self.ball_list = []
		self.ref_pts = []
		self.lr_walls = []
		self.tb_walls = []

	def write_circles(self,img):
		'''
		draws circles around all the balls that are detected
		returns the x,y coords of the balls as well as the ball number
		'''
		# img = cv2.imread(img,0)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.medianBlur(img,5)
		cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

		circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,30,
		                            param1=50,param2=23,minRadius=0,maxRadius=126)

		circles = np.uint16(np.around(circles))

		count = 0
		for i in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
		    #ball_list
		    self.ball_list.append(ball(i[0],i[1],count))
		    #counter
		    count+=1

		cv2.imwrite('circles.jpg',cimg)

		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return self.ball_list

	def store_points(self,event,x,y,flags,param):
		'''
		stores the coordinates of a point if left-click is pressed
		'''
	    if event == cv2.EVENT_LBUTTONDOWN:
	        coords = (x, y)

	        if len(self.ref_pts) == 3:
	        	cv2.destroyAllWindows()

	        if len(self.ref_pts) % 2 == 1:
	        	self.ref_pts.append(coords)
	        	self.tb_walls.append(coords[1])
	        else:
	        	self.ref_pts.append(coords)
	        	self.lr_walls.append(coords[0])

	def wall_finder(self,img):
		'''
		starting from left wall, click on wall and move clockwise around the table
		stores the wall coords in a list
		'''
		# img = cv2.imread(img)

		cv2.imshow('walls',img)
		cv2.setMouseCallback('walls', self.store_points)

if __name__ == '__main__':
	pass
	# I = Image_Detection()
	# I.wall_finder('warped.jpg')
	# I.write_circles('warped.jpg')
