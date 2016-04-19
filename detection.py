"detects balls on the pool table"
import numpy as np
import cv2
img = cv2.imread('pool_table.jpg')
imgray = cv2.imread('pool_table.jpg',0)
img_filt = cv2.medianBlur(imgray, 7)
img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (255,255,255), 1)
cv2.imwrite('pool_table_contours.jpg', img)





# cap = cv2.VideoCapture(0)

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Display the resulting frame
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()