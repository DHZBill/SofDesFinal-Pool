#basic display graphics, draw table with pockets and balls given a list of ball objects
import pygame, math, physics, sys
from ball import ball
import numpy as np

class Table(object):
	'''
	Main table object that stores all balls relevant to the pool table
	'''
	def __init__(self, ballList, top = 84,bottom = 789,left = 84,right =1494, pockets = ((83,78, 1),(790,57, 2),(1499,80, 3),(83,791, 4),(790,810, 5),(1499,790, 6))):
		'''
		Constructor requires an argument of a list of balls to be put on the table
		'''
		self.colors = {0 : (255, 255, 255), 1 : (0, 255, 255), 2 : (255, 0, 255), 3 : (255, 255, 0), 4 : (0, 0, 255), 5 : (0, 255, 0), 6 : (255, 0, 0), 7 : (100, 100, 255), 8 : (0, 0, 0), 9 : (100, 255, 100), 10 : (255, 100, 100), 11 : (100, 100, 0), 12 : (100, 0, 100), 13 : (0, 100, 100), 14 : (50, 100, 255), 15 : (50, 255, 100), 16 : (100, 50, 255), 17 : (100, 255, 50), 18 : (50, 50, 50)} # dictionary for pool ball colors, only goes up to 18 currently
		self.pockets = pockets # pocket format is x coordinate, y coordinate, and pocket number
		self.walls = (top, bottom, left, right)
		self.ballList = ballList # ballList MUST include a cue ball (ball with allocated 'num' value 0), put it in index 0 in the list
		self.running = False

	def initializeHit(self, x, y):
		'''
		Hit applied to cue ball, x and y are the velocity" components that the cue ball will begin with
		'''
		self.ballList[0].velMagnitude = math.sqrt(x**2 + y**2)
		self.ballList[0].vel = [x/self.ballList[0].velMagnitude, y/self.ballList[0].velMagnitude]
		self.running = True

	def checkRunning(self):
		'''Checks to see if any balls on the table are still in motion'''
		if self.running:
			for ball in self.ballList:
				if(ball.velMagnitude != 0):
					return True
			self.running = False
		return False

	def draw_table(self):
		'''Animates the movement of balls on the table as they collide and rebound off of walls'''
		if(not self.checkRunning()):
			print("Nothing is moving you dingus")
			return
		screen = pygame.display.set_mode((1579,873))
		table = pygame.image.load('pool_table.png')
		while self.checkRunning():
			self.ballList = physics.run(self.ballList, self.walls, self.pockets)
			screen.blit(table,(0,0))
			for ball in self.ballList:
				pygame.draw.circle(screen, self.colors[ball.num], [int(x) for x in ball.pos], ball.radius)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
					sys.exit()
			pygame.display.update()
		pygame.time.wait(500)
		pygame.quit()
		sys.exit()

	def draw_projection(self, length = 100):
		'''Displays the projected path of the balls for a given period after the cue ball has been hit'''
		screen = pygame.display.set_mode((1579,873))
		table = pygame.image.load('pool_table.png')
		screen = pygame.display.set_mode((1579,873))
		table = pygame.image.load('pool_table.png')
		screen.blit(table,(0,0))
		for ball in self.ballList:
			pygame.draw.circle(screen, self.colors[ball.num], [int(x) for x in ball.pos], ball.radius)
		pygame.display.update()
		for x in range(length):
			self.ballList = physics.run(self.ballList, self.walls, self.pockets)
			for ball in self.ballList:
				pygame.draw.circle(screen, self.colors[ball.num], [int(x) for x in ball.pos], 1)
		pygame.display.update()
		while(True):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
					sys.exit()
	def initializeHitFromCue(cue1, cue2):
		'''Creates a hit on the cue ball from the cue in the event that the cue is aligned to hit the cue ball'''
		cueBall = self.ballList[0]
		dx = cue1[0] - cue2[0]
		dy = cue1[1] - cue2[1]
		xspace = np.linspace(cue1[0], cue2[0], max(int(dx), int(dy)))
		yspace = np.linspace(cue1[1], cue2[1], max(int(dx), int(dy)))
		for i in range(xspace): # double check this later to make sure these line up with points on the line
			if(math.sqrt((xspace[i] - cueBall.pos[0])**2 + (yspace[i] - cueBall.pos[1])**2) < (cueBall.radius)):
				t.initializeHit(dx, dy)
				break

if __name__ == '__main__':
	'''Sample running of the table class'''
	ball1 = ball(200, 300, 0)
	ball2 = ball(700, 290, 1)
	ball3 = ball(900, 250, 2)
	ball4 = ball(800, 250, 3)
	ball5 = ball(845, 150, 4)
	ball6 = ball(700, 790, 5)
	ball7 = ball(900, 150, 6)
	ball8 = ball(800, 650, 7)
	ball9 = ball(1245, 150, 8)
	t = Table([ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8, ball9])
	t.initializeHit(400, -250) # test collision between balls
	# t.initializeHit(100, 50) # test wall bouncing
	t.draw_table()
	t.draw_projection()


