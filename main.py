import pygame, math, physics, sys, cv2, calibration, detection
import numpy as np
from ball import ball
from draw_table import Table

if __name__ == '__main__': # so this is currently pseudo-code, and we will need to define these explicit functions that will return specific values
	newImage, oldImage = calibration.calibrateVideoFeed # need a function that will allow for calibration of video feed and return both the sheared and original images
	ballList = detection.detectBalls # need an explicit function to detect balls and return the balls as a list, make sure to define the balls properly as a ball class
	t = Table(ballList)
	while(True):
		cue = detection.detectCue # need a function to detect the cue and return it as something, maybe a line or just two points
		t.ballList = detection.detectBalls
		t.initializeHitFromCue(cue) # need a function to specifically start a hit from the cue point
		t.draw_projection() # need to change this function to handle displaying from new inputs, might be best for it to return an image and handle displaying things in this file