#will take in list of ball objects and current cue position/direction, output end state of balls
#later will output lines for projected ball motions

# READ
# READ
# READ
# READ
# READ
# We do not actually have to implement physics in terms of "actual" physics (eg. forces, friction, etc.), but simply a simulation that will model similar effects.
# Basically, we only need balls to have a "velocity" in x and y components that will decay over time
import numpy as np
import math
from ball import ball

'''currently uneccessary'''
# class line(object):
# 	# draw lines
# 	def __init__(self, width = 1, color = pygame.Color('white'), table, start, end):
# 		self.width = width
# 		self.color = color
# 		self.table = table
# 		self.start = start
# 		self.end = end
# 	def draw(self):
# 		pygame.draw.line(self.table, 
# 						 self.color,
# 						 self.start,
# 						 self.end,
# 						 self.width)

def update(ball1):
	# Update ball position
	step = 0.2
	slow = 1
	if ball1.velMagnitude != 0:
		# dvx =  abs(ball1.vel[0] / math.sqrt(ball1.vel[0]**2 + ball1.vel[1]**2) * step)
		# dvy =  abs(ball1.vel[1] / math.sqrt(ball1.vel[0]**2 + ball1.vel[1]**2) * step)
		ball1.pos = [ball1.pos[0] + ball1.vel[0] * ball1.velMagnitude * step, ball1.pos[1] + ball1.vel[1] * ball1.velMagnitude * step] # updating ball positions based on velocity
	# if abs(ball1.vel[0]) > 0:
	# 	if abs(ball1.vel[0]) < dvx:
	# 		ball1.vel[0] = 0
	# 	else:
	# 		ball1.vel[0] += dvx if ball1.vel[0] < 0 else (-1 * dvx) # decreasing velocity
	# if abs(ball1.vel[1]) > 0:
	# 	if abs(ball1.vel[1]) < dvy:
	# 		ball1.vel[1] = 0
	# 	else:
	# 		ball1.vel[1] += dvy if ball1.vel[1] < 0 else (-1 * dvy)
	ball1.velMagnitude -= slow
	if(ball1.velMagnitude < 0):
		ball1.velMagnitude = 0
	return ball1

def ball_collision(ball_1, ball_2): 
		# Calculate velocity after collision between two balls
	m1 = ball_1.mass
	m2 = ball_2.mass
	pos_1 = np.array(ball_1.pos)
	pos_2 = np.array(ball_2.pos)
	vel_1 = np.array([ball_1.vel[0] * ball_1.velMagnitude, ball_1.vel[1] * ball_1.velMagnitude])
	vel_2 = np.array([ball_2.vel[0] * ball_2.velMagnitude, ball_2.vel[1] * ball_2.velMagnitude])

	n = pos_2 - pos_1
	un = n / math.sqrt(np.dot(n,n))
	ut = np.array(-un[1],un[0])

	vel_1n = np.dot(un, vel_1) # use numpy's dot, not vdot
	vel_1t = np.dot(ut, vel_1)
	vel_2n = np.dot(un, vel_2)
	vel_2t = np.dot(ut, vel_2)

	new_vel_1t = vel_1t * ut
	new_vel_2t = vel_2t * ut
	new_vel_1n = (vel_1n*(m1-m2) + 2*m2*vel_2n)/(m1+m2) * un
	new_vel_2n = (vel_2n*(m2-m1) + 2*m1*vel_1n)/(m1+m2) * un

	new_vel_1 = new_vel_1n + new_vel_1t
	new_vel_2 = new_vel_2n + new_vel_2t

	dist = math.sqrt(np.dot(pos_1 - pos_2, pos_1 - pos_2))

	while dist <= (ball_1.radius + ball_2.radius):
		pos_1 += new_vel_1 * 0.1
		pos_2 += new_vel_2 * 0.1
		dist = math.sqrt(np.dot(pos_1 - pos_2, pos_1 - pos_2))


	return [list(new_vel_1), list(new_vel_2), pos_1, pos_2]

		
def run(ballList, walls, pockets):
	for index in range(len(ballList)):
		ball = ballList[index]
		if not ball.pstate: #only operate on non-pocketed balls
			ball.wallCollision(walls)
			ball.checkPocketed(pockets, 30)
			if index < len(ballList) - 1: # ensures no out of index error by checking collisions for the last ball in the list
				for ball2 in ballList[index + 1:]:
					if(ball.checkCollision(ball2)):
						vel1, vel2, ball.pos, ball2.pos = ball_collision(ball, ball2)
						ball.velMagnitude = math.sqrt(vel1[0]**2 + vel1[1]**2)
						ball.vel = [vel1[0]/ball.velMagnitude, vel1[1]/ball.velMagnitude]
						ball2.velMagnitude = math.sqrt(vel2[0]**2 + vel2[1]**2)
						ball2.vel = [vel2[0]/ball2.velMagnitude, vel2[1]/ball2.velMagnitude]
	for ball in ballList:
		update(ball)
	return ballList















