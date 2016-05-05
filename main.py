import pygame, math, physics, sys, cv2, calibration
import numpy as np
from ball import ball
from draw_table import Table
from detection import Image_Detection as ImD
import cue_detection
walls = {'top' : 84, 'bottom' : 789, 'left' : 84, 'right' : 1494}

def activeProjection(): #input is a table object
	# cap = cv2.VideoCapture(0)
	# ret, frame = cap.read()
	img, warped, pts = calibration.calibrate_interface('pool_pic.JPG') # returns the original image, the sheared image, and the points used to warp the image
	# img, warped, pts = calibration.calibrate_interface(frame)
	I = ImD()
	I.wall_finder(warped)
	ballList = normalizeBallsToWalls(I, I.write_circles(warped))
	t = Table(ballList)
	screen = pygame.display.set_mode((1579,873))
	table = pygame.image.load('pool_table.png')
	screen = pygame.display.set_mode((1579,873))
	table = pygame.image.load('pool_table.png')
	screen.blit(table,(0,0))
	while(True):
		# ret, img = cap.read()
		# warped = calibration.four_point_transform(img, pts)
		t.ballList = normalizeBallsToWalls(I, I.write_circles(warped))
		# if cue_detection.Track_cue(warped) is not None:
			# cue1, cue2 = cue_detection.Track_cue(warped)
			# t.initializeHitFromCue(cue1, cue2)
		t.initializeHit(100, 0)
		if(t.ballList != None):
			for ball in t.ballList:
				pygame.draw.circle(screen, t.colors[ball.num], [int(x) for x in ball.pos], ball.radius)
			pygame.display.update()
			for x in range(100):
				t.ballList = physics.run(t.ballList, t.walls, t.pockets)
				for ball in t.ballList:
					pygame.draw.circle(screen, t.colors[ball.num], [int(x) for x in ball.pos], 1)
			pygame.display.update()
		else:
			print('no balls')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

def normalizeBallsToWalls(I, ballList):
	return [ball(int(float(b.pos[0] - I.lr_walls[0]) / (I.lr_walls[1] - I.lr_walls[0]) * (walls['right'] - walls['left']) + walls['left']), int(float(b.pos[1] - I.tb_walls[0]) / (I.tb_walls[1] - I.tb_walls[0]) * (walls['bottom'] - walls['top']) + walls['top']), b.num) for b in ballList]

if __name__ == '__main__': # so this is currently pseudo-code, and we will need to define these explicit functions that will return specific values
	activeProjection()
