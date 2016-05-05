"detects balls on the pool table"
import numpy as np
from ball import ball
import cv2

class Image_Detection(object):
	def __init__(self):
		self.ball_list = []
		self.ref_pts = []
		self.lr_walls = []
		self.tb_walls = []

	def write_circles(self,image_name):
		img = cv2.imread(image_name,0)
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
		    self.ball_list.append([i[0],i[1],count])
		    #counter
		    count+=1

		cv2.imwrite('circles.jpg',cimg)

		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return self.ball_list

	def store_points(self,event,x,y,flags,param):
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

	def wall_finder(self,image_name):
		'starting from left wall, click on wall and move counterclockwise around the table'
		img = cv2.imread(image_name)

		cv2.imshow('circles.jpg',img)
		cv2.setMouseCallback('circles.jpg', self.store_points)

if __name__ == '__main__':
	I = Image_Detection()
	I.wall_finder('warped.jpg')
	I.write_circles('warped.jpg')
	print 'left and right walls:',I.lr_walls
	print 'top and bottom walls:',I.tb_walls