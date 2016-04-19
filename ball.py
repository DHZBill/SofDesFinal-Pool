#ball class created here, holds ball positions, number, etc.
import math

class ball:
	def __init__(self, xpos, ypos, number, pocketed = False, pocketNum = 0, xv = 0, yv = 0, ballRadius = 20, mass = 1):
		self.pos = [xpos, ypos]
		self.num = number
		self.pstate = pocketed
		self.pocket = pocketNum
		self.vel = [xv, yv]
		self.radius = ballRadius
		self.mass = mass
	def checkCollision(self, otherBall): # returns true if colliding with the other ball, else if no collision
		return math.sqrt((self.pos[0] - otherBall.pos[0])**2 + (self.pos[1] - otherBall.pos[1])**2) <= (self.radius * 2)
	def checkPocketed(self, pocketList, pocketRadius):
		for p in pocketList:
			if math.sqrt((self.pos[0] - p[0])**2 + (self.pos[1] - p[1])**2) < (self.radius + pocketRadius):
				self.pocketed = True
				self.pocketNum = p[2]
				self.vel = [0, 0]
				self.pos = [p[0], p[1]]
				return True
		return False
	def wallCollision(self, walls):
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
		