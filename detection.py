"detects balls on the pool table"
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')

while(True):
    # Capture frame-by-frame
	ret, frame = cap.read()
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	for (x,y,w,h) in faces:
		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)

		cv2.circle(frame, (x+3*w/10, y+8*w/20),w/9,(0,0,0),-1)
		cv2.circle(frame, (int(x+w*(.7)), y+8*w/20),w/9,(0,0,0),-1)

		cv2.rectangle(frame,(x+w/5,y+7*w/20),(x+2*w/5,y+9*w/20),(255,255,255),-1)
		cv2.rectangle(frame,(x+3*w/5,y+7*w/20),(x+4*w/5,y+9*w/20),(255,255,255),-1)

		cv2.ellipse(frame, (int(x+w*0.5), int(y+h*0.75)), (int(w*0.20), int(0.07*h)), 0, 0, 180, (0,0,0), thickness=8)      
    # Display the resulting frame
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()