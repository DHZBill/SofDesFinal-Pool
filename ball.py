#ball class created here, holds ball positions, number, etc.
import math

class ball:
	'''Ball class for all of the balls on the table'''
	def __init__(self, xpos, ypos, number, pocketed = False, pocketNum = 0, xv = 0, yv = 0, ballRadius = 20, mass = 1, mag = 0):
		'''Balls require an x and y position as well as what number they are, where the number 0 indicates the cue ball'''
		self.pos = [xpos, ypos]
		self.num = number
		self.pstate = pocketed
		self.pocket = pocketNum
		self.vel = [xv, yv] # unit vector
		self.velMagnitude = mag
		self.radius = ballRadius
		self.mass = mass
	def checkCollision(self, otherBall):
		'''Returns true if colliding with the other ball, else false if no collision'''
		if(self.pstate or otherBall.pstate):
			return False
		return math.sqrt((self.pos[0] - otherBall.pos[0])**2 + (self.pos[1] - otherBall.pos[1])**2) <= (self.radius * 2)
	def checkPocketed(self, pocketList, pocketRadius):
		'''Returns true if this instance of the ball is in a pocket, otherwise returns false'''
		for p in pocketList:
			if math.sqrt((self.pos[0] - p[0])**2 + (self.pos[1] - p[1])**2) < (self.radius + pocketRadius):
				self.pstate = True
				self.pocketNum = p[2]
				self.vel = [0, 0]
				self.velMagnitude = 0
				self.pos = [p[0], p[1]]
				return True
		return False
	def wallCollision(self, walls):
		'''Checks for collision with any walls, rebounding off of the walls in the event of a collision'''
		if self.pos[1] - self.radius <= walls[0]:
			self.vel[1] = self.vel[1] * -1
			self.pos[1] = walls[0] + self.radius + 1
		if self.pos[1] + self.radius >= walls[1]:
			self.vel[1] = self.vel[1] * -1
			self.pos[1] = walls[1] - self.radius - 1
		if self.pos[0] - self.radius <= walls[2]:
			self.vel[0] = self.vel[0] * -1
			self.pos[0] = walls[2] + self.radius + 1
		if self.pos[0] + self.radius >= walls[3]:
			self.vel[0] = self.vel[0] * -1
			self.pos[0] = walls[3] - self.radius - 1
		