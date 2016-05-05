import pygame, math, physics, sys, cv2, calibration
import numpy as np
from ball import ball
from draw_table import Table
from detection import Image_Detection as ImD

def activeProjection(): #input is a table object
	# cap = cv2.VideoCapture(0)
	# ret, frame = cap.read()
	img, warped, pts = calibration.calibrate_interface('pool_pic.JPG') # returns the original image, the sheared image, and the points used to warp the image
	I = ImD()
	I.wall_finder(warped)
	ballList = I.write_circles(warped)
	t = Table(ballList)
	screen = pygame.display.set_mode((1579,873))
	table = pygame.image.load('pool_table.png')
	screen = pygame.display.set_mode((1579,873))
	table = pygame.image.load('pool_table.png')
	screen.blit(table,(0,0))
	while(True):
		t.ballList = detection.detectBalls
		# cue = detection.detectCue # need a function to detect the cue and return it as something, maybe a line or just two points
		# t.initializeHitFromCue(cue)
		for ball in t.ballList:
			pygame.draw.circle(screen, t.colors[ball.num], [int(x) for x in ball.pos], ball.radius)
		pygame.display.update()
		for x in range(100):
			t.ballList = physics.run(t.ballList, t.walls, t.pockets)
			for ball in t.ballList:
				pygame.draw.circle(screen, t.colors[ball.num], [int(x) for x in ball.pos], 1)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()

if __name__ == '__main__': # so this is currently pseudo-code, and we will need to define these explicit functions that will return specific values
	activeProjection()
