import pygame, math, physics, sys, cv2, calibration, detection
import numpy as np
from ball import ball
from draw_table import Table

def activeProjection(t, ballList): #input is a table object
	screen = pygame.display.set_mode((1579,873))
	table = pygame.image.load('pool_table.png')
	screen = pygame.display.set_mode((1579,873))
	table = pygame.image.load('pool_table.png')
	screen.blit(table,(0,0))
	while(True):
		t.ballList = detection.detectBalls
		cue = detection.detectCue
		t.initializeHitFromCue(cue)
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
	newImage, oldImage = calibration.calibrateVideoFeed # need a function that will allow for calibration of video feed and return both the sheared and original images
	ballList = detection.detectBalls # need an explicit function to detect balls and return the balls as a list, make sure to define the balls properly as a ball class
	t = Table(ballList)
	while(True):
		cue = detection.detectCue # need a function to detect the cue and return it as something, maybe a line or just two points
		t.ballList = detection.detectBalls
		t.initializeHitFromCue(cue) # need a function to specifically start a hit from the cue point
		t.draw_projection() # need to change this function to handle displaying from new inputs, might be best for it to return an image and handle displaying things in this file
