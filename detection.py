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
		print lines
		for x1,y1,x2,y2 in lines[0]:
		    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

		cv2.imshow('circles.jpg',img)

		# img = cv2.imread(image_name)
		# imgray = cv2.imread(image_name,0)
		# img_filt = cv2.medianBlur(imgray, 7)
		# img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
		# print img_filt
		# #contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

		# #cv2.drawContours(img, contours, -1, (255,120,255), 1)
		# #cv2.imwrite('pool_table_contours.jpg', img)
		# cv2.imwrite('pool_table_contours.jpg', img_th)

	def calibrate_interface(self,file_name):
	    '''
	    Runs the four-point click calibration process.
	    Click in order: top-left, top-right, bottom-right, bottom-left

	    Inputs:
	    file_name: a string that points to the image used for specifying the corners
	    '''

	    img = cv2.imread(file_name) # set input image
	    # initialize the window and set interaction function
	    cv2.namedWindow('original')
	    cv2.setMouseCallback('original', store_points)

	    while True:
	        # display the input image
	        cv2.imshow('original',img)

	        # wait until there have been 4 clicks
	        if len(ref_pts) > 3:
	            pts = np.array(ref_pts)
	            warped = four_point_transform(img, pts)
	            #display the transformed image
	            cv2.imshow('warped', warped)
	            cv2.waitKey(0)
	            break

	        #press esc to exit
	        key = cv2.waitKey(10)
	        if key == 27:
	            raise RuntimeError('User escaped the four-point calibration process')
	            break
	    cv2.destroyAllWindows

if __name__ == '__main__':
	I = Image_Detection()
	#I.wall_finder('warped.jpg')
	I.calibrate_interface('pool_pic.JPG')
	I.write_circles('warped.jpg')