"detects balls on the pool table"
import numpy as np
from ball import ball
import cv2

class Image_Detection(object):
	def __init__(self):
		self.ball_list=[]

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

	def wall_finder(self,image_name):
		img = cv2.imread(image_name)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,10,200)

		minLineLength = 500
		maxLineGap = 10
		lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength,maxLineGap)
		for x1,y1,x2,y2 in lines[0]:
		    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

		cv2.imshow('circles.jpg',img)

		# lines = cv2.HoughLines(edges,1,np.pi/180,200)
		# for rho,theta in lines[0]:
		#     a = np.cos(theta)
		#     b = np.sin(theta)
		#     x0 = a*rho
		#     y0 = b*rho
		#     x1 = int(x0 + 1000*(-b))
		#     y1 = int(y0 + 1000*(a))
		#     x2 = int(x0 - 1000*(-b))
		#     y2 = int(y0 - 1000*(a))

		#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

		# cv2.imshow('circles.jpg',img)

if __name__ == '__main__':
	I = Image_Detection()
	I.wall_finder('warped.jpg')
	I.write_circles('warped.jpg')