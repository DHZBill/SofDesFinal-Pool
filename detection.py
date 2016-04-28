"detects balls on the pool table"
import numpy as np
import cv2

# img = cv2.imread('pool_pic.JPG')
# imgray = cv2.imread('pool_pic.JPG',0)
# img_filt = cv2.medianBlur(imgray, 7)
# img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# #contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# #cv2.drawContours(img, contours, -1, (255,120,255), 1)
# #cv2.imwrite('pool_table_contours.jpg', img)
# cv2.imwrite('pool_table_contours.jpg', img_th)


img = cv2.imread('warped.jpg',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,
                            param1=50,param2=23,minRadius=0,maxRadius=150)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


r = 1800.0 / cimg.shape[1]
dim = (1800, int(cimg.shape[0]*r))
resized = cv2.resize(cimg,dim,interpolation = cv2.INTER_AREA)
cv2.imwrite("resized.jpg",resized)

cv2.waitKey(0)
cv2.destroyAllWindows()