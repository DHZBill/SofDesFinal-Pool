#ball class created here, holds ball positions, number, etc.
import math

class ball:
	def __init__(self, xpos, ypos, number, pocketed = False, pocketNum = 0, xv = 0, yv = 0, ballRadius = 5):
		self.pos = [xpos, ypos]
		self.num = number
		self.pstate = pocketed
		self.pocket = pocketNum
		self.vel = [xv, yv]
		self.radius = ballRadius
	def checkCollision(self, otherBall):
		#returns true if colliding with the other ball, else if no collision
		return math.sqrt((self.pos[0] - otherBall.pos[0])**2 + (self.pos[1] - otherBall.pos[1])**2) <= (radius * 2)
	def checkPocketed(self, pocketList, pocketRadius):
		for p in pocketList:
			if math.sqrt((self.pos[0] - otherBall.pos[0])**2 + (p.pos[1] - p.pos[1])**2) < (radius + pocketRadius):
				self.pocketed = True
				self.pocketNum = p.num
				return True
		return False
		